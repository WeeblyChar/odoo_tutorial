import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor

# Set up OpenTelemetry Tracing Provider
trace.set_tracer_provider(TracerProvider())

# Configure OTLP Exporter
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))
##trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(otlp_exporter)) <-- Not good for high performance systems.

# Integrate OpenTelemetry with Python Logging
LoggingInstrumentor().instrument(set_logging_format=True)
RequestsInstrumentor().instrument()
Psycopg2Instrumentor().instrument()
logging.basicConfig(level=logging.DEBUG)

# Test log message (to verify it's working)
logger = logging.getLogger("odoo.otel")
logger.debug("OpenTelemetry logging is set up!")
