# Use the official Odoo image as the base
FROM odoo:18

# Switch to root user to install packages
USER root

# Install OpenTelemetry dependencies
RUN pip install --break-system-packages \
    opentelemetry-api \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp \
    opentelemetry-instrumentation \
    opentelemetry-instrumentation-logging \
    opentelemetry-instrumentation-requests \
    opentelemetry-instrumentation-sqlalchemy \
    opentelemetry-instrumentation-psycopg2

# Switch back to Odoo user for security
USER odoo
