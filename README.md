# getmem-ai

Persistent memory API for AI agents. Two API calls — your agent remembers everything.

```bash
pip install getmem-ai
```

```python
import getmem_ai as getmem

mem = getmem.init("gm_your_api_key")

# After each turn — automatic extraction
mem.ingest("user_123", messages=messages)

# Before each turn — intelligent context
context = mem.get("user_123", query=user_message)
```

**[Get started → platform.getmem.ai](https://platform.getmem.ai)**

Docs: [getmem.ai](https://getmem.ai) · PyPI: [getmem-ai](https://pypi.org/project/getmem-ai/)

## OpenClaw plugin

The fastest way to add getmem.ai memory to any OpenClaw agent — no code changes needed:

```bash
# Install
openclaw plugins install clawhub:@getmem/openclaw-getmem

# Set your API key
openclaw config set plugins.openclaw-getmem.apiKey gm_live_...

# Restart
openclaw gateway restart
```

Every user is remembered automatically across sessions and restarts.

- Plugin repo: https://github.com/getmem-ai/openclaw-getmem
- Get API key: https://platform.getmem.ai

## OpenClaw — manual integration

If you prefer to call the SDK directly in your own handler:

```python
import getmem_ai as getmem, os

mem = getmem.init(os.environ["GETMEM_API_KEY"])

async def handle_message(user_id, message, session):
    context = mem.get(user_id, query=message)["context"]
    reply = await session.llm(message, system=context)
    mem.ingest(user_id, messages=[
    {"role": "user", "content": message},
    {"role": "assistant", "content": reply},
])
# or shorthand: mem.ingest_conversation(user_id, message, reply)
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

import getmem_ai as getmem, os
mem = getmem.init(os.environ["GETMEM_API_KEY"])
context = mem.get(user_id, query=user_message)["context"]
mem.ingest_conversation(user_id, user_message, reply)
```
