# Use the official Odoo image as the base
FROM odoo:latest

USER root

# Install OpenTelemetry dependencies in a clean environment
RUN pip config set global.break-system-packages true && \
    pip install --no-cache-dir \
    opentelemetry-exporter-prometheus \
#   ^ Prometheus Exporter
    # opentelemetry-api \
    # opentelemetry-sdk \
#   ^ Already included in opentelemetry-distro
#   ^ sdk something, should be made by bootsrtap
    opentelemetry-instrumentation-psycopg2 \
    opentelemetry-instrumentation-wsgi \
    opentelemetry-exporter-otlp-proto-http\ 
#   ^ HTTP
    opentelemetry-exporter-otlp \
#   ^ gRPC || OpenTelemetry Protocol -> Sends logs in an OpenTelemetry format
    opentelemetry-distro && \
#   ^ Contains opentelemetry api and sdk
    opentelemetry-bootstrap -a install && \
    rm ~/.config/pip/pip.conf

RUN apt-get update && apt-get install -y curl wget iputils-ping grep && rm -rf /var/lib/apt/lists/*

#Entrypoint something
COPY entrypoint.py /opt/odoo/odoo-entrypoint.py
RUN chmod +x /opt/odoo/odoo-entrypoint.py

# Set environment variables for OpenTelemetry
# ENV OTEL_SERVICE_NAME=odoo
# ENV OTEL_TRACES_EXPORTER=console,otlp
# ENV OTEL_METRICS_EXPORTER=console,otlp
# ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
# ENV OTEL_EXPORTER_PROMETHEUS_HOST="otel-collector"
# ENV OTEL_EXPORTER_PROMETHEUS_PORT=4317

# Ensure OpenTelemetry CLI tool is accessible
# ENV PATH="/usr/local/bin:/root/.local/bin:$PATH"

# Check instrumentation package
# RUN ln -s /usr/local/bin/opentelemetry-instrument /usr/bin/opentelemetry-instrument || true

# Copy the modified Odoo startup script
# COPY odoo-bin /usr/bin/odoo-bin

# Ensure execution permission
# RUN chmod +x /usr/bin/odoo-bin

# Set the entrypoint
# ENTRYPOINT ["odoo-bin"]

USER odoo

