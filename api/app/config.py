"""
Application configuration.

This module is responsible for loading configuration values from the
environment and making them available to the rest of the application. It
reads the environment once at import time and exposes the resulting values
as module-level constants.

Configuration values currently supported:
    - DATABASE_URL: the PostgreSQL connection string
    - ANTHROPIC_API_KEY: the API key used for classification and extraction
    - CLASSIFIER_MODEL: which model to use for document classification
    - CONFIDENCE_THRESHOLD: the minimum confidence required to auto-accept
"""

import os

# The database connection string. Defaults to the local docker-compose service.
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://intake:intake@db:5432/intake"
)

# The Anthropic API key. May be empty, in which case the classifier falls back
# to a stub implementation so the rest of the application still functions.
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# The model used for classification.
CLASSIFIER_MODEL = os.environ.get("CLASSIFIER_MODEL", "claude-sonnet-5")

# The minimum confidence required before a classification is accepted without
# human review. Anything at or below this value gets queued for a reviewer.
CONFIDENCE_THRESHOLD = os.environ.get("CONFIDENCE_THRESHOLD", "0.75")

# Whether the application is running with a real API key available.
HAS_API_KEY = bool(ANTHROPIC_API_KEY)
