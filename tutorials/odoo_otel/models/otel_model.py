import logging
from odoo import models, fields
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
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
otlp_exporter = OTLPSpanExporter(endpoint="http://0.0.0.0:4317", insecure=True)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

# Configure OTLP Exporter for Metrics
metric_exporter = OTLPMetricExporter(endpoint="http://localhost:4317", insecure=True)
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

    otlp_endpoint = fields.Char(string="OTLP Endpoint", default="http://0.0.0.0:4317")

    def send_custom_trace(self):
        """ Sends a custom trace to OpenTelemetry for monitoring. """
        self.ensure_one()  # Ensure method works correctly on single records
        
        # Start a custom trace to monitor specific method activity
        with tracer.start_as_current_span("odoo_custom_trace") as span:
            logger.info("Odoo is sending a custom trace to OpenTelemetry")

            # Optionally add custom attributes to the trace
            span.set_attribute("custom.tag", "odoo_app")
            span.set_attribute("custom.operation", "send_custom_trace")

            request_counter.add(1, {"operation": "send_custom_trace"})
            with tracer.start_as_current_span("odoo_important_operation") as inner_span:
                logger.info("Performing important operation...")
                span.set_attribute("operation.type", "database_query")
                request_latency.record(0.2, {"operation": "database_query"})  # Simulated latency
    
    def record_http_request(self):
        """Increment the HTTP request counter each time a request is received."""
        request_counter.add(1, {
            "route": "/web",
            "method": "GET",
            "status_code": "200"
        })
        logging.info("Recorded an HTTP request metric in OpenTelemetry")