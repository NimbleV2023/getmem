# getmem.ai — Persistent Memory for AI Agents

> Your AI agent remembers everything. Send raw messages, get back context. 2 lines of code.

**[Join the waitlist →](https://getmem.ai)**

---

## The problem

Every time a user starts a new session with your AI agent, it remembers nothing. You work around it by:

- Dumping entire chat history into the context (breaks at scale, burns tokens)
- Building custom RAG pipelines (weeks of work, unreliable retrieval)
- Manually deciding what to save and writing extraction logic yourself

getmem solves all of this in 2 lines. Send the raw conversation — getmem figures out what to remember.

---

## How it works

```python
import getmem

mem = getmem.init("gm_your_api_key")

# After each turn — send raw messages, we extract what matters automatically
mem.ingest("user_123", messages=messages)

# Before each turn — get the right context
context = mem.get("user_123", query=user_message)

# Use it
prompt = f"{context}\n\nUser: {user_message}"
```

That's it. You never write extraction logic. getmem runs an internal LLM pass on each `ingest()` call, extracts what's worth keeping, deduplicates against existing memories, and stores it. The developer just sends the raw conversation.

Works with **any LLM** — OpenAI, Anthropic Claude, Google Gemini, Mistral, or any local model.  
Works with **any framework** — LangChain, LlamaIndex, raw API calls, or your own stack.

---

## JavaScript / TypeScript

```typescript
import getmem from 'getmem'

const mem = getmem.init('gm_your_api_key')

// After each turn
await mem.ingest('user_123', { messages })

// Before each turn
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

# Ingest a conversation turn — extraction happens automatically
mem.ingest(user_id: str, messages: List[dict]) -> None

# Retrieve relevant context for a query
mem.get(user_id: str, query: str) -> str  # formatted context string, ready for prompt

# List all memories for a user
mem.list(user_id: str) -> List[Memory]

# Delete a specific memory
mem.delete(user_id: str, id: int) -> None

# Delete all memories for a user
mem.delete(user_id: str) -> None
```

### What `messages` looks like

Standard OpenAI message format:

```python
messages = [
    {"role": "user", "content": "I'm building a Python FastAPI service on AWS..."},
    {"role": "assistant", "content": "Got it, here's how I'd structure that..."}
]

mem.ingest("user_123", messages=messages)
# getmem extracts: "User is building a Python FastAPI service on AWS"
# Stores it. Deduplicates. Done.
```

---

## Why not just use Mem0?

The critical difference: **Mem0 requires you to decide what to remember.** You call `mem.add("user_123", "some fact you manually extracted")`. That means you're still writing extraction logic — which defeats the whole point.

getmem accepts raw messages and handles extraction automatically. Send the conversation, get back context. That's the 2-line promise.

| | **getmem.ai** | Mem0 | Zep | DIY RAG |
|---|---|---|---|---|
| Lines to integrate | **2** | ~15 | ~20 | 100+ |
| Automatic extraction from raw messages | ✅ | ❌ | ❌ | ❌ |
| Graph memory | ✅ | ✅ | ✅ | ❌ |
| Intelligent context selection | ✅ | Partial | Partial | ❌ |
| Pay per use | ✅ | ❌ | ❌ | ❌ |
| Setup time | **< 2 min** | ~30 min | ~1 hour | Days |

---

## Architecture

- **Extraction layer** — LLM pass on raw messages, pulls out facts, preferences, entities
- **Graph layer** (Neo4j) — entity relationships and knowledge graph
- **Vector layer** (Qdrant) — semantic similarity search across all memories  
- **Metadata layer** (PostgreSQL) — user management, billing, audit logs
- **Context builder** — selects and ranks the most relevant memories for each query

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

Charged per `mem.ingest()` and `mem.get()` call — like Stripe for memory.  
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
