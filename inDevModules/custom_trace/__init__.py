from . import controllers, models

# Import OpenTelemetry Instrumentations
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor # <-- Database Intrumentator

# Apply instrumentation for PostgreSQL queries (psycopg2)
Psycopg2Instrumentor().instrument()