from __future__ import annotations

from typing import Any

import pandas as pd
from sqlalchemy import create_engine, text


def build_connection_url(config: dict[str, Any]) -> str:
    db = config["database"]

    user = db["user"]
    password = db["password"]
    host = db["host"]
    port = db["port"]
    dbname = db["dbname"]

    if password:
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    return f"postgresql+psycopg2://{user}@{host}:{port}/{dbname}"


def create_table_if_not_exists(engine, table_name: str) -> None:
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        city TEXT,
        country TEXT,
        lat DOUBLE PRECISION,
        lon DOUBLE PRECISION,

        weather_main TEXT,
        weather_description TEXT,

        temperature DOUBLE PRECISION,
        feels_like DOUBLE PRECISION,
        temp_min DOUBLE PRECISION,
        temp_max DOUBLE PRECISION,
        pressure DOUBLE PRECISION,
        humidity DOUBLE PRECISION,
        visibility DOUBLE PRECISION,
        wind_speed DOUBLE PRECISION,
        wind_deg DOUBLE PRECISION,
        clouds_pct DOUBLE PRECISION,

        aqi DOUBLE PRECISION,
        co DOUBLE PRECISION,
        no DOUBLE PRECISION,
        no2 DOUBLE PRECISION,
        o3 DOUBLE PRECISION,
        so2 DOUBLE PRECISION,
        pm2_5 DOUBLE PRECISION,
        pm10 DOUBLE PRECISION,
        nh3 DOUBLE PRECISION,

        weather_timestamp TIMESTAMP,
        air_quality_timestamp TIMESTAMP,
        weather_source TEXT,
        air_quality_source TEXT,
        weather_raw_file TEXT,
        air_quality_raw_file TEXT,
        pipeline_run_at TIMESTAMP,

        hour DOUBLE PRECISION,
        day_of_week DOUBLE PRECISION,
        month DOUBLE PRECISION,
        is_weekend DOUBLE PRECISION,
        temp_humidity_interaction DOUBLE PRECISION,
        temp_wind_interaction DOUBLE PRECISION,
        pm_ratio DOUBLE PRECISION,
        pollution_load DOUBLE PRECISION
    );
    """

    with engine.begin() as connection:
        connection.execute(text(create_table_sql))


def load_to_postgres(df: pd.DataFrame, config: dict[str, Any]) -> None:
    table_name = config["database"].get("table_name", "environment_data")
    connection_url = build_connection_url(config)

    engine = create_engine(connection_url)
    create_table_if_not_exists(engine, table_name)

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
    )

    print(f"Loaded {len(df)} row(s) into PostgreSQL table '{table_name}'.")