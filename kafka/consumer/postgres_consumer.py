from kafka import KafkaConsumer
from sqlmodel import create_engine, Field, SQLModel, Session
from pydantic import field_validator, BaseModel
from typing import Optional
import simplejson as json
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

DATABASE_URI = "postgresql://{}:{}@localhost:5432/{}".format(
    os.getenv("POSTGRES_USER"), os.getenv("POSTGRES_PASSWORD"), os.getenv("POSTGRES_DB")
)

consumer = KafkaConsumer(
    "transactions",
    bootstrap_servers=["localhost:9092"],
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)


class TransactionBase(BaseModel):
    id: int = Field(..., nullable=False, primary_key=True)
    date: datetime = Field(..., nullable=False)
    client_id: int = Field(..., nullable=False)
    card_id: int = Field(..., nullable=False)
    amount: float = Field(..., nullable=False)
    use_chip: str
    merchant_id: int
    merchant_city: str
    merchant_state: str = Field(max_length=2)
    zip: str = Field(max_length=10)
    mcc: int
    errors: Optional[str] = None
    is_suspicious: bool = Field(default=False)

    @field_validator("amount", mode="before")
    @classmethod
    def validate_amount(cls, v):
        v = float(v.replace("$", "").replace(",", ""))
        return v

    @field_validator("date", mode="before")
    @classmethod
    def parse_custom_date(cls, value):
        if isinstance(value, str):
            val = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            return val
        return value

    def model_post_init(self, __context):
        if self.amount < 0:
            self.is_suspicious = True


class Transaction(SQLModel, table=True):
    id: int = Field(..., nullable=False, primary_key=True)
    date: datetime = Field(..., nullable=False)
    client_id: int = Field(..., nullable=False)
    card_id: int = Field(..., nullable=False)
    amount: float = Field(..., nullable=False)
    use_chip: str
    merchant_id: int
    merchant_city: str
    merchant_state: str = Field(max_length=2)
    zip: str = Field(max_length=10)
    mcc: int
    errors: Optional[str] = None
    is_suspicious: bool = False


engine = create_engine(DATABASE_URI, echo=True)
SQLModel.metadata.create_all(engine)


for message in consumer:
    try:
        with Session(engine) as session:
            validated_data = TransactionBase(**message.value)
            transaction = Transaction(**validated_data.model_dump())
            session.add(transaction)
            print(f"Added transaction to session: {transaction}")
            session.commit()
    except Exception as e:
        print(f"Transaction insert failed: {e}")
        continue
