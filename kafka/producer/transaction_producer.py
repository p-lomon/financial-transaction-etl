from kafka import KafkaProducer
import pandas as pd
import random
from time import sleep
import simplejson as json

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    acks="all",
)

# Simulate transactions based on transaction csv
df = pd.read_csv("transactions-dataset/transactions_data.csv")
df = df.astype(
    {
        "zip": "str",
    }
)
df = df.fillna("")
for index, row in df.iterrows():
    print(f"Processing row {index + 1} of {len(df)}")
    transaction = {
        "id": row["id"],
        "date": row["date"],
        "client_id": row["client_id"],
        "card_id": row["card_id"],
        "amount": row["amount"],
        "use_chip": row["use_chip"],
        "merchant_id": row["merchant_id"],
        "merchant_city": row["merchant_city"],
        "merchant_state": row["merchant_state"],
        "zip": row["zip"],
        "mcc": row["mcc"],
        "errors": row["errors"],
    }
    print(f"Processing transaction {index + 1}: {transaction}")
    # transaction_json = json.dumps(transaction, allow_nan=False)
    producer.send("transactions", value=transaction)
    print(f"Sent transaction: {transaction}")
    sleep(random.uniform(0.1, 0.3))  # Simulate a delay between transactions
producer.flush()
print("All transactions sent successfully.")
