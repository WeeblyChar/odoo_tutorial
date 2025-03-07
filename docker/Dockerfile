# Use the official Odoo image as the base (can change depending on the Odoo version).
FROM odoo:latest

# Set as root to install dependencies.
USER root
# idk, add py3
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
USER odoo

ENV PATH="/var/lib/odoo/.local/bin:$PATH"

# Install OpenTelemetry dependencies in a clean environment
RUN pip config set global.break-system-packages true && \
    pip install --no-cache-dir \
    prometheus_client \
    opentelemetry-exporter-prometheus \
    opentelemetry-instrumentation-psycopg2 \
    opentelemetry-instrumentation-wsgi \
    opentelemetry-exporter-otlp-proto-http \
    opentelemetry-exporter-otlp \
    opentelemetry-distro && \
    opentelemetry-bootstrap -a install

USER root
# Installing curl, wget, ping and grep for docker container. REMOVE IF NOT NEEDED.
RUN apt-get update && apt-get install -y curl wget iputils-ping grep && rm -rf /var/lib/apt/lists/*
USER odoo

# Set OpenTelemetry environment variable
ENV OTEL_SERVICE_NAME=odoo \
    OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317 \
    OTEL_METRICS_EXPORTER=prometheus \
    OTEL_TRACES_EXPORTER=otlp \
    OTEL_LOGS_EXPORTER=otlp \
    OTEL_RESOURCE_ATTRIBUTES=service.name=odoo,service.version=18.0 \
    OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true \
    OTEL_PYTHON_LOG_LEVEL=INFO

USER root
# Entrypoint
COPY entrypoint.py /opt/odoo/odoo-entrypoint.py
RUN chmod +x /usr/bin/python3 /opt/odoo/odoo-entrypoint.py
USER odoo

# Switch back to user
# USER odoo

RUN which python3

# Run Odoo with OpenTelemetry Auto-Instrumentation
ENTRYPOINT ["opentelemetry-instrument", "--traces_exporter", "console", "--metrics_exporter", "none", "--", "/usr/bin/python3", "/opt/odoo/odoo-entrypoint.py"]
# ENTRYPOINT ["opentelemetry-instrument", "--traces_exporter", "otlp", "--metrics_exporter", "prometheus", "--logs_exporter", "otlp", "--", "/usr/bin/python3", "/opt/odoo/odoo-entrypoint.py"]

# ENTRYPOINT ["/usr/bin/python3", "/opt/odoo/odoo-entrypoint.py"]