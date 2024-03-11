from kafka import KafkaConsumer
import json
import logging
import os
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

logging.basicConfig(level=logging.DEBUG)

logging.error("Error")
logging.critical("Critical")

kafka_bootstrap_servers = 'kafka0:9092,kafka1:9093,kafka2:9094'
kafka_topic = 'crypto'
bucket = "crypto"
token = os.environ.get("INFLUXDB_TOKEN")

org = "Binance"
url = "http://influxdb:8086"
client = InfluxDBClient(url=url, token=token, org=org)

write_api = client.write_api(write_options=SYNCHRONOUS)
consumer = KafkaConsumer(kafka_topic, bootstrap_servers=kafka_bootstrap_servers, group_id='my-group',
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')))

for message in consumer:
    crypto_data = message.value
    try:

        point = Point("crypto_data") \
            .tag("id", crypto_data['id']) \
            .field("name", crypto_data['name']) \
            .field("price", crypto_data['price']) \
            .field("change", crypto_data['change']) \
            .field("volume", crypto_data['volume']) \
            .field("cap", crypto_data['cap'])

        write_api.write(bucket=bucket, record=point)
        print("Received from Kafka:", crypto_data["name"])
        print(f"Send to InfluxDB: {point}")

    except Exception as e:
        print("Error processing Kafka message:", e)
