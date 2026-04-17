"""
getmem-ai — Persistent memory API for AI agents.
Two API calls. Your agent remembers everything.

https://getmem.ai
"""

__version__ = "0.1.0"
__author__ = "getmem.ai"

from .client import GetMem
from .errors import (
    GetMemError, APIError, ConnectionError, TimeoutError,
    UnauthorizedError, QuotaExceededError, ForbiddenError,
    NotFoundError, ValidationError, RateLimitedError,
    InternalError, ServiceUnavailableError,
)

def init(api_key: str, base_url: str = "https://memory.getmem.ai", timeout: int = 30) -> GetMem:
    """
    Initialize the getmem client.

    Args:
        api_key: Your getmem API key (get one at https://platform.getmem.ai)
        base_url: API base URL (default: https://memory.getmem.ai)
        timeout: Request timeout in seconds (default: 30)

    Returns:
        GetMem client instance

    Example:
        import getmem_ai as getmem
        mem = getmem.init("gm_live_...")
        context = mem.get("user_123", query="What do I like?")
    """
    return GetMem(api_key=api_key, base_url=base_url, timeout=timeout)


__all__ = [
    "init", "GetMem",
    "GetMemError", "APIError", "ConnectionError", "TimeoutError",
    "UnauthorizedError", "QuotaExceededError", "ForbiddenError",
    "NotFoundError", "ValidationError", "RateLimitedError",
    "InternalError", "ServiceUnavailableError",
]
