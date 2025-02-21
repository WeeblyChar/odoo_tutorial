#!/usr/bin/env python3
# import logging

import os
os.environ["PYTHONPATH"] = "/usr/local/lib/python3.12/dist-packages"
# ^-- Apparently this is a must only for my container due to the Open Telemetry's library being in a weird directory

# Ensure logs are visible
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# logger.info("Initializing Odoo with OpenTelemetry...")

# Set up OpenTelemetry auto-instrumentation
"""
from opentelemetry.instrumentation.auto_instrumentation import sitecustomize  # Enables auto instrumentation
^ might be the reason why it kept repeating itself
"""

# #### Metric Dependencies #####
# from opentelemetry import metrics
# from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
# from opentelemetry.sdk.metrics import MeterProvider
# from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
# ###############################

#### Tracing Dependencies #####
# from opentelemetry import trace
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor
###############################

# #### Logging Dependencies (Loki) ####
# from opentelemetry._logs import set_logger_provider
# from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
#     OTLPLogExporter,
# )
# from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
# from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
# #####################################

#### General Dependencies ####
# from opentelemetry.sdk.resources import Resource
# from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
# from opentelemetry.instrumentation.requests import RequestsInstrumentor
##############################

### Configure General Settings for OpenTelemetry ###
# general_resource = Resource.create(
#     {"service.name": "odoo"}
# )

# ### OTel-Logger initialization ###
# logger_provider = LoggerProvider(
#     resource=Resource.create(
#     {"service.name": "odoo"}
# ),
# )
# set_logger_provider(logger_provider)
# log_exporter = OTLPLogExporter(endpoint="http://otel-collector:4317", insecure=True)
# logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
# log_handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
# logging.getLogger().addHandler(log_handler)
# #################################


# Configure Tracing
# trace.set_tracer_provider(TracerProvider(resource=Resource.create({"service.name": "odoo"})))
# tracer = trace.get_tracer(__name__)

# otlp_trace_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
# trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_trace_exporter))

# Configure Metrics
# metrics.set_meter_provider(MeterProvider(
#     metric_readers=[PeriodicExportingMetricReader(OTLPMetricExporter(endpoint="http://otel-collector:4317", insecure=True))]  
# ))
# meter = metrics.get_meter(__name__)

# # Test Metric
# startup_counter = meter.create_counter(
#     name="odoo.startup.count",
#     description="Counts how many times Odoo has started",
#     unit="1"
# )
# startup_counter.add(1, {"service": "odoo"})

# Automatically instrument PostgreSQL queries
# Psycopg2Instrumentor().instrument()
# Automatically instrument HTTP Requests
# RequestsInstrumentor().instrument()

# logger.info("OpenTelemetry Tracing & Metrics are enabled for Odoo!")

# request_counter = meter.create_counter(
#     "odoo.http.requests.total",
#     description="Total number of HTTP requests handled by Odoo"
# )

import odoo
# from odoo import http

# class MetricsController(http.Controller):
#     @http.route('/metrics', type='http', auth='public')
#     def metrics(self):
#         request_counter.add(1, {"service": "odoo"})
#         return "Metrics tracked!"

import sys

# Start Odoo
if __name__ == "__main__":
    sys.argv.extend(["-i", "base"])  # Ensure base module installation
    odoo.cli.main()
