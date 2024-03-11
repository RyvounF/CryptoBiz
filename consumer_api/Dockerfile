FROM python:3.8

WORKDIR /docker

COPY consumer_api/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
ENV INFLUXDB_TOKEN=mJedwlV38eRtm4zsD65itGtpTUjhjCnp_c9QIdWgS9vM4jab_EiHrLs3Bu7-pv9p2zGpDBJmWHGW7hpReYaA4g==
COPY consumer_api/consumer_api.py .

CMD ["python3", "consumer_api.py"]
