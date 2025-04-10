########### Tracing Dependencies ############
from odoo import http
from opentelemetry import trace
from opentelemetry.trace import SpanKind
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
import time
#############################################
#===========================================#
######## Logging Dependencies (Loki) ########
import logging
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
#############################################
#===========================================#
############ Metric Dependencies ############
from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
#############################################
#===========================================#
######## Initialize Instrumentation #########
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("✅   Initializing OpenTelemetry...")

# Set OpenTelemetry Tracer Provider
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Set Up OpenTelemetry Exporter
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Apply Instrumentations
RequestsInstrumentor().instrument()
Psycopg2Instrumentor().instrument()
LoggingInstrumentor().instrument(set_logging_format=True) 

logger.info("✅   OpenTelemetry Instrumentation Applied!")
#############################################
#===========================================#
##### OTel-Logger initialization #####
logger_provider = LoggerProvider(
    resource=Resource.create({
    "service.name": "odoo",
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
#############################################
#===========================================#
########## Prometheus Exporter ##############
from prometheus_client import CollectorRegistry, Counter, Gauge, generate_latest

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class PrometheusController(http.Controller):
    @http.route(["/metrics"], auth="public", type="http", methods=["GET"])
    def metrics(self):
        """
        Provide Prometheus metrics.
        """

        registry = CollectorRegistry()
        
        ############## Added Code ######################
        # Collect system metrics
        system_metrics = request.env["ir.metric"].get_system_metrics()
        cpu_gauge = Gauge("system_cpu_usage", "CPU usage percentage", registry=registry)
        cpu_gauge.set(system_metrics["cpu_usage_percentage"])

        memory_gauge = Gauge("system_memory_usage", "Memory usage percentage", registry=registry)
        memory_gauge.set(system_metrics["memory_usage_percentage"])

        disk_gauge = Gauge("system_disk_usage", "Disk usage percentage", registry=registry)
        disk_gauge.set(system_metrics["disk_usage_percentage"])
        
        memory_used_gauge = Gauge("system_memory_used_gb", "Memory used in GB", registry=registry)
        memory_used_gauge.set(system_metrics["memory_used_gb"])

        memory_total_gauge = Gauge("system_memory_total_gb", "Total system memory in GB", registry=registry)
        memory_total_gauge.set(system_metrics["memory_total_gb"])

        disk_used_gauge = Gauge("system_disk_used_gb", "Disk used in GB", registry=registry)
        disk_used_gauge.set(system_metrics["disk_used_gb"])

        disk_total_gauge = Gauge("system_disk_total_gb", "Total disk space in GB", registry=registry)
        disk_total_gauge.set(system_metrics["disk_total_gb"])
        
        # Collect Odoo-specific metrics
        online_users_gauge = Gauge("odoo_online_users", "Number of online users", registry=registry)
        online_users_gauge.set(request.env["ir.metric"].get_online_users())
        
        total_users_gauge = Gauge("odoo_total_users", "Number of total users", registry=registry)
        total_users_gauge.set(request.env["ir.metric"].get_total_users())
        
        response_time_gauge = Gauge("odoo_request_response_time", "Average request response time", registry=registry)
        response_time_gauge.set(request.env["ir.metric"].get_request_response_time())

        query_time_gauge = Gauge("odoo_query_execution_time", "Average query execution time", registry=registry)
        query_time_gauge.set(request.env["ir.metric"].get_query_execution_time())
        ################################################
        
        for metric in request.env["ir.metric"].sudo().search([]):
            if metric.metric_type == "gauge":
                g = Gauge(metric.name, metric.description, registry=registry)
                g.set(metric._get_value())
            if metric.metric_type == "counter":
                c = Counter(metric.name, metric.description, registry=registry)
                c.inc(metric._get_value())
        return generate_latest(registry)
#############################################
#===========================================#
################# Metrics ###################
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
#############################################
#===========================================#
################ Trace/Span #################
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
#############################################
#===========================================#
########### Metrics Controller ##############
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
#############################################
#===========================================#