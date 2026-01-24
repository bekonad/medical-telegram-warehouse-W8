from dagster import op, job
import subprocess
import sys

@op
def scrape_telegram_data():
    subprocess.check_call([sys.executable, 'src/scraper.py'])

@op
def load_raw_to_postgres():
    subprocess.check_call([sys.executable, 'src/load_raw_to_postgres.py'])

@op
def download_images():
    subprocess.check_call([sys.executable, 'src/download_images.py'])

@op
def run_yolo_enrichment():
    subprocess.check_call([sys.executable, 'src/run_yolo.py'])

@op
def load_yolo_results():
    subprocess.check_call([sys.executable, 'src/load_yolo_to_postgres.py'])

@op
def run_dbt_transformations():
    subprocess.check_call(['dbt', 'run'])

@op
def run_dbt_tests():
    subprocess.check_call(['dbt', 'test'])

@job
def telegram_data_pipeline():
    scrape_telegram_data()
    load_raw_to_postgres()
    download_images()
    run_yolo_enrichment()
    load_yolo_results()
    run_dbt_transformations()
    run_dbt_tests()
