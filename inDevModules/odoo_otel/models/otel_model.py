import logging
from odoo import models, fields
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# Set up OpenTelemetry Tracing Provider
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure OTLP Exporter
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

# Configure OTLP Exporter for Metrics
metric_exporter = OTLPMetricExporter(endpoint="http://otel-collector:4317", insecure=True)
metric_reader = PeriodicExportingMetricReader(metric_exporter)
meter_provider = MeterProvider(metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter("odoo-metrics")

# Define Metrics
request_counter = meter.create_counter(
    name="odoo_requests_total",
    description="Total number of Odoo requests processed",
    unit="1"
)
request_latency = meter.create_histogram(
    name="odoo_request_latency_seconds",
    description="Latency of Odoo requests in seconds",
    unit="seconds"
)

# Integrate OpenTelemetry with Python Logging, Requests, and Database
LoggingInstrumentor().instrument(set_logging_format=True)
RequestsInstrumentor().instrument()
Psycopg2Instrumentor().instrument()

# Test log message (to verify it's working)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("odoo.otel")
logger.debug("OpenTelemetry logging is set up!")

# Odoo model with custom tracing
class OdooOtelSettings(models.Model):
    _name = "odoo.otel.settings"
    _description = "Odoo OpenTelemetry Settings"

    otlp_endpoint = fields.Char(string="OTLP Endpoint", default="http://otel-collector:4317")

    def send_custom_trace(self):
        self.ensure_one()
        try:
            with tracer.start_as_current_span("odoo_custom_trace") as span:
                # Add trace attributes for observability
                span.set_attribute("record_id", self.id)
                span.set_attribute("record_name", self.display_name)
                
                # Commit the transaction to persist changes
                self.env.cr.commit()
                
                # Use the `_sendone` method to send a message
                db_name = self.env.cr.dbname  # Get the database name
                channel = f"{db_name}:odoo_otel_trace"  # Define the channel
                message = {"info": "Trace sent successfully!", "record_id": self.id}  # Define the message
                
                self.env["bus.bus"]._sendone(channel, message, "Log somehow sent")  # Send the notification
                
                # Log success
                self._log_trace_info()
        except Exception as e:
            logger.error(f"Failed to send custom trace for record ID {self.id}: {e}")
            raise

    def _log_trace_info(self):
        logger.info("Custom trace executed successfully.")