# Use the official Odoo image as the base (can change depending on the Odoo version).
FROM odoo:latest

# Set as root to install dependencies.
USER root

# Install OpenTelemetry dependencies in a clean environment
RUN pip config set global.break-system-packages true && \
#                  ^ DEVELOPER ONLY (ONLY IF NEEDED). REMOVE IF NOT NEEDED
    pip install --no-cache-dir \
    opentelemetry-instrumentation-psycopg2 \
    opentelemetry-distro && \
    opentelemetry-bootstrap -a install && \
    rm ~/.config/pip/pip.conf

# Entrypoint
COPY entrypoint.py /opt/odoo/odoo-entrypoint.py
RUN chmod +x /opt/odoo/odoo-entrypoint.py

# Switch back to user
USER odoo