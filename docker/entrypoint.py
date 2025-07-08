import sys
import odoo

# import logging
# from opentelemetry import trace
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
# from opentelemetry.instrumentation.requests import RequestsInstrumentor
# from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
# from opentelemetry.instrumentation.logging import LoggingInstrumentor

# # Logging Setup
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# logger.info("✅   Initializing OpenTelemetry...")

# # Set OpenTelemetry Tracer Provider
# trace.set_tracer_provider(TracerProvider())
# tracer = trace.get_tracer(__name__)

# # Set Up OpenTelemetry Exporter
# otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
# span_processor = BatchSpanProcessor(otlp_exporter)
# trace.get_tracer_provider().add_span_processor(span_processor)

# # Apply Instrumentations
# RequestsInstrumentor().instrument()
# Psycopg2Instrumentor().instrument()
# LoggingInstrumentor().instrument(set_logging_format=True) 

# logger.info("✅   OpenTelemetry Instrumentation Applied!")

import os
os.environ["PYTHONPATH"] = "/usr/local/lib/python3.12/dist-packages"

if __name__ == "__main__":
    sys.argv.extend(["-i", "base"])  # Ensure base module installation
    odoo.cli.main()