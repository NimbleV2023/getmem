"""
getmem.ai Python SDK — client with retry logic and structured error handling
"""

import json
import time
import urllib.request
import urllib.error
from typing import List, Optional, Dict, Any

from .errors import (
    GetMemError, ConnectionError, TimeoutError,
    RateLimitedError, InternalError, ServiceUnavailableError,
    _raise_for_response,
)

DEFAULT_BASE_URL = "https://memory.getmem.ai"
_RETRYABLE = (RateLimitedError, InternalError, ServiceUnavailableError)


class GetMem:
    """
    getmem.ai persistent memory client.

    Usage:
        import getmem_ai as getmem

        mem = getmem.init("gm_live_...")

        # Get memory context before each LLM call
        result = mem.get("user_123", query=user_message)
        context = result["context"]  # inject into system prompt

        # Save conversation after each turn
        mem.ingest("user_123", messages=[
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": reply},
        ])
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = 30,
        max_retries: int = 3,
    ):
        if not api_key:
            raise ValueError("getmem: api_key is required")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries

    # ── Core methods ──────────────────────────────────────────────────────────

    def get(self, user_id: str, query: str) -> Dict[str, Any]:
        """
        Retrieve relevant memory context for a query.

        Returns a dict with:
          - context (str): ready-to-use string for LLM system prompt
          - memories (list): individual memory items with relevance scores
          - meta (dict): timing and search metadata

        Args:
            user_id: Unique identifier for the user
            query: The current user message or topic to retrieve context for

        Example:
            result = mem.get("user_123", query="What do I prefer for breakfast?")
            system_prompt = f"You are a helpful assistant.\\n\\n{result['context']}"
        """
        return self._post("/v1/memory/get", {"user_id": user_id, "query": query})

    def ingest(
        self,
        user_id: str,
        messages: List[Dict[str, str]],
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Ingest conversation messages into memory.

        Extraction runs asynchronously — returns immediately.

        Args:
            user_id: Unique identifier for the user
            messages: List of message dicts with 'role' and 'content' keys
            session_id: Optional session identifier for grouping messages

        Example:
            mem.ingest("user_123", messages=[
                {"role": "user", "content": "I love hiking"},
                {"role": "assistant", "content": "That sounds great!"},
            ])
        """
        body: Dict[str, Any] = {"user_id": user_id, "messages": messages}
        if session_id is not None:
            body["session_id"] = session_id
        return self._post("/v1/memory/ingest", body)

    def ingest_conversation(
        self,
        user_id: str,
        user_message: str,
        assistant_message: str,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Convenience method: ingest a single user + assistant exchange.

        Example:
            mem.ingest_conversation("user_123", user_msg, reply)
        """
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()
        return self.ingest(
            user_id=user_id,
            messages=[
                {"role": "user", "content": user_message, "timestamp": now},
                {"role": "assistant", "content": assistant_message, "timestamp": now},
            ],
            session_id=session_id,
        )

    def health(self) -> Dict[str, Any]:
        """Check API health. Returns service status and component health."""
        return self._get("/v1/health")

    # ── Internal request + retry logic ────────────────────────────────────────

    def _request(self, method: str, path: str, body: Optional[Dict] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": f"getmem-python/{__import__('getmem_ai').__version__}",
        }
        data = json.dumps(body).encode() if body is not None else None

        attempt = 0
        while True:
            try:
                req = urllib.request.Request(url, data=data, headers=headers, method=method)
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    return json.loads(resp.read().decode())

            except urllib.error.HTTPError as e:
                resp_body = {}
                try:
                    resp_body = json.loads(e.read().decode())
                except Exception:
                    pass

                # Try to raise the right error class
                try:
                    _raise_for_response(e.code, resp_body)
                except _RETRYABLE as retryable_err:
                    if attempt >= self.max_retries:
                        raise

                    # Rate limit: respect retry_after
                    if isinstance(retryable_err, RateLimitedError):
                        wait = retryable_err.retry_after
                    else:
                        # Exponential backoff: 1s, 2s, 4s for 500; 2s, 4s, 8s for 503
                        base = 2 if isinstance(retryable_err, ServiceUnavailableError) else 1
                        wait = base * (2 ** attempt)

                    time.sleep(wait)
                    attempt += 1
                    continue

            except urllib.error.URLError as e:
                if "timed out" in str(e.reason).lower():
                    raise TimeoutError(f"Request timed out after {self.timeout}s")
                raise ConnectionError(f"Connection error: {e.reason}")

    def _post(self, path: str, body: Dict) -> Dict[str, Any]:
        return self._request("POST", path, body)

    def _get(self, path: str) -> Dict[str, Any]:
        return self._request("GET", path)
