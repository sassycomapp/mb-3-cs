import anvil.email
# Mybizz CS — Metrics Configuration
# Phase 0 Implementation — TODO 3

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CollectorRegistry
import time

# Create registry
registry = CollectorRegistry()

# Bookings metrics
BOOKINGS_CREATED = Counter(
    'bookings_created_total',
    'Total number of bookings created',
    registry=registry
)

BOOKINGS_COMPLETED = Counter(
    'bookings_completed_total',
    'Total number of bookings completed',
    registry=registry
)

BOOKINGS_CANCELLED = Counter(
    'bookings_cancelled_total',
    'Total number of bookings cancelled',
    registry=registry
)

BOOKING_LATENCY = Histogram(
    'booking_creation_latency_ms',
    'Time from booking request to confirmation in milliseconds',
    buckets=[100, 250, 500, 1000, 2500, 5000],
    registry=registry
)

# Payment metrics
PAYMENTS_PROCESSED = Counter(
    'payments_processed_total',
    'Total number of payments processed',
    registry=registry
)

PAYMENTS_SUCCESSFUL = Counter(
    'payments_successful_total',
    'Total number of successful payments',
    registry=registry
)

PAYMENTS_FAILED = Counter(
    'payments_failed_total',
    'Total number of failed payments',
    registry=registry
)

PAYMENT_AMOUNT = Counter(
    'payment_amount_total',
    'Total payment amount in system currency',
    registry=registry
)

PAYMENT_LATENCY = Histogram(
    'payment_processing_latency_ms',
    'Payment processing latency in milliseconds',
    buckets=[100, 250, 500, 1000, 2500, 5000],
    registry=registry
)

# Email metrics
EMAILS_SENT = Counter(
    'emails_sent_total',
    'Total number of emails sent',
    registry=registry
)

EMAILS_DELIVERED = Counter(
    'emails_delivered_total',
    'Total number of emails delivered',
    registry=registry
)

EMAILS_FAILED = Counter(
    'emails_failed_total',
    'Total number of emails failed',
    registry=registry
)

# Error metrics
ERRORS_TOTAL = Counter(
    'errors_total',
    'Total number of errors',
    ['function', 'error_type'],
    registry=registry
)

# Request metrics
API_REQUESTS = Counter(
    'api_requests_total',
    'Total number of API requests',
    ['endpoint', 'method'],
    registry=registry
)

API_LATENCY = Histogram(
    'api_request_latency_ms',
    'API request latency in milliseconds',
    buckets=[50, 100, 250, 500, 1000, 2500, 5000],
    registry=registry
)

# Active users gauge
ACTIVE_USERS = Gauge(
    'active_users',
    'Number of active users (last 30 days)',
    registry=registry
)

# Revenue gauge
REVENUE_TOTAL = Gauge(
    'revenue_total',
    'Total revenue in system currency',
    registry=registry
)

def record_booking_created():
    """Record a booking creation."""
    BOOKINGS_CREATED.inc()

def record_booking_completed():
    """Record a booking completion."""
    BOOKINGS_COMPLETED.inc()

def record_booking_cancelled():
    """Record a booking cancellation."""
    BOOKINGS_CANCELLED.inc()

def record_booking_latency(latency_ms):
    """Record booking creation latency."""
    BOOKING_LATENCY.observe(latency_ms)

def record_payment_processed():
    """Record a payment processed."""
    PAYMENTS_PROCESSED.inc()

def record_payment_successful():
    """Record a successful payment."""
    PAYMENTS_SUCCESSFUL.inc()

def record_payment_failed():
    """Record a failed payment."""
    PAYMENTS_FAILED.inc()

def record_payment_amount(amount):
    """Record payment amount."""
    PAYMENT_AMOUNT.inc(amount)

def record_payment_latency(latency_ms):
    """Record payment processing latency."""
    PAYMENT_LATENCY.observe(latency_ms)

def record_email_sent():
    """Record an email sent."""
    EMAILS_SENT.inc()

def record_email_delivered():
    """Record an email delivered."""
    EMAILS_DELIVERED.inc()

def record_email_failed():
    """Record an email failed."""
    EMAILS_FAILED.inc()

def record_error(function, error_type):
    """Record an error."""
    ERRORS_TOTAL.labels(function=function, error_type=error_type).inc()

def record_api_request(endpoint, method):
    """Record an API request."""
    API_REQUESTS.labels(endpoint=endpoint, method=method).inc()

def record_api_latency(latency_ms):
    """Record API request latency."""
    API_LATENCY.observe(latency_ms)

def get_metrics():
    """Get Prometheus metrics in text format."""
    return generate_latest(registry)

def get_metrics_json():
    """Get metrics as JSON (simplified)."""
    import json
    # This is a simplified version - real implementation would parse the text format
    return {"status": "ok", "registry_size": len(registry._names_to_collectors)}
