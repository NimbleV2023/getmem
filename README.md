# getmem.ai — Persistent Memory for AI Agents

> Add memory to your AI agent in 2 lines of code.

**[Join the waitlist →](https://getmem.ai)**

---

## The problem

Every time a user starts a new session with your AI agent, it remembers nothing. You work around it by:

- Dumping entire chat history into the context (breaks at scale, burns tokens)
- Building custom RAG pipelines (weeks of work, unreliable retrieval)
- Using Mem0 (works, but ~15 lines of setup and subscription pricing)

getmem solves this with 2 lines of code and pay-per-use pricing.

---

## How it works

```python
import getmem

mem = getmem.init("gm_your_api_key")

# Save what matters
mem.add("user_123", "User is a senior Python developer who prefers concise answers")

# Get the right context, every time
context = mem.get("user_123", query=user_message)

# Drop it straight into your prompt
prompt = f"{context}\n\nUser: {user_message}"
```

Works with **any LLM** — OpenAI, Anthropic Claude, Google Gemini, Mistral, or any local model.  
Works with **any framework** — LangChain, LlamaIndex, raw API calls, or your own stack.

---

## JavaScript / TypeScript

```typescript
import getmem from 'getmem'

const mem = getmem.init('gm_your_api_key')

await mem.add('user_123', 'User prefers dark mode and concise answers')
const context = await mem.get('user_123', { query: userMessage })

const response = await openai.chat.completions.create({
  messages: [
    { role: 'system', content: context },
    { role: 'user', content: userMessage }
  ]
})
```

---

## API reference

```python
# Initialize
mem = getmem.init("gm_your_api_key")

# Store a memory
mem.add(user_id: str, text: str) -> Memory

# Retrieve relevant memories for a query
mem.get(user_id: str, query: str) -> str  # formatted context string

# List all memories for a user
mem.list(user_id: str) -> List[Memory]

# Delete a specific memory
mem.delete(user_id: str, id: int) -> None

# Delete all memories for a user
mem.delete(user_id: str) -> None
```

---

## Why not just use Mem0?

| | **getmem.ai** | Mem0 | Zep | DIY RAG |
|---|---|---|---|---|
| Lines to integrate | **2** | ~15 | ~20 | 100+ |
| Graph memory | ✅ | ✅ | ✅ | ❌ |
| Intelligent context selection | ✅ | Partial | Partial | ❌ |
| Pay per use | ✅ | ❌ | ❌ | ❌ |
| Setup time | **< 2 min** | ~30 min | ~1 hour | Days |
| Per-user isolation | ✅ | ✅ | ✅ | Manual |

---

## Architecture

Under the hood, getmem uses a graph + vector hybrid:

- **Graph layer** (Neo4j) — stores entities and relationships between memories
- **Vector layer** (Qdrant) — semantic similarity search across all memories
- **Metadata layer** (PostgreSQL) — user management, billing, audit logs
- **Context builder** — proprietary algorithm that selects and ranks the most relevant memories for each query

---

## Use cases

- **Customer support bots** — remember account history, past issues, preferences
- **Coding assistants** — remember stack, coding style, project context  
- **Personal AI assistants** — remember preferences, relationships, ongoing tasks
- **Sales bots** — remember company info, previous conversations, deal stage
- **Educational tools** — remember student progress, weak areas, learning style

---

## Pricing

Pay-per-use. No monthly minimums. No seat licenses.

You're charged per `mem.add()` and `mem.get()` call — like Stripe for memory.  
Scales from 0 to millions of users without changing plans.

---

## Status

Currently in **early access**. We're onboarding developers now.

**[Join the waitlist at getmem.ai →](https://getmem.ai)**

---

## LLM-readable docs

- [`/llms.txt`](https://getmem.ai/llms.txt) — summary for AI crawlers
- [`/llms-full.txt`](https://getmem.ai/llms-full.txt) — full documentation

---

*© 2026 getmem.ai*
