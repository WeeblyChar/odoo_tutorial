#### Tracing Dependencies #####
from odoo import http
from opentelemetry import trace
from opentelemetry.trace import SpanKind
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
import time
#####################################

#### Logging Dependencies (Loki) ####
import logging
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter,
)
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
######################################

#### Metric Dependencies #####
from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
######################################

##### OTel-Logger initialization #####
logger_provider = LoggerProvider(
    resource=Resource.create({
    "service.name": "odoo",
    # "severity.text": "level" # <-- No workie. Dunno why but it no workie like I wanted it to be.
    }),
)

# Set Resources
set_logger_provider(logger_provider)

# Set Exporter
log_exporter = OTLPLogExporter(endpoint="http://otel-collector:4317", insecure=True)

# Batch Log Record Processor
logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))

# Log Handlers
log_handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
logging.getLogger().setLevel(logging.INFO) # <-- logging.INFO = logs anything from INFO level and above
logging.getLogger().addHandler(log_handler)

logging.getLogger(__name__)
#####################################

metrics.set_meter_provider(MeterProvider(
    metric_readers=[PeriodicExportingMetricReader(OTLPMetricExporter(endpoint="http://otel-collector:4317", insecure=True))]  
))
meter = metrics.get_meter(__name__)

# Test Metric
startup_counter = meter.create_counter(
    name="odoo.startup.count",
    description="Counts how many times Odoo has started",
    unit="1"
)
startup_counter.add(1, {"service": "odoo"})

request_counter = meter.create_counter(
    "odoo.http.requests.total",
    description="Total number of HTTP requests handled by Odoo"
)

# Set up OpenTelemetry Tracer Provider
trace.set_tracer_provider(TracerProvider(resource=Resource.create({"service.name": "odoo"})))
tracer = trace.get_tracer(__name__)

# Configure OTLP Exporter to send traces to Tempo
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)

# Attach Exporter to OpenTelemetry SDK
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Print traces to console for debugging (this can be optional)
# trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))


class MetricsController(http.Controller):
    @http.route('/*', type='http', auth='public')
    def catch_all(self, **kwargs):
        # Start a span to trace this HTTP request
        with tracer.start_as_current_span("http_request", kind=SpanKind.SERVER) as span:
            start_time = time.time()  # Track request start time

            # Extract request method and path
            request_path = http.request.httprequest.path
            request_method = http.request.httprequest.method
            
            # Set attributes fpr trance span
            span.set_attribute("http.method", request_method)
            span.set_attribute("http.route", request_path)

            # Handle requests differently based on path
            if request_path.startswith("/api/"):  
                response = self.handle_api_request()
            elif request_path.startswith("/web/"):
                response = self.handle_web_request()
            elif request_path.startswith("/static/"):  
                response = "Static file request ignored"
            else:
                response = "Default request tracking"

            # Measure request duration
            end_time = time.time()
            duration = end_time - start_time

            # Attach duration to span
            span.set_attribute("http.request.duration", duration)
            span.add_event("Request completed", {"duration": duration})

            return response

    def handle_api_request(self):
        """Handles API requests separately."""
        return "API request handled"

    def handle_web_request(self):
        """Handles backend web requests separately."""
        return "Web request handled"
