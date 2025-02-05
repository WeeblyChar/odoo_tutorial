import logging
from odoo import models, fields
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# Set up OpenTelemetry Tracing Provider
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure OTLP Exporter
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

# Integrate OpenTelemetry with Python Logging, Requests, and Database
LoggingInstrumentor().instrument(set_logging_format=True)
RequestsInstrumentor().instrument()
Psycopg2Instrumentor().instrument()

logging.basicConfig(level=logging.DEBUG)

# Test log message (to verify it's working)
logger = logging.getLogger("odoo.otel")
logger.debug("OpenTelemetry logging is set up!")

# Odoo model with custom tracing
class OdooOtelSettings(models.Model):
    _name = "odoo.otel.settings"
    _description = "Odoo OpenTelemetry Settings"

    otlp_endpoint = fields.Char(string="OTLP Endpoint", default="http://localhost:4317")

    def send_custom_trace(self):
        # Start a custom trace to monitor specific method activity
        with tracer.start_as_current_span("odoo_custom_trace") as span:
            logger.info("Odoo is sending a custom trace to OpenTelemetry")

            # Optionally add custom attributes to the trace
            span.set_attribute("custom.tag", "odoo_app")
            span.set_attribute("custom.operation", "send_custom_trace")

            # Your custom method logic goes here
            self._perform_important_operation()

    def _perform_important_operation(self):
        # You can create nested spans here if needed
        with tracer.start_as_current_span("odoo_important_operation") as span:
            logger.info("Performing important operation...")
            # Add additional custom trace data here if necessary
            span.set_attribute("operation.type", "database_query")
            # Simulate the operation (e.g., database queries, complex logic, etc.)
