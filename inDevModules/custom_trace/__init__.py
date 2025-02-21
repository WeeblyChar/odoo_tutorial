from . import controllers

# Import OpenTelemetry Instrumentations
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor

# Apply instrumentation for HTTP requests
RequestsInstrumentor().instrument()

# Apply instrumentation for PostgreSQL queries (psycopg2)
Psycopg2Instrumentor().instrument()