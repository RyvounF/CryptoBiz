import requests
from kafka import KafkaProducer
import json
import time
import logging

logging.debug("Debug")
logging.info("Info")
logging.warning("Warning")
logging.error("Error")
logging.critical("Critical")

kafka_bootstrap_servers = 'kafka0:9092,kafka1:9093,kafka2:9094'
kafka_topic = 'crypto_api'

producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

api_url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false&locale=en'

while True:
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        crypto_data_list = response.json()
        filtered_crypto_data_list = [
            {
                'id': item['id'],
                'name': item['name'],
                'price': float(item.get('current_price', '')),
                'change': item['price_change_percentage_24h'],
                'volume': item['total_volume'],
                'cap': item['market_cap']
            }
            for item in crypto_data_list
        ]

        for crypto_data in filtered_crypto_data_list:
            producer.send(kafka_topic, value=crypto_data)
            print("Send to Kafka!", crypto_data)

    except Exception as e:
        print("Error: ", e)

    time.sleep(60)