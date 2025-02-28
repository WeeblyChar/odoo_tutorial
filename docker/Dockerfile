# Use the official Odoo image as the base (can change depending on the Odoo version).
FROM odoo:latest

# Set as root to install dependencies.
USER root

# Install OpenTelemetry dependencies in a clean environment
RUN pip config set global.break-system-packages true && \
#                  ^ DEVELOPER ONLY (ONLY IF NEEDED). REMOVE IF NOT NEEDED
    pip install --no-cache-dir \
    prometheus_client \
#   ^ Custom prometheus exporter for Odoo
    opentelemetry-exporter-prometheus \
#   ^ Prometheus Exporter
    opentelemetry-instrumentation-psycopg2 \
#   ^ Query Logging
    opentelemetry-instrumentation-wsgi \
    opentelemetry-exporter-otlp-proto-http\ 
#   ^ HTTP
    opentelemetry-exporter-otlp \
#   ^ gRPC || OpenTelemetry Protocol -> Sends logs in an OpenTelemetry format
    opentelemetry-distro && \
#   ^ Contains opentelemetry api and sdk
    opentelemetry-bootstrap -a install && \
#   ^ unpack the distro package
    rm ~/.config/pip/pip.conf

# Installing curl, wget, ping and grep for docker container. REMOVE IF NOT NEEDED.
RUN apt-get update && apt-get install -y curl wget iputils-ping grep && rm -rf /var/lib/apt/lists/*


# Entrypoint
COPY entrypoint.py /opt/odoo/odoo-entrypoint.py
RUN chmod +x /opt/odoo/odoo-entrypoint.py

# Switch back to user
USER odoo