🚀 Salary Intelligence Dashboard
  AI, ML, and Data Science Jobs (2020–2025)
  This project is part of the Data Zoomcamp course and showcases a complete end-to-end data engineering pipeline using Docker, Airflow, DagsHub (DVC + Git + S3), PySpark, PostgreSQL, and Metabase—all running locally without paid cloud services.

🛠️ Why Not GCP or AWS?
As a student, I aimed to build a professional-grade data engineering project without relying on paid cloud platforms like GCP or AWS. While GCP offers a 3-month free trial, I had already used it up before starting this project.

Instead, I used DagsHub, which offers free data lake storage powered by AWS S3 behind the scenes. This allowed me to version datasets using DVC, push them to a remote storage, and still avoid direct AWS billing.

📦 Project Summary
Workflow:
Kaggle Dataset → DagsHub (Data Lake) → PostgreSQL (Data Warehouse) → PySpark (Transformation) → Metabase (Visualization)

Processing Mode:
Since the dataset is updated weekly, I implemented batch processing with Airflow to automate the pipeline.

Tech Stack:
Docker, Docker Compose, Airflow, DagsHub + DVC, PySpark, PostgreSQL, Metabase, Kaggle API

🧠 Project Goal
To build an automated data pipeline that:

Downloads weekly-updated salary data from Kaggle.

Pushes the raw dataset to a data lake (DagsHub via DVC).

Loads data into a PostgreSQL data warehouse.

Transforms data using PySpark.

Visualizes insights with Metabase dashboards.

🛠 Tech Stack

·Data Ingestion: Airflow, Kaggle API
·Data Lake: DagsHub (with DVC for versioning)
·Data Warehouse: PostgreSQL
·Transformation Engine: PySpark
·Orchestration: Airflow (with Docker)
·Visualization: Metabase
·Environment: Docker & Docker Compose

📦 Project Structure

datazoomcamp_project2025/
├── dags/                   # Airflow DAGs
├── jars/                  # JDBC driver for Postgres
├── Dockerfile              # Airflow custom image (with Java)
├── requirements.txt        # Python dependencies
├── docker-compose.yaml     # Docker Compose setup
├── instructions/           # Setup instructions
└── .env                    # (Not included in repo - add manually)

🔧 Prerequisites
 ·Docker & Docker Compose
 ·Kaggle API Token
 ·DagsHub account
 ·Git installed

 ⚙️ Setup Instructions
1. Clone the Repository
  git clone ～
  cd datazoomcamp_project2025
2. Configure Environment Variables
Create a .env file in the root directory with the following content:
DAGSHUB_REPO_OWNER=your_dagshub_username
DAGSHUB_REPO_NAME=your_repo_name
DAGSHUB_USER_TOKEN=your_dagshub_token
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_key
DVC_USERNAME=your_dvc_username
DVC_PASSWORD=your_dvc_password
3. Download JDBC Driver
Download the latest PostgreSQL JDBC Driver (e.g., postgresql-42.7.4.jar) and place it in the jars/ directory. I already put it in.

🚀 Running the Project

  docker-compose build
  docker-compose up -d

This will:
Build a custom Airflow image with Java (for PySpark).
Start Airflow, PostgreSQL, and Metabase services.
🛑 If any ports (like 3000 or 8080) are in use, update docker-compose.yaml.

🌐 Service Interfaces

Airflow UI: http://localhost:8080
Metabase UI: http://localhost:3000

🧩 How the Pipeline Works (Airflow DAG: datazoomcamp_pipeline)

Step	Description
1️⃣	Download Kaggle dataset using BashOperator
2️⃣	Push dataset to DagsHub via Git + DVC
3️⃣	Pull dataset from DagsHub for processing
4️⃣	Load CSV into PostgreSQL
5️⃣	Use PySpark for transformation: cleaning, standardizing, salary classification
✅	Output saved to salaries_transformed table

🧪 Inspecting Transformed Data

 Metabase Dashboard
Add a new database:
Type: PostgreSQL
Host: postgres-data
Port: 5432
Username: root
Password: root
DB Name: datadb

📊 Dashboard Examples
<img width="1045" alt="Screenshot 2025-04-21 at 21 02 18" src="https://github.com/user-attachments/assets/d1ecb91b-3539-426b-bb36-bcee75debc5d" />
