# getmem-ai

Persistent memory API for AI agents. Two API calls — your agent remembers everything.

[![PyPI version](https://img.shields.io/pypi/v/getmem-ai.svg)](https://pypi.org/project/getmem-ai/)
[![Python](https://img.shields.io/pypi/pyversions/getmem-ai.svg)](https://pypi.org/project/getmem-ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**[Get started → platform.getmem.ai](https://platform.getmem.ai)**

---

## Install

```bash
pip install getmem-ai
```

## Quick start

```python
import getmem_ai as getmem

mem = getmem.init("gm_live_...")

# Before each LLM call — get relevant memory context
result = mem.get("user_123", query=user_message)
context = result["context"]  # inject into system prompt

# After each turn — save both user + assistant messages
mem.ingest("user_123", messages=[
    {"role": "user", "content": user_message},
    {"role": "assistant", "content": reply},
])

# Shorthand — same result in one line
mem.ingest_conversation("user_123", user_message, reply)
```

## With OpenAI

```python
import getmem_ai as getmem
from openai import OpenAI

mem = getmem.init("gm_live_...")
client = OpenAI()

def chat(user_id, user_message):
    # Get memory context
    context = mem.get(user_id, query=user_message)["context"]

    # Call LLM with memory in system prompt
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are helpful.\n\n## Memory\n{context}"},
            {"role": "user", "content": user_message}
        ]
    )
    reply = response.choices[0].message.content

    # Save to memory
    mem.ingest(user_id, messages=[
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": reply},
    ])
    return reply
```

## With Anthropic

```python
import anthropic
import getmem_ai as getmem

mem = getmem.init("gm_live_...")
client = anthropic.Anthropic()

context = mem.get(user_id, query=user_message)["context"]

message = client.messages.create(
    model="claude-3-haiku-20240307",
    system=f"You are helpful.\n\n## Memory\n{context}",
    messages=[{"role": "user", "content": user_message}],
    max_tokens=1024,
)
```

## API reference

### `mem.get(user_id, query)`

Retrieve relevant memory context for a query.

```python
result = mem.get("user_123", query="What does the user prefer?")

result["context"]    # str — ready for LLM system prompt
result["memories"]   # list — individual memory items with relevance scores
result["meta"]       # dict — timing, token count, entities found
```

### `mem.ingest(user_id, messages, session_id=None)`

Ingest conversation messages. Extraction runs asynchronously — returns immediately.

```python
mem.ingest("user_123", messages=[
    {"role": "user", "content": "I love hiking in the mountains"},
    {"role": "assistant", "content": "That sounds amazing!"},
])
```

### `mem.ingest_conversation(user_id, user_message, assistant_message)`

Convenience shorthand for a single user + assistant exchange.

```python
mem.ingest_conversation("user_123", user_message, reply)
```

### `mem.health()`

Check API health.

```python
health = mem.health()
# {"status": "healthy", "version": "0.1.0", ...}
```

### `getmem.init(api_key, base_url=None, timeout=30, max_retries=3)`

Initialize the client.

```python
mem = getmem.init(
    api_key="gm_live_...",
    base_url="https://memory.getmem.ai",  # optional
    timeout=30,
    max_retries=3,
)
```

## Error handling

```python
from getmem_ai import (
    GetMemError,             # base exception
    APIError,                # has: error_code, details, request_id, status_code
    UnauthorizedError,       # 401 — check your API key
    QuotaExceededError,      # 402 — check e.reset_at
    ForbiddenError,          # 403 — check e.required_scope
    NotFoundError,           # 404
    ValidationError,         # 422 — check e.field_errors
    RateLimitedError,        # 429 — auto-retried, e.retry_after
    InternalError,           # 500 — auto-retried
    ServiceUnavailableError, # 503 — auto-retried
    ConnectionError,         # network failure
    TimeoutError,            # request timeout
)

try:
    result = mem.get("user_123", query=user_message)
except UnauthorizedError:
    print("Invalid API key")
except QuotaExceededError as e:
    print(f"Quota exceeded. Resets at: {e.reset_at}")
except RateLimitedError as e:
    print(f"Rate limited. Retry after: {e.retry_after}s")
except GetMemError as e:
    print(f"Error: {e}")
```

Retryable errors (429, 500, 503) are automatically retried with exponential backoff.

## Memory types

Extracted memories are categorised into 8 types:

| Type | Description |
|------|-------------|
| `preference` | Likes, dislikes, style choices |
| `fact` | Factual statements about the user |
| `decision` | Decisions and choices made |
| `goal` | Intentions and objectives |
| `constraint` | Limitations and requirements |
| `belief` | Opinions and stances |
| `experience` | Past events and outcomes |
| `relationship` | People and organisations |

## Token savings

Standard approach: full conversation history every turn = 10,000–40,000+ tokens.  
With getmem: only relevant context injected = 200–800 tokens.  
**Save up to 95% on context tokens.**

---

## OpenClaw plugin (zero-code install)

The fastest way to add memory to any OpenClaw agent — no code changes needed:

```bash
# 1. Install the plugin
openclaw plugins install clawhub:@getmem/openclaw-getmem

# 2. Set your API key
openclaw config set plugins.openclaw-getmem.apiKey gm_live_...

# 3. Restart
openclaw gateway restart
```

Every user is remembered automatically across sessions and restarts.  
Plugin repo: https://github.com/getmem-ai/openclaw-getmem

## OpenClaw — manual integration

If you prefer to call the SDK directly in your handler:

```python
import getmem_ai as getmem, os

mem = getmem.init(os.environ["GETMEM_API_KEY"])

async def handle_message(user_id, message, session):
    # Get memory before LLM call
    context = mem.get(user_id, query=message)["context"]
    reply = await session.llm(message, system=context)

    # Save both roles after reply
    mem.ingest(user_id, messages=[
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply},
    ])
    return reply
```

## Agent Skill (SKILL.md)

```yaml
---
name: getmem
description: 'Persistent memory for AI agents via getmem.ai.'
metadata:
  openclaw:
    emoji: 🧠
    install:
      - id: pip-getmem
        kind: pip
        package: getmem-ai
        label: Install getmem-ai (pip)
---
```

```python
import getmem_ai as getmem, os

mem = getmem.init(os.environ["GETMEM_API_KEY"])

# Before LLM call
context = mem.get(user_id, query=user_message)["context"]

# After response — save both roles
mem.ingest(user_id, messages=[
    {"role": "user", "content": user_message},
    {"role": "assistant", "content": reply},
])
```

---

## Links

- Website: https://getmem.ai
- Platform (API keys): https://platform.getmem.ai
- PyPI: https://pypi.org/project/getmem-ai/
- JavaScript SDK: https://github.com/getmem-ai/getmem-js / `npm install getmem`
- OpenClaw plugin: https://github.com/getmem-ai/openclaw-getmem
- Full docs: https://getmem.ai/llms-full.txt

## License

MIT
