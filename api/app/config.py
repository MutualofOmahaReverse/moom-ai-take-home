"""
Application configuration.

Values are read from the environment once at import time and exposed as
module-level constants.
"""

import os

# The database connection string. Defaults to the docker-compose service.
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://intake:intake@db:5432/intake"
)

# Live model calls are OPT-IN. With no key set, classification and extraction
# run offline -- see app/services/offline.py. That is the default everywhere,
# including local development, and nothing in this repo requires a key.
#
# Set ANTHROPIC_API_KEY if you specifically want to exercise the live path.
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
USE_LIVE_MODEL = bool(ANTHROPIC_API_KEY)

# Which model to use when the live path is enabled.
CLASSIFIER_MODEL = os.environ.get("CLASSIFIER_MODEL", "claude-sonnet-5")

# The minimum confidence required before a classification is accepted without
# human review. Anything at or below this value gets queued for a reviewer.
CONFIDENCE_THRESHOLD = os.environ.get("CONFIDENCE_THRESHOLD", "0.75")
