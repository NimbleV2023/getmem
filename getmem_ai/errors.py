"""
getmem.ai SDK error hierarchy — matches API error catalog v2.0
"""


class GetMemError(Exception):
    """Base exception for all getmem errors."""
    pass


class APIError(GetMemError):
    """HTTP error from the getmem API."""
    def __init__(self, message: str, error_code: str = "", details: dict = None,
                 request_id: str = "", status_code: int = 0):
        super().__init__(message)
        self.error_code = error_code
        self.details = details or {}
        self.request_id = request_id
        self.status_code = status_code

    def __repr__(self):
        return (f"{self.__class__.__name__}(status={self.status_code}, "
                f"error={self.error_code!r}, message={str(self)!r}, "
                f"request_id={self.request_id!r})")


class UnauthorizedError(APIError):
    """401 — API key missing, malformed, unknown, or deactivated. Do not retry."""
    pass


class QuotaExceededError(APIError):
    """402 — Monthly quota exhausted. Do not retry; check reset_at."""
    @property
    def current(self) -> int:
        return self.details.get("current", 0)

    @property
    def limit(self) -> int:
        return self.details.get("limit", 0)

    @property
    def reset_at(self) -> str:
        return self.details.get("reset_at", "")


class ForbiddenError(APIError):
    """403 — API key lacks required scope. Do not retry."""
    @property
    def required_scope(self) -> str:
        return self.details.get("required_scope", "")

    @property
    def available_scopes(self) -> list:
        return self.details.get("available_scopes", [])


class NotFoundError(APIError):
    """404 — Resource not found. Do not retry."""
    pass


class ValidationError(APIError):
    """422 — Request body failed validation. Do not retry."""
    @property
    def field_errors(self) -> list:
        return self.details.get("field_errors", [])


class RateLimitedError(APIError):
    """429 — Too many requests. Retryable — sleep retry_after seconds."""
    @property
    def retry_after(self) -> float:
        return self.details.get("retry_after", 60.0)

    @property
    def current(self) -> int:
        return self.details.get("current", 0)

    @property
    def limit(self) -> int:
        return self.details.get("limit", 0)


class InternalError(APIError):
    """500 — Unexpected server error. Retryable with exponential backoff."""
    pass


class ServiceUnavailableError(APIError):
    """503 — Backend dependency unavailable. Retryable with exponential backoff."""
    pass


class ConnectionError(GetMemError):
    """Network-level failure before HTTP response was received."""
    pass


class TimeoutError(GetMemError):
    """Request timed out."""
    pass


# Map HTTP status codes to exception classes
_STATUS_MAP = {
    401: UnauthorizedError,
    402: QuotaExceededError,
    403: ForbiddenError,
    404: NotFoundError,
    422: ValidationError,
    429: RateLimitedError,
    500: InternalError,
    503: ServiceUnavailableError,
}


def _raise_for_response(status_code: int, body: dict) -> None:
    """Parse an API error response and raise the appropriate exception."""
    exc_class = _STATUS_MAP.get(status_code, APIError)

    if status_code == 422:
        # FastAPI validation format: {"detail": [...]}
        field_errors = body.get("detail", [])
        message = "; ".join(
            f"{'.'.join(str(x) for x in e.get('loc', []))}: {e.get('msg', '')}"
            for e in field_errors
        ) or "Validation error"
        raise exc_class(
            message=message,
            error_code="validation_error",
            details={"field_errors": field_errors},
            request_id=body.get("request_id", ""),
            status_code=status_code,
        )

    raise exc_class(
        message=body.get("message", f"HTTP {status_code}"),
        error_code=body.get("error", ""),
        details=body.get("details", {}),
        request_id=body.get("request_id", ""),
        status_code=status_code,
    )
