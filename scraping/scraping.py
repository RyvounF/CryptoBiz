from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from kafka import KafkaProducer
import logging
import json
import time
logging.debug("Debug")
logging.info("Info")
logging.warning("Warning")
logging.error("Error")
logging.critical("Critical")

kafka_bootstrap_servers = 'kafka0:9092,kafka1:9093,kafka2:9094'
print(kafka_bootstrap_servers)
kafka_topic = 'crypto'
producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
options = Options()
options.add_argument('headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)
while True:
    for page in range(1, 26):
        driver.implicitly_wait(15)
        driver.get(f'https://crypto.com/price?page={page}')
        time.sleep(3)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        markets_div = soup.find('tr', {'class': 'css-1cxc880'})
        print("markets_div")

        if markets_div:
            markets = []
            print("markets_div find")
            market_blocks = soup.find_all('tr', {'class': 'css-1cxc880'})
            for block in market_blocks:
                id = block.find('span', {'class': 'chakra-text css-1jj7b1a'}).text.strip()
                name = block.find('p', {'class': 'chakra-text css-rkws3'}).text.strip()
                price = block.find('div', {'class': 'css-b1ilzc'}).text.strip()
                volume = block.find('td', {'class': 'css-15lyn3l'}).text.strip()
                change = block.find('td', {'class': 'css-vtw5vj'}).text.strip()
                cap = block.find_all('td', {'class': 'css-15lyn3l'})[1].text.strip()

                def parse_data(volume, cap, price, change):
                    volume = volume.replace(',', '.').replace('$', '')
                    cap = cap.replace('$', '')
                    price = price.replace('$', '')
                    change = change.replace('%', '').replace('+', '')

                    if ',' in change:
                        change_value = float(change.replace(',', ''))
                    else:
                        change_value = float(change) if change != 'N/A' else None

                    if ',' in price:
                        print(price + " price here")
                        price_value = float(price.replace(',', ''))
                    else:
                        price_value = float(price) if price != 'N/A' else None

                    if 'B' in cap:
                        cap_value = float(cap.replace('B', '')) * 1_000_000_000
                    elif 'M' in cap:
                        cap_value = float(cap.replace('M', '')) * 1_000_000
                    else:
                        cap_value = float(cap) if cap != 'N/A' else None

                    if 'B' in volume:
                        volume_value = float(volume.replace('B', '')) * 1_000_000_000
                    elif 'M' in volume:
                        volume_value = float(volume.replace('M', '')) * 1_000_000
                    elif 'K' in volume:
                        volume_value = float(volume.replace('K', '')) * 1_000
                    else:
                        print(volume + " volume here")
                        volume_value = float(volume.replace(',', '.')) if volume != 'N/A' else None

                    return volume_value, cap_value, price_value, change_value

                parsed_volume, parsed_cap, parsed_price, parsed_change = parse_data(volume, cap, price, change)

                market_data = {
                    'id': id,
                    'name': name,
                    'price': parsed_price,
                    'change': parsed_change,
                    'volume': parsed_volume,
                    'cap': parsed_cap,
                }
                print(market_data)
                markets.append(market_data)
            for market in markets:
                try:
                    crypto_data = market
                    producer.send(kafka_topic, value=crypto_data)
                    print("Send to Kafka!", crypto_data)
                except Exception as e:
                    print("Error!", e)


    else:
        print("Finish!")
    time.sleep(60)
