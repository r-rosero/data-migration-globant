# data-migration-globant

## Overview
This project is designed to clean and migrate data from CSV files to a PostgreSQL database. It also provides a REST API service to receive new data, backup data in AVRO format, and restore data from AVRO backups.

## Project Structure
- `api/`: Contains the API configuration and models.
- `data/`: Contains the CSV files and migration logs.
- `scripts/`: Contains the scripts for data cleaning, database table creation, data migration, and the main pipeline.
- `services/`: Contains the services for backup and restore.

## Setup
1. Create a virtual environment:
    ```sh
    python -m venv venv
    ```
2. Activate the virtual environment:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```
3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
### Data Cleaning and Migration
To run the data cleaning and migration pipeline:
```sh
python scripts/pipeline/main.py path/to/your/file.csv entity