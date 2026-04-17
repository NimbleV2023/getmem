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

## OpenClaw integration

```python
import getmem_ai as getmem, os

mem = getmem.init(os.environ["GETMEM_API_KEY"])

async def handle_message(user_id, message, session):
    context = mem.get(user_id, query=message)["context"]
    reply = await session.llm(message, system=context)
    mem.ingest_conversation(user_id, message, reply)
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
