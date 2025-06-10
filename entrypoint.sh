#!/bin/bash

# Protects script from continuing with an error
set -eu -o pipefail

echo "Starting InfluxDB setup script..."

# Ensures environment variables are set
# export DOCKER_INFLUXDB_INIT_MODE=$INFLUXDB_MODE
# export DOCKER_INFLUXDB_INIT_USERNAME=$INFLUXDB_USERNAME
# export DOCKER_INFLUXDB_INIT_PASSWORD=$INFLUXDB_PASSWORD
# export DOCKER_INFLUXDB_INIT_ORG=$INFLUXDB_ORG
# export DOCKER_INFLUXDB_INIT_BUCKET=$INFLUXDB_BUCKET
# export DOCKER_INFLUXDB_INIT_RETENTION=$INFLUXDB_RETENTION
# export DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=$INFLUXDB_TOKEN
# export DOCKER_INFLUXDB_INIT_PORT=$INFLUXDB_PORT
# export DOCKER_INFLUXDB_INIT_HOST=$INFLUXDB_HOST

# Conducts initial InfluxDB using the CLI
echo "Running influx setup..."
influx setup \
    --skip-verify \
    --bucket "${INFLUXDB_BUCKET}" \
    --retention "${INFLUXDB_RETENTION}" \
    --token "${INFLUXDB_TOKEN}" \
    --org "${INFLUXDB_ORG}" \
    --username "${INFLUXDB_USERNAME}" \
    --password "${INFLUXDB_PASSWORD}" \
    --host "${INFLUXDB_URL}" \
    --force || {
        echo "InfluxDB setup failed"
        exit 1
    }

echo "InfluxDB setup completed successfully"

