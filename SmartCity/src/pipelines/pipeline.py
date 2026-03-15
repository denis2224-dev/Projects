from __future__ import annotations

from src.ingestion.extract_weather import load_config, extract_weather
from src.ingestion.extract_air_quality import extract_air_quality
from src.transformation.clean_data import clean_and_save
from src.transformation.feature_engineering import engineer_features
from src.loading.load_postgres import load_to_postgres


def main() -> None:
    config = load_config()

    weather_record = extract_weather(config)
    air_record = extract_air_quality(config)

    df, output_path = clean_and_save(weather_record, air_record)
    df = engineer_features(df)

    load_to_postgres(df, config)

    print(df.head())
    print(f"\nProcessed file saved to: {output_path}")
    print("\nPipeline run completed successfully.")


if __name__ == "__main__":
    main()