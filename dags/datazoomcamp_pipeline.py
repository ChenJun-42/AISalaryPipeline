from datetime import datetime, timedelta
import os
import requests
import pandas as pd
import psycopg2
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col, upper

# Default args
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2025, 1, 1),
}

# Kaggle & DagsHub config
KAGGLE_DATASET_ID = "samithsachidanandan/the-global-ai-ml-data-science-salary-for-2025"
WORK_DIR = "/tmp/ds_salary_data"
DATA_DIR = f"{WORK_DIR}/data"
REPO_DIR = f"{WORK_DIR}/repo"
DVC_CMD = "/home/airflow/.local/bin/dvc"

DAGSHUB_REPO_OWNER = os.environ.get("DAGSHUB_REPO_OWNER", "shuchenjuncj")
DAGSHUB_REPO_NAME = os.environ.get("DAGSHUB_REPO_NAME", "my-first-repo")
DAGSHUB_USER_TOKEN = os.environ.get("DAGSHUB_USER_TOKEN")
FILE_PATH = "data/ds_salary/salaries.csv"
LOCAL_PATH = "/tmp/salaries.csv"

POSTGRES_HOST = "postgres-data"
POSTGRES_PORT = 5432
POSTGRES_DB = "datadb"
POSTGRES_USER = "root"
POSTGRES_PASSWORD = "root"
TABLE_NAME = "salaries"

def download_from_dagshub():
    url = f"https://dagshub.com/{DAGSHUB_REPO_OWNER}/{DAGSHUB_REPO_NAME}/raw/main/{FILE_PATH}"
    headers = {}
    if DAGSHUB_USER_TOKEN:
        headers["Authorization"] = f"token {DAGSHUB_USER_TOKEN}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    with open(LOCAL_PATH, "wb") as f:
        f.write(resp.content)

def load_to_postgres():
    df = pd.read_csv(LOCAL_PATH)
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    cur = conn.cursor()
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        {', '.join([f'"{col}" TEXT' for col in df.columns])}
    );
    """
    cur.execute(create_table_sql)
    conn.commit()
    cur.execute(f"TRUNCATE TABLE {TABLE_NAME};")
    for _, row in df.iterrows():
        placeholders = ','.join(['%s'] * len(row))
        insert_sql = f'INSERT INTO {TABLE_NAME} VALUES ({placeholders})'
        cur.execute(insert_sql, tuple(row))
    conn.commit()
    cur.close()
    conn.close()

def spark_transformation():
    spark = SparkSession.builder \
        .appName("PostgresSalariesETL") \
        .config("spark.jars", "/opt/airflow/jars/postgresql-42.7.4.jar") \
        .getOrCreate()

    df = spark.read.format("jdbc") \
        .option("url", "jdbc:postgresql://postgres-data:5432/datadb") \
        .option("dbtable", "salaries") \
        .option("user", "root") \
        .option("password", "root") \
        .option("driver", "org.postgresql.Driver") \
        .load()

    df = df.withColumn("job_title", upper(col("job_title")))
    df = df.withColumn("work_mode", when(col("remote_ratio") == 100, "Remote")
                                     .when(col("remote_ratio") == 0, "Onsite")
                                     .otherwise("Hybrid"))
    df = df.withColumn("experience_level_full",
        when(col("experience_level") == "SE", "Senior")
        .when(col("experience_level") == "MI", "Mid-level")
        .when(col("experience_level") == "EN", "Entry-level")
        .when(col("experience_level") == "EX", "Executive"))
    df = df.withColumn("company_size_full",
        when(col("company_size") == "S", "Small")
        .when(col("company_size") == "M", "Medium")
        .when(col("company_size") == "L", "Large"))
    df = df.withColumn("salary_level",
        when(col("salary_in_usd") < 50000, "Low")
        .when((col("salary_in_usd") >= 50000) & (col("salary_in_usd") < 150000), "Medium")
        .otherwise("High"))

    df.write.format("jdbc") \
        .option("url", "jdbc:postgresql://postgres-data:5432/datadb") \
        .option("dbtable", "salaries_transformed") \
        .option("user", "root") \
        .option("password", "root") \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()

    spark.stop()

with DAG(
    'full_etl_pipeline',
    default_args=default_args,
    description='Kaggle → DagsHub → Postgres → PySpark ETL pipeline',
    schedule_interval='@weekly',
    catchup=False,
) as dag:

    setup_directories = BashOperator(
        task_id='setup_directories',
        bash_command=f"""
            mkdir -p {DATA_DIR}
            mkdir -p {REPO_DIR}
            rm -rf {DATA_DIR}/* || true
            rm -rf {REPO_DIR}/* || true
        """
    )

    download_dataset = BashOperator(
        task_id='download_dataset',
        bash_command=f"""
            kaggle datasets download -d {KAGGLE_DATASET_ID} -p {DATA_DIR} --unzip --force
            ls -la {DATA_DIR}
        """
    )

    clone_repo = BashOperator(
        task_id='clone_repo',
        bash_command=f"""
            cd {REPO_DIR}
            git clone https://$DAGSHUB_REPO_OWNER:$DAGSHUB_USER_TOKEN@dagshub.com/$DAGSHUB_REPO_OWNER/$DAGSHUB_REPO_NAME.git . || \
            git clone https://oauth2:$DAGSHUB_USER_TOKEN@dagshub.com/$DAGSHUB_REPO_OWNER/$DAGSHUB_REPO_NAME.git .
            git config --local user.name "Airflow Robot"
            git config --local user.email "airflow@example.com"
        """
    )

    track_with_dvc = BashOperator(
        task_id='track_with_dvc',
        bash_command=f"""
            cd {REPO_DIR}
            mkdir -p data/ds_salary
            cp -r {DATA_DIR}/* data/ds_salary/
            if [ ! -d .dvc ]; then
                {DVC_CMD} init
                {DVC_CMD} remote add -d origin https://dagshub.com/$DAGSHUB_REPO_OWNER/$DAGSHUB_REPO_NAME.dvc
                git add .dvc/config
                git commit -m "Configure DVC remote"
            fi
            {DVC_CMD} add data/ds_salary
            git add data/ds_salary.dvc data/.gitignore
            if git status --porcelain | grep .; then
                git commit -m "Update Data Science Salary Dataset $(date +'%Y-%m-%d')"
            fi
        """
    )

    push_to_dagshub = BashOperator(
        task_id='push_to_dagshub',
        bash_command=f"""
            cd {REPO_DIR}
            git push https://$DAGSHUB_REPO_OWNER:$DAGSHUB_USER_TOKEN@dagshub.com/$DAGSHUB_REPO_OWNER/$DAGSHUB_REPO_NAME.git main
            {DVC_CMD} config --local core.remote origin
            {DVC_CMD} config --local remote.origin.url "https://dagshub.com/$DAGSHUB_REPO_OWNER/$DAGSHUB_REPO_NAME.dvc"
            {DVC_CMD} config --local remote.origin.auth basic
            {DVC_CMD} config --local remote.origin.user "$DVC_USERNAME"
            {DVC_CMD} config --local remote.origin.password "$DVC_PASSWORD"
            {DVC_CMD} push -r origin -v
        """
    )

    download_from_dagshub_task = PythonOperator(
        task_id="download_from_dagshub",
        python_callable=download_from_dagshub,
    )
    load_to_postgres_task = PythonOperator(
        task_id="load_to_postgres",
        python_callable=load_to_postgres,
    )
    spark_transformation_task = PythonOperator(
        task_id="spark_transformation",
        python_callable=spark_transformation,
    )

    # Set dependencies between tasks
    setup_directories >> download_dataset >> clone_repo >> track_with_dvc >> push_to_dagshub \
        >> download_from_dagshub_task >> load_to_postgres_task >> spark_transformation_task