# Airflow POC Project

The Airflow POC project aims to demonstrate the capabilities and benefits of using Apache Airflow, an open-source platform to programmatically author, schedule, and monitor workflows. This project serves as a starting point for exploring Airflow's features and understanding how it can be integrated into your data pipeline.


## Get Started
### 1. Download docker-compose.yaml
- Use this command to download the file:
```bash 
Curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.0/docker-compose.yaml'
```

### 2. Setting on Linux
- Run these commands to create some directories and a file:


``` bash
mkdir -p ./dags ./logs ./plugins ./config ./data
echo -e "AIRFLOW_UID=$(id -u)" > .env
```
### 3. Create Dockerfile and config requirements.txt
- Put this content in your Dockerfile:
``` bash
FROM apache/airflow:2.8.0
USER airflow
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --user -r /tmp/requirements.txt
```

### 4. Build Docker Image 
- Use this command to build the Docker image:
``` bash
docker build -t apache/airflow:2.8.0 .
```

### 5. Config Docker-compose.yaml file for folder data to csv file
 - Add these lines to the file. They tell Docker where to find your data:
```bash
  volumes:
    - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
    - ${AIRFLOW_PROJ_DIR:-.}/logs:/opt/airflow/logs
    - ${AIRFLOW_PROJ_DIR:-.}/data:/opt/airflow/data
    - ${AIRFLOW_PROJ_DIR:-.}/config:/opt/airflow/config
    - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins
```


### 6. Initialize the database
- Run this command to set up the database:

``` bash
docker compose up airflow-init
```

### 7. Running Airflow
- Finally, use this command to start Airflow:


``` bash
docker compose up
```