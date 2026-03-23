# 🏙️ SmartCity

SmartCity is a smart city environmental monitoring project that collects weather and air quality data from public APIs, transforms the raw responses into a structured analytical dataset, stores the final data in PostgreSQL, and prepares the data for analytics, machine learning, and visualization.

The project is designed as a complete ETL based portfolio project for data engineering, data analytics, and machine learning roles.

## 💡 Project Value

This project shows how environmental data can be transformed into a reusable analytics and machine learning dataset through a clean, modular, and scalable pipeline. It reflects practical workflows used in data engineering and intelligent city monitoring systems.

## ✍️ Overview

SmartCity integrates environmental data into a single workflow:

* weather data collection
* air quality data collection
* raw data persistence
* data cleaning and merging
* feature engineering
* processed dataset generation
* PostgreSQL loading
* analytical querying
* machine learning ready dataset preparation

## 🔑 Key Features

* real time weather extraction from OpenWeather
* real time air quality extraction from OpenWeather
* raw JSON storage for traceability and debugging
* clean merged dataset stored as CSV
* engineered features for analytics and machine learning
* automatic loading into PostgreSQL
* modular Python project structure
* SQL layer prepared for analytics queries
* ML module placeholder for pollution prediction
* dashboard placeholder for visualization

## 🏛️ Architecture

The project follows an ETL architecture:

1. Extract data from external APIs
2. Transform raw responses into a clean structured format
3. Load the final dataset into PostgreSQL

### 📊 Data Flow

```text
Weather API + Air Quality API
            ↓
        Extraction
            ↓
      Raw JSON Storage
            ↓
     Cleaning and Merge
            ↓
   Feature Engineering
            ↓
 Processed CSV Dataset
            ↓
     PostgreSQL Table
            ↓
   SQL Analytics / ML / Dashboard
```

## 📁 Project Structure

```text
SmartCity/

config/
    config.yaml

data/
    raw/
    processed/

src/
    ingestion/
        extract_weather.py
        extract_air_quality.py

    transformation/
        clean_data.py
        feature_engineering.py

    loading/
        load_postgres.py

    pipelines/
        pipeline.py

    utils/
        logger.py
        helpers.py

sql/
    schema.sql
    analytics_queries.sql

ml/
    train_model.py
    predict.py

notebooks/
    exploration.ipynb

dashboard/

tests/
    test_pipeline.py

requirements.txt
README.md
```

## 🧑‍💻 Technologies Used

* Python
* Requests
* PyYAML
* Pandas
* PostgreSQL
* SQLAlchemy
* Psycopg2
* Scikit learn
* Jupyter Notebook
* Streamlit

## ⚙️ ETL Components

### 📥 Extract

Extraction is handled by:

* `src/ingestion/extract_weather.py`
* `src/ingestion/extract_air_quality.py`

These modules:

* read API configuration from `config/config.yaml`
* call the weather and air quality endpoints
* validate responses
* save raw JSON payloads in `data/raw/`
* return flattened Python dictionaries for downstream processing

### 🧹 Transform

Transformation is handled by:

* `src/transformation/clean_data.py`
* `src/transformation/feature_engineering.py`

These modules:

* merge weather and air quality observations into one record
* clean text and numeric fields
* standardize timestamps
* generate analytical and ML oriented features

Current engineered features include:

* `hour`
* `day_of_week`
* `month`
* `is_weekend`
* `temp_humidity_interaction`
* `temp_wind_interaction`
* `pm_ratio`
* `pollution_load`

### 📤 Load

Loading is handled by:

* `src/loading/load_postgres.py`

This module:

* builds the PostgreSQL connection string
* creates the destination table if needed
* loads the final transformed dataset into PostgreSQL

## 🗂️ Dataset

The project generates its own dataset from API observations.

### 📄 Raw Dataset

Raw API responses are saved as JSON files in:

* `data/raw/`

### 📘 Processed Dataset

The processed dataset is saved as:

* `data/processed/environment_data.csv`

This file contains the cleaned and merged environmental observations.

### 🗃️ Database Dataset

The final dataset is also stored in PostgreSQL inside the table:

* `environment_data`

## 🛢️ Database

The PostgreSQL layer is used for structured storage and analytics.

### 🧱 Schema

The database schema is defined in:

* `sql/schema.sql`

The main table contains:

* location fields
* weather measurements
* air pollution measurements
* timestamps
* engineered features

### 🔎 Example Queries

Example database inspection:

```bash
psql -d smartcity -c "\dt"
psql -d smartcity -c "SELECT city, temperature, aqi, pm2_5, pipeline_run_at FROM environment_data;"
```

## 🛠️ Configuration

Project configuration is stored in:

* `config/config.yaml`

Typical configuration includes:

* OpenWeather API key
* weather endpoint
* air quality endpoint
* target city and coordinates
* PostgreSQL connection settings

## 🚀 How to Run

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the project

Fill in `config/config.yaml` with:

* your OpenWeather API key
* location coordinates
* PostgreSQL settings

### 4. Start PostgreSQL

Example on macOS with Homebrew:

```bash
brew services start postgresql@18
```

### 5. Create the database

```bash
createdb smartcity
```

### 6. Run the pipeline

```bash
python -m src.pipelines.pipeline
```

## 📦 Pipeline Output

A pipeline run produces:

* raw weather JSON file
* raw air quality JSON file
* processed CSV dataset
* new row inserted into PostgreSQL

## 📈 SQL Analytics

SQL analytics are organized in:

* `sql/analytics_queries.sql`

This layer is intended for queries such as:

* daily pollution averages
* hourly pollution patterns
* weather and pollution comparisons
* top pollution observations



## 🤖 Machine Learning Engine

Machine learning modules are organized in:

* `ml/train_model.py`
* `ml/random_forest.py` ( for future model implementation )

The ML layer is intended for pollution prediction using the collected dataset and also a synthetic AI generated dataset.



## 🎯 Example Use Cases

SmartCity can be used as a portfolio project to demonstrate:

* ETL pipeline design
* API based ingestion
* data transformation and cleaning
* relational database loading
* SQL analytics
* feature engineering
* machine learning readiness
* modular Python architecture

## 📌 Current Deliverables

The project currently includes:

* a working weather ingestion script
* a working air quality ingestion script
* raw JSON persistence
* processed CSV generation
* PostgreSQL integration
* a complete ETL pipeline entry point
* a starter machine learning structure
* a repository structure ready for extension with analytics, dashboarding, and testing

## 🌍 Future Expansion

SmartCity is structured so it can be extended with:

* scheduled pipeline execution
* larger historical datasets
* more advanced forecasting models
* richer dashboards
* cloud deployment
* Docker based reproducibility
* CI testing and validation

## 📬 Contact / Notes

This README can be adapted further with screenshots, database query outputs, model evaluation plots, and dashboard previews once those modules are completed.
