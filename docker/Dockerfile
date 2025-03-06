# Use the official Odoo image as the base (can change depending on the Odoo version).
FROM odoo:latest

# Set as root to install dependencies.
USER root

# Install OpenTelemetry dependencies in a clean environment
RUN pip config set global.break-system-packages true && \
    prometheus_client \
    opentelemetry-exporter-prometheus \
    opentelemetry-instrumentation-psycopg2 \
    opentelemetry-instrumentation-wsgi \
    opentelemetry-exporter-otlp-proto-http \
    opentelemetry-exporter-otlp \
    opentelemetry-distro && \
    opentelemetry-bootstrap -a install

# Installing curl, wget, ping and grep for docker container. REMOVE IF NOT NEEDED.
RUN apt-get update && apt-get install -y curl wget iputils-ping grep && rm -rf /var/lib/apt/lists/*

# Set OpenTelemetry environment variables
ENV OTEL_SERVICE_NAME=odoo \
    OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317 \
    OTEL_METRICS_EXPORTER=prometheus \
    OTEL_TRACES_EXPORTER=otlp \
    OTEL_LOGS_EXPORTER=otlp \
    OTEL_RESOURCE_ATTRIBUTES=service.name=odoo,service.version=18.0 \
    OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true \
    OTEL_PYTHON_LOG_LEVEL=INFO

# Entrypoint
COPY entrypoint.py /opt/odoo/odoo-entrypoint.py
RUN chmod +x /opt/odoo/odoo-entrypoint.py

# Switch back to user
USER odoo