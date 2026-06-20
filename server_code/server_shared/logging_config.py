import anvil.email
# Mybizz CS — Logging Configuration
# Phase 0 Implementation — TODO 3

import structlog
import logging
import sys

def setup_logging(log_level=logging.INFO):
    """Configure structured logging for all server functions."""
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format='%(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

def get_logger(name=None):
    """Get structured logger."""
    return structlog.get_logger(name)

# Example usage in server functions:
# logger = get_logger()
# logger.info("function_entry", function="get_vault_secret", secret_name=name)
# logger.info("function_exit", function="get_vault_secret", result_type=type(result).__name__)
# logger.error("function_error", function="get_vault_secret", 
#              error_type=type(e).__name__, error_message=str(e))
