from flask import Flask, request
from kafka import KafkaProducer
import json

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='localhost:9094')
TOPIC_METRICS = 'metrics'
TOPIC_WORKORDERS = 'workorders'


@app.route('/metrics', methods=['POST'])
def metrics():
    data = request.get_json()
    print(data)
    producer.send(TOPIC_METRICS, json.dumps(data).encode('utf-8'))
    return 'Metrics data published to Kafka'


@app.route('/workorders', methods=['POST'])
def workorders():
    data = request.get_json()
    print(data)
    producer.send(TOPIC_WORKORDERS, json.dumps(data).encode('utf-8'))
    return 'Workorder data published to Kafka'


if __name__ == '__main__':
    app.run(debug=True)
