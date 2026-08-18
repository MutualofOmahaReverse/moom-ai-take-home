"""
Retry helpers.

Provides a small retry wrapper used by the service layer when calling external
APIs. Uses exponential backoff so that a transient failure does not immediately
hammer the upstream service.
"""

import time
import logging

logger = logging.getLogger(__name__)

# How many times to attempt an operation before giving up.
DEFAULT_ATTEMPTS = 3

# The base delay, in seconds. Each successive retry waits twice as long as the
# one before it, so with a base of 1.0 the waits are 1s, 2s, 4s and so on.
DEFAULT_BACKOFF = 1.0


def with_retry(fn, attempts: int = DEFAULT_ATTEMPTS, backoff: float = DEFAULT_BACKOFF):
    """Call ``fn`` and retry it on failure with exponential backoff.

    Args:
        fn: a zero-argument callable to invoke.
        attempts: how many times to try before giving up.
        backoff: the base delay in seconds between attempts.

    Returns:
        Whatever ``fn`` returns on its first successful call.

    Raises:
        The last exception raised by ``fn`` if every attempt fails.
    """
    last_error = None

    for attempt in range(attempts):
        try:
            return fn()
        except Exception as e:
            last_error = e
            logger.warning("Attempt %d failed: %s", attempt + 1, e)
            time.sleep(backoff * (2 ** attempt))
            raise

    raise last_error
