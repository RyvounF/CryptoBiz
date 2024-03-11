from kafka import KafkaConsumer
import json
import logging
import os
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import (SYNCHRONOUS)

logging.basicConfig(level=logging.DEBUG)
logging.error("Error")
logging.critical("Critical")

kafka_bootstrap_servers = 'kafka0:9092,kafka1:9093,kafka2:9094'
kafka_api_topic = 'crypto_api'
bucket_api = "crypto"
token = os.environ.get("INFLUXDB_TOKEN")

org = "Binance"
url = "http://influxdb:8086"
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

consumer_api = KafkaConsumer(kafka_api_topic, bootstrap_servers=kafka_bootstrap_servers, group_id='my-group',
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')))


for message in consumer_api:
    crypto_api_data = message.value
    try:
        point_api = Point("crypto_api_data")
        point_api.tag("id", crypto_api_data['id'])
        point_api.field("name", crypto_api_data['name'])
        point_api.field("price", crypto_api_data['price'])
        point_api.field("change", crypto_api_data['change'])
        point_api.field("volume", crypto_api_data['volume'])
        point_api.field("cap", crypto_api_data['cap'])

        write_api.write(bucket=bucket_api, record=point_api)
        print("Received from Kafka:", crypto_api_data["name"])
        print(f"Send to InfluxDB: {point_api}")

    except Exception as e:
        print("Error processing Kafka message:", e)