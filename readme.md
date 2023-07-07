# Project Handover Documentation

## Overview
This document serves as a handover guide for the project. It provides an overview of the project's components, architecture, and instructions for setting up and running the project.

## Project Components
The project consists of the following components:

1. **Kafka**: A message broker system used for streaming data.
2. **Producer API**: A Flask application that receives metrics and workorders data via API endpoints and publishes the data to Kafka topics.
3. **Consumer**: A Python script that consumes data from Kafka topics, performs data transformations and correlations, and generates a report.

## Architecture
The project follows a streaming ETL (Extract, Transform, Load) pipeline architecture. The data flow is as follows:

1. Metrics and workorders data are sent to the Producer API via POST requests.
2. The Producer API publishes the data to Kafka topics: `metrics` and `workorders`.
3. The Consumer script subscribes to the Kafka topics and consumes the data.
4. The Consumer script performs data transformations, correlations, and generates a report.

## Setup Instructions

### Prerequisites
- Docker: Ensure that Docker is installed and running on the machine.
- Python 3.x: Install Python 3.x to run the Python scripts.

### Steps
1. Clone the project repository to your local machine.

2. Start the Kafka broker and create the necessary topics using the provided `docker-compose.yml` file:
$ docker-compose up -d
3. Install the Python dependencies:
  ```
  $ pip install -r requirements.txt
  ```

4. Start the Producer API by running the `main.py` script:
  ```
  $ python main.py
  ```
5. Use the API endpoints to send metrics and workorders data:
- Send metrics data:
  ```
  $ curl -X POST -H "Content-Type: application/json" -d '{"id": 10, "val": 553.1947969841733, "time": 1624378100}' http://localhost:5000/metrics
  ```

- Send workorders data:
  ```
  $ curl -X POST -H "Content-Type: application/json" -d '{"time": 1625748534, "product": 1, "production": 5470.282493383858}' http://localhost:5000/workorders
  ```

6. Run the Consumer script to consume data from Kafka, perform data transformations, correlations, and generate the report:
  ```
  $ python consumer.py
  ```


7. The generated report will be saved as `report.csv` in the project directory.




