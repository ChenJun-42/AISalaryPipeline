<h1 align="center" style="color:#2b6cb0;">🚀 Salary Intelligence Dashboard</h1>
<h3 align="center">AI, ML, and Data Science Jobs (2020–2025)</h3>

<p>This project is part of the <b>Data Zoomcamp</b> course and showcases a complete end-to-end data engineering pipeline using <b>Docker, Airflow, DagsHub (DVC + Git + S3), PySpark, PostgreSQL</b>, and <b>Metabase</b>—all running locally without paid cloud services.</p>

<h2>🛠️ Why Not GCP or AWS?</h2>
<p>
As a student, I aimed to build a professional-grade data engineering project without relying on paid cloud platforms like GCP or AWS. While GCP offers a 3-month free trial, I had already used it up before starting this project.
</p>
<p>
Instead, I used <b>DagsHub</b>, which offers free data lake storage powered by AWS S3 behind the scenes. This allowed me to version datasets using DVC, push them to a remote storage, and still avoid direct AWS billing.
</p>

<h2>📦 Project Summary</h2>
<h4>Workflow:</h4>
<p>
Kaggle Dataset → <b>DagsHub</b> (Data Lake) → <b>PostgreSQL</b> (Data Warehouse) → <b>PySpark</b> (Transformation) → <b>Metabase</b> (Visualization)
</p>

<h4>Processing Mode:</h4>
<p>
Since the dataset is updated weekly, I implemented <b>batch processing</b> with Airflow to automate the pipeline.
</p>

<h4>Tech Stack:</h4>
<ul>
  <li>Docker, Docker Compose</li>
  <li>Airflow</li>
  <li>DagsHub + DVC</li>
  <li>PySpark</li>
  <li>PostgreSQL</li>
  <li>Metabase</li>
  <li>Kaggle API</li>
</ul>

<h2>🧠 Project Goal</h2>
<p>To build an automated data pipeline that:</p>
<ul>
  <li>Downloads weekly-updated salary data from Kaggle.</li>
  <li>Pushes the raw dataset to a data lake (DagsHub via DVC).</li>
  <li>Loads data into a PostgreSQL data warehouse.</li>
  <li>Transforms data using PySpark.</li>
  <li>Visualizes insights with Metabase dashboards.</li>
</ul>

<h2>🛠 Tech Stack</h2>
<ul>
  <li><b>Data Ingestion:</b> Airflow, Kaggle API</li>
  <li><b>Data Lake:</b> DagsHub (with DVC for versioning)</li>
  <li><b>Data Warehouse:</b> PostgreSQL</li>
  <li><b>Transformation Engine:</b> PySpark</li>
  <li><b>Orchestration:</b> Airflow (with Docker)</li>
  <li><b>Visualization:</b> Metabase</li>
  <li><b>Environment:</b> Docker & Docker Compose</li>
</ul>

<h2>📦 Project Structure</h2>
<pre>
datazoomcamp_project2025/
├── dags/                   # Airflow DAGs
├── jars/                   # JDBC driver for Postgres
├── Dockerfile              # Airflow custom image (with Java)
├── requirements.txt        # Python dependencies
├── docker-compose.yaml     # Docker Compose setup
├── instructions/           # Setup instructions
└── .env                    # (Not included in repo - add manually)
</pre>

<h2>🔧 Prerequisites</h2>
<ul>
  <li>Docker & Docker Compose</li>
  <li>Kaggle API Token</li>
  <li>DagsHub account</li>
  <li>Git installed</li>
</ul>

<h2>⚙️ Setup Instructions</h2>
<ol>
  <li>Clone the Repository</li>
  <pre><code>git clone ～  
cd datazoomcamp_project2025</code></pre>

  <li>Configure Environment Variables</li>
  <p>Create a <code>.env</code> file in the root directory with the following content:</p>
  <pre><code>
DAGSHUB_REPO_OWNER=your_dagshub_username
DAGSHUB_REPO_NAME=your_repo_name
DAGSHUB_USER_TOKEN=your_dagshub_token
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_key
DVC_USERNAME=your_dvc_username
DVC_PASSWORD=your_dvc_password
</code></pre>

  <li>Download JDBC Driver</li>
  <p>Download the latest PostgreSQL JDBC Driver (e.g., postgresql-42.7.4.jar) and place it in the <code>jars/</code> directory. I already put it in.</p>
</ol>

<h2>🚀 Running the Project</h2>
<pre><code>
docker-compose build  
docker-compose up -d
</code></pre>

<p>This will:</p>
<ul>
  <li>Build a custom Airflow image with Java (for PySpark).</li>
  <li>Start Airflow, PostgreSQL, and Metabase services.</li>
</ul>

<p>🛑 If any ports (like 3000 or 8080) are in use, update <code>docker-compose.yaml</code>.</p>

<h2>🌐 Service Interfaces</h2>
<ul>
  <li><b>Airflow UI:</b> <a href="http://localhost:8080">http://localhost:8080</a></li>
  <li><b>Metabase UI:</b> <a href="http://localhost:3000">http://localhost:3000</a></li>
</ul>

<h2>🧩 How the Pipeline Works (Airflow DAG: datazoomcamp_pipeline)</h2>
<table>
  <tr><th>Step</th><th>Description</th></tr>
  <tr><td>1️⃣</td><td>Download Kaggle dataset using <code>BashOperator</code></td></tr>
  <tr><td>2️⃣</td><td>Push dataset to DagsHub via Git + DVC</td></tr>
  <tr><td>3️⃣</td><td>Pull dataset from DagsHub for processing</td></tr>
  <tr><td>4️⃣</td><td>Load CSV into PostgreSQL</td></tr>
  <tr><td>5️⃣</td><td>Use PySpark for transformation: cleaning, standardizing, salary classification</td></tr>
  <tr><td>✅</td><td>Output saved to <code>salaries_transformed</code> table</td></tr>
</table>

<h2>🧪 Inspecting Transformed Data</h2>
<p><b>Metabase Dashboard</b></p>
<p>Add a new database:</p>
<ul>
  <li><b>Type:</b> PostgreSQL</li>
  <li><b>Host:</b> postgres-data</li>
  <li><b>Port:</b> 5432</li>
  <li><b>Username:</b> root</li>
  <li><b>Password:</b> root</li>
  <li><b>DB Name:</b> datadb</li>
</ul>

<h2>📊 Dashboard Examples</h2>
<img width="1045" alt="Screenshot 2025-04-21 at 21 02 18" src="https://github.com/user-attachments/assets/d1ecb91b-3539-426b-bb36-bcee75debc5d" />
