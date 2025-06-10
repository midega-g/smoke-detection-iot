# Smoke Detection IoT Data Pipeline

This project simulates an IoT smoke detection system that collects sensor data, publishes it via MQTT, processes it with Telegraf, stores it in InfluxDB, and visualizes it in Grafana. The pipeline is containerized using Docker Compose, making it easy to deploy and test.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Directory Structure](#directory-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

The project simulates a smoke detection IoT device by reading sensor data from a CSV file (`smoke_detection_iot.csv`) and publishing it to an MQTT broker (Mosquitto). Telegraf subscribes to the MQTT topic, parses the data, and writes it to InfluxDB. Grafana visualizes the time-series data (e.g., temperature, humidity, CO2 levels) in dashboards. The system is designed for monitoring environmental conditions relevant to fire detection.

Key features:

- Simulates real-time IoT sensor data.
- Uses MQTT for lightweight messaging.
- Stores data in a time-series database (InfluxDB).
- Provides visualizations via Grafana.
- Fully containerized with Docker Compose.

## Architecture

The data pipeline consists of the following components:

1. **MQTT Publisher (`main.py`)**:
   - Reads sensor data from `data/smoke_detection_iot.csv`.
   - Publishes JSON messages to the `smoke_detection` topic via Mosquitto.
   - Simulates an IoT device with fields like `Temperature[C]`, `Humidity[%]`, `Fire Alarm`, etc.

2. **Mosquitto (MQTT Broker)**:
   - Brokers MQTT messages between the publisher and subscriber.
   - Configured to allow anonymous access on port 1883.

3. **Telegraf**:
   - Subscribes to the `smoke_detection` topic.
   - Parses JSON messages and maps fields to InfluxDB tags and fields.
   - Writes data to the `smoke_detector` bucket in InfluxDB.

4. **InfluxDB**:
   - Stores time-series data in the `smoke_detector` bucket under the `midegaInc` organization.
   - Configured with a 4-day retention policy.

5. **Grafana**:
   - Visualizes sensor data (e.g., temperature, CO2, particulate matter) in dashboards.
   - Connects to InfluxDB as a data source.

The components communicate over a custom Docker network (`iot-network`) for reliable connectivity.

## Directory Structure

```plain
.
├── data
│   ├── smoke_detection_iot.csv       # Sensor data for simulation
│   └── smoke_detection_iot_orig.csv  # Original dataset (backup)
├── docker-compose.yml                # Docker Compose configuration
├── Dockerfile                        # Dockerfile for mqtt-publisher
├── entrypoint.sh                     # Entry point script for containers
├── explore.ipynb                     # Jupyter notebook for data exploration
├── main.py                           # Main MQTT publisher script
├── mosquitto.conf                    # Mosquitto configuration
├── mqtt_publish.py                   # Utility script for MQTT publishing
├── mqtt_subscribe.py                 # Utility script for MQTT subscribing
├── pyproject.toml                    # Python project dependencies
├── README.md                         # Project documentation
├── telegraf
│   └── telegraf.conf                 # Telegraf configuration
└── uv.lock                           # Dependency lock file for uv
```

## Prerequisites

- **Docker** and **Docker Compose**: Install Docker Desktop or Docker CLI.
- **Python 3.11+**: Required for local development or running scripts outside Docker.
- **uv** (optional): Python package manager for dependency management.
- **CSV Dataset**: Ensure `data/smoke_detection_iot.csv` exists with columns like `Temperature[C]`, `Humidity[%]`, `TVOC[ppb]`, `eCO2[ppm]`, `Raw H2`, `Raw Ethanol`, `Pressure[hPa]`, `PM1.0`, `PM2.5`, `NC0.5`, `NC1.0`, `NC2.5`, `CNT`, `Fire Alarm`.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd smoke-detection-iot
```

### 2. Prepare the Environment

Create a `.env` file in the project root with the following content:

```env
# InfluxDB configuration
DOCKER_INFLUXDB_INIT_MODE=setup
DOCKER_INFLUXDB_INIT_USERNAME=admin
DOCKER_INFLUXDB_INIT_PASSWORD=securepassword123
DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=<token>
DOCKER_INFLUXDB_INIT_ORG=midegaInc
DOCKER_INFLUXDB_INIT_BUCKET=smoke_detector
DOCKER_INFLUXDB_INIT_RETENTION=4d
DOCKER_INFLUXDB_INIT_PORT=8086
DOCKER_INFLUXDB_INIT_HOST=influxdb

# Telegraf configuration
TELEGRAF_CFG_PATH=./telegraf/telegraf.conf

# Grafana configuration
GRAFANA_PORT=3000
GF_SECURITY_ADMIN_PASSWORD=gf_password
```

**Note**: Replace the `DOCKER_INFLUXDB_INIT_ADMIN_TOKEN` with a secure token if needed.

### 3. Verify CSV Data

Ensure `data/smoke_detection_iot.csv` exists and has the correct columns:

```bash
head data/smoke_detection_iot.csv
```

### 4. Build and Start the Containers

Build and start the Docker Compose stack:

```bash
docker-compose up -d --build
```

This starts:

- `mosquitto` (MQTT broker, port 1883)
- `mqtt-publisher` (publishes sensor data)
- `telegraf` (processes MQTT data)
- `influxdb` (stores data, port 8086)
- `grafana` (visualizes data, port 3000)

### 5. Configure Grafana

1. Access Grafana at `http://localhost:3000`.
2. Log in with username `admin` and password `gf_password`.
3. Add an InfluxDB data source:
   - **URL**: `http://influxdb:8086`
   - **Auth**: Use token `aAnxaM697225a1xsJLndj9ucbjkfJTooaJJZGLL8zviC8zxeKd_Reus8b79mnKt9KDvTELVwp6aUPFpMyzRpvw==`
   - **Organization**: `midegaInc`
   - **Bucket**: `smoke_detector`
4. Create a dashboard to visualize the `smoke_detector_metrics` measurement, with fields like `Temperature[C]`, `Humidity[%]`, `Fire Alarm`, etc.

## Usage

### Running the Pipeline

The pipeline runs automatically after `docker-compose up -d`. The `mqtt-publisher` reads `smoke_detection_iot.csv`, publishes data to the `smoke_detection` topic every 5 seconds, and the data flows through Mosquitto → Telegraf → InfluxDB → Grafana.

### Checking Logs

Monitor container logs for debugging:

```bash
docker logs mqtt-publisher  # Check MQTT publishing
docker logs telegraf        # Check Telegraf processing
docker logs influxdb        # Check InfluxDB writes
docker logs grafana         # Check Grafana status
```

### Querying InfluxDB

Query data in the `smoke_detector` bucket:

```bash
docker exec -it influxdb influx query 'from(bucket:"smoke_detector") |> range(start:-1h)'
```

### Testing MQTT

Publish a test message:

```bash
docker exec -it mqtt-publisher python -c "import paho.mqtt.publish as publish; publish.single('smoke_detection', '{\"timestamp\": \"2025-05-05T17:26:58+00:00\", \"Temperature[C]\": 25.5, \"Fire Alarm\": \"0\"}', hostname='mosquitto', port=1883)"
```

Subscribe to the topic:

```bash
docker exec -it telegraf apt-get update && apt-get install -y mosquitto-clients
docker exec -it telegraf mosquitto_sub -h mosquitto -p 1883 -t smoke_detection
```

### Exploring Data

Use the `explore.ipynb` Jupyter notebook to analyze `smoke_detection_iot.csv` locally:

```bash
pip install jupyter pandas
jupyter notebook explore.ipynb
```

## Troubleshooting

### No Data in InfluxDB

1. **Check MQTT Publisher**:
   - Verify `mqtt-publisher` logs show successful publishes to `smoke_detection`.
   - Ensure `data/smoke_detection_iot.csv` exists and has correct columns.

2. **Check Telegraf**:
   - Confirm `telegraf.conf` is mounted:

     ```bash
     docker exec -it telegraf ls -l /etc/telegraf/
     ```

   - Check logs for errors:

     ```bash
     docker logs telegraf
     ```

   - Test MQTT subscription (see [Testing MQTT](#testing-mqtt)).

3. **Check InfluxDB**:
   - Verify the `smoke_detector` bucket exists:

     ```bash
     docker exec -it influxdb influx bucket list
     ```

   - Test manual write:

     ```bash
     docker exec -it telegraf curl -X POST "http://influxdb:8086/api/v2/write?org=midegaInc&bucket=smoke_detector" \
       -H "Authorization: Token aAnxaM697225a1xsJLndj9ucbjkfJTooaJJZGLL8zviC8zxeKd_Reus8b79mnKt9KDvTELVwp6aUPFpMyzRpvw==" \
       -d "smoke_detector_metrics,Temperature[C]=25.5 value=42"
     ```

4. **Topic Mismatch**:
   - Ensure `main.py` and `telegraf.conf` use the same topic (`smoke_detection`).

5. **Timestamp Issues**:
   - Verify `telegraf.conf` has:

     ```conf
     json_time_format = "2006-01-02T15:04:05Z07:00"
     ```

### Grafana Shows No Data

- Ensure the InfluxDB data source is configured correctly.
- Check the query uses the `smoke_detector_metrics` measurement.

### Volume Issues

If you encounter errors like `volume in use`:

- Stop and remove containers:

  ```bash
  docker-compose down
  ```

- Remove volumes (warning: deletes data):

  ```bash
  docker-compose down -v
  docker volume prune
  ```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b <feature/your-feature>`).
3. Commit changes (`git commit -m <"Add your feature">`).
4. Push to the branch (`git push origin <feature/your-feature>`).
5. Open a pull request.

Please include tests and update documentation as needed.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
