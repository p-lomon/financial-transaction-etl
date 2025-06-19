#  Financial Transaction Data pipeline 

A simulated real-time data pipeline to stream, store, and visualize financial transactions with Kafka, PostgreSQL, and Grafana. This project demonstrates a fault-tolerant, scalable architecture suitable for financial fraud detection use cases.

---

##  Project Overview

This project simulates real-time financial transactions using transaction data set from [Kaggle](https://www.kaggle.com/datasets/computingvictor/transactions-fraud-datasets). Kafka is used for message streaming, PostgreSQL for structured storage, and Grafana for live dashboards. Suspicious transactions are flagged based on custom logic and stored for analysis.

---

##  Architecture

```plaintext
[Kaggle Transaction Dataset]
           ↓
       [Kafka Producer]
           ↓
        Kafka Topic
           ↓
      [Kafka Consumer]
           ↓
     [PostgreSQL Database]
           ↓
         [Grafana]
```


| Component      | Technology                 |
| -------------- | -------------------------- |
| Data Streaming | Apache Kafka, kafka-python |
| Data Storage   | PostgreSQL (Dockerized)    |
| Dashboard      | Grafana                    |
| Scripting      | Python + SQLModel          |
| Orchestration  | Docker Compose             |


# How to Run
1. Clone the Repo
```
git clone https://github.com/yourusername/fraud-detection-pipeline.git
cd fraud-detection-pipeline
```

2. Create `.env file and add the following to the file
```
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database_name
```
4. Install the required python package.
If using pip, 
```
pip install .
```
   Or in uv
```
uv pip install .
```
5. Start service and orchestrator script
```
bash start.sh
```
This starts Kafka, PostgreSQL, and Grafana and the producer and consumer scripts.


# Grafana Dashboard
Access Grafana at: http://localhost:3000

Default credentials: admin / admin

The dashboard displays: 
 - Total number of transaction
 - Suspicious vs Normal transaction count
 - Location where the suspicious transaction is made
 - Histogram for transaction amount


## Suspicious Transaction Criteria
As of now, transactions are flagged as suspicious based on:

 - Metadata contains errors

