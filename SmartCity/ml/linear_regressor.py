from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import pickle

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


@dataclass
class Config:
    base_dir: Path = Path(__file__).resolve().parent.parent
    data_path: Path = base_dir / "data" / "processed" / "environment_data_generated.csv"
    target_column: str = "pm2_5"
    timestamp_column: str = "pipeline_run_at"
    prediction_horizon: int = 1
    test_size: float = 0.2
    artifacts_dir: Path = base_dir / "ml" / "artifacts"
    min_rows_required: int = 12


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError("Dataset is empty.")
    return df


def prepare_dataset(df: pd.DataFrame, config: Config) -> tuple[pd.DataFrame, pd.Series]:
    df = df.copy()

    if config.target_column not in df.columns:
        raise ValueError(f"Missing target column: {config.target_column}")

    if config.timestamp_column not in df.columns:
        raise ValueError(f"Missing timestamp column: {config.timestamp_column}")

    df[config.timestamp_column] = pd.to_datetime(df[config.timestamp_column], errors="coerce")
    df = df.dropna(subset=[config.timestamp_column])
    df = df.sort_values(config.timestamp_column).reset_index(drop=True)

    future_target = f"{config.target_column}_future"
    df[future_target] = df[config.target_column].shift(-config.prediction_horizon)
    df = df.dropna(subset=[future_target]).reset_index(drop=True)

    if len(df) < config.min_rows_required:
        raise ValueError(
            f"Not enough rows to train the model. Current rows: {len(df)}. Collect more data first."
        )

    columns_to_drop = [
        config.target_column,
        future_target,
        "weather_timestamp",
        "air_quality_timestamp",
        "pipeline_run_at",
        "weather_source",
        "air_quality_source",
    ]

    X = df.drop(columns=columns_to_drop, errors="ignore")
    y = df[future_target]

    return X, y


def chronological_split(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    split_index = int(len(X) * (1 - test_size))

    if split_index <= 0 or split_index >= len(X):
        raise ValueError("Invalid split index. Adjust test_size or dataset size.")

    X_train = X.iloc[:split_index].copy()
    X_test = X.iloc[split_index:].copy()
    y_train = y.iloc[:split_index].copy()
    y_test = y.iloc[split_index:].copy()

    return X_train, X_test, y_train, y_test


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    numeric_features = X.select_dtypes(include=["int64", "float64", "int32", "float32"]).columns.tolist()
    categorical_features = X.select_dtypes(include=["object", "string", "category", "bool"]).columns.tolist()

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )


def build_model(preprocessor: ColumnTransformer) -> Pipeline:
    return Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", LinearRegression()),
        ]
    )


def evaluate_model(
    model: Pipeline,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict[str, float]:
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)

    metrics = {
        "train_mae": float(mean_absolute_error(y_train, train_pred)),
        "test_mae": float(mean_absolute_error(y_test, test_pred)),
        "train_rmse": float(root_mean_squared_error(y_train, train_pred)),
        "test_rmse": float(root_mean_squared_error(y_test, test_pred)),
        "train_r2": float(r2_score(y_train, train_pred)),
        "test_r2": float(r2_score(y_test, test_pred)),
    }

    return metrics


def plot_actual_vs_predicted(y_test: pd.Series, y_pred, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred)
    plt.xlabel("Actual future pm2_5")
    plt.ylabel("Predicted future pm2_5")
    plt.title("Linear Regression: Actual vs Predicted")

    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val])

    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def save_artifacts(model: Pipeline, metrics: dict[str, float], artifacts_dir: Path) -> None:
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    with open(artifacts_dir / "linear_regression_model.pkl", "wb") as file:
        pickle.dump(model, file)

    with open(artifacts_dir / "linear_regression_metrics.json", "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2, ensure_ascii=False)


def main() -> None:
    config = Config()
    artifacts_dir = config.artifacts_dir
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    df = load_data(config.data_path)
    X, y = prepare_dataset(df, config)
    X_train, X_test, y_train, y_test = chronological_split(X, y, config.test_size)

    preprocessor = build_preprocessor(X_train)
    model = build_model(preprocessor)

    model.fit(X_train, y_train)

    metrics = evaluate_model(model, X_train, y_train, X_test, y_test)
    y_pred = model.predict(X_test)

    print("Linear Regression Metrics:")
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}")

    plot_actual_vs_predicted(
        y_test,
        y_pred,
        artifacts_dir / "actual_vs_predicted.png",
    )

    save_artifacts(model, metrics, artifacts_dir)

    print(f"\nArtifacts saved to: {artifacts_dir.resolve()}")


if __name__ == "__main__":
    main()