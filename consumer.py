from json import loads
from kafka import KafkaConsumer
import numpy as np
import pandas as pd

TOPIC_METRICS = 'metrics'
TOPIC_WORKORDERS = 'workorders'

REPORT_OUTPUT = []
METRICS_DATA = []
WORKORDER_DATA = []


def find_top_correlated_params(metrics_data, workorders_data, product_id):
    product_metrics = [metrics for metrics in metrics_data if metrics['id'] == product_id]

    param_values = np.array([metrics['val'] for metrics in product_metrics])
    production_values = np.array([workorder['production'] for workorder in workorders_data])

    min_len = min(len(param_values), len(production_values))
    param_values = param_values[:min_len]
    production_values = production_values[:min_len]

    correlations = np.corrcoef(param_values, production_values)[0, 1:]
    sorted_indices = np.argsort(correlations)[::-1]
    top_correlated_params = param_values[sorted_indices][:3]

    return top_correlated_params


def generate_report():
    metrics_data = METRICS_DATA
    workorders_data = WORKORDER_DATA

    # Perform necessary data transformations and correlations
    report_data = []
    processed_ids = set()

    for workorder in workorders_data:
        product_id = workorder['product']
        if product_id not in processed_ids:
            top_correlated_params = find_top_correlated_params(metrics_data, workorders_data, product_id)
            report_data.append({'Product ID': product_id, 'Top Correlated Params': top_correlated_params})
            processed_ids.add(product_id)

    if report_data:
        df_report = pd.DataFrame(report_data)
        df_report.to_csv('report.csv', index=False)
        print('Report generated successfully.')


def consume_data():
    consumer = KafkaConsumer(bootstrap_servers='localhost:9094',
                             auto_offset_reset='earliest',
                             group_id='my_group',
                             enable_auto_commit=True,
                             value_deserializer=lambda x: loads(x.decode('utf-8')))

    consumer.subscribe([TOPIC_METRICS, TOPIC_WORKORDERS])

    while True:
        raw_messages = consumer.poll(timeout_ms=100, max_records=20000)
        try:
            for topic_partition, messages in raw_messages.items():
                if topic_partition.topic == 'metrics':
                    for message in messages:
                        METRICS_DATA.extend(message.value)

                if topic_partition.topic == 'workorders':
                    for message in messages:
                        WORKORDER_DATA.extend(message.value)
        except UnboundLocalError:
            pass

        generate_report()


if __name__ == '__main__':
    consume_data()
