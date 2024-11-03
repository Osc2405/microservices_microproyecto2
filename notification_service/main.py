import json
import os
from kafka import KafkaConsumer
from prometheus_client import start_http_server, Counter
from dotenv import load_dotenv

load_dotenv()

# Prometheus metrics configuration
EVENTS_CONSUMED = Counter("events_consumed", "Total number of events consumed")

# Kafka broker URL
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")


def consume_user_events():
    """Consume user registration events from Kafka."""
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BROKER_URL],
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )

    for message in consumer:
        event = message.value
        if event.get("event_type") == "UserRegistered":
            print("Event received:", event)
            EVENTS_CONSUMED.inc()  # Increment the counter for consumed events


if __name__ == "__main__":
    start_http_server(8001)  # Start the HTTP server for Prometheus metrics on port 8001
    consume_user_events()
