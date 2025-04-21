FROM apache/airflow:2.10.5

ENV AIRFLOW_HOME=/opt/airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

USER root
RUN apt-get update && apt-get install -y git unzip openjdk-17-jre-headless && apt-get clean

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]
USER airflow

WORKDIR $AIRFLOW_HOME

USER $AIRFLOW_UID