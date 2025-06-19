#!/bin/bash

mkdir transactions-dataset
curl -L -o ./transactions-dataset/transactions-fraud-datasets.zip\
  https://www.kaggle.com/api/v1/datasets/download/computingvictor/transactions-fraud-datasets

unzip -o ./transactions-dataset/transactions-fraud-datasets.zip -d ./transactions-dataset
rm ./transactions-dataset/transactions-fraud-datasets.zip

export $(cat .env | xargs) && \
envsubst < ./grafana/provisioning/datasources/datasources.yml.template > ./grafana/provisioning/datasources/datasources.yml && \
docker-compose up --build -d
sleep 5
if (docker ps | grep kafka) then
    python main.py
else
    echo "Kafka is not running on port 9092. Please start Kafka and try again."
    docker-compose down
    exit 1
fi


