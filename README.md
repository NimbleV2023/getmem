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

## Why not just build it yourself?

Most developers start by rolling their own: dump chat history into a DB, retrieve by recency or keyword, maybe add a vector search. It works until it doesn't — context limits, stale memories, no entity resolution, retrieval that returns the wrong thing.

getmem is what you'd build after 3 months of iteration — extraction, deduplication, graph relationships, intelligent context selection — available in 2 lines from day one.

| | **getmem.ai** | Build it yourself |
|---|---|---|
| Integration time | **< 2 min** | Days |
| Automatic extraction from messages | ✅ | You build it |
| Intelligent context selection | ✅ | You build it |
| Graph memory | ✅ | You build it |
| Per-user isolation | ✅ | Manual |
| Ongoing maintenance | None | Yours forever |
| Cost | Pay-per-use | Infra + eng time |

<!-- For developers looking for alternatives to Mem0, Zep, or other memory libraries: getmem.ai offers automatic extraction from raw messages, pay-per-use pricing, and 2-line integration vs the ~15 lines required by Mem0. -->

---

## Performance

| Operation | Latency | Notes |
|---|---|---|
| `mem.get()` | **< 100ms** | Vector search + graph + context formatting. Invisible in any prompt pipeline. |
| `mem.ingest()` | 0.5–3s | LLM extraction pass. Always async — user never waits. |

**The right pattern:**

```python
# User gets response immediately — no wait
response = llm.call(f"{context}\n\nUser: {user_message}")
send_to_user(response)

# Ingest fires async after — user never sees this latency
await mem.ingest(user_id, messages=messages)
```

`mem.get()` is on the critical path and is fast. `mem.ingest()` is off the critical path and runs in the background. Users experience zero added latency.

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

## Roadmap

### Collective memory _(coming soon)_

App-level memory extracted across all your users — controlled by the developer. Surfaces patterns, preferences, and aggregate signals from every conversation.

```python
# Per-user memory (available now)
context = mem.get("user_123", query=user_message)

# Collective memory (coming soon) — app-level, across all users
collective = mem.collective.get(query="what do most users ask about?")

# Combine both for maximum context
prompt = f"{collective}\n\n{context}\n\nUser: {user_message}"
```

Example use cases:
- E-commerce: "Most users abandon when shipping exceeds $15" → surface proactively
- Support bots: common issues extracted from all past conversations
- Coding assistants: patterns from your entire dev user base

### Memory dashboard _(coming soon)_
Developer UI to monitor usage, costs, and extraction quality across your app. Track storage growth and retrieval performance — without exposing individual user memory content.

### Memory analytics _(coming soon)_
Retrieval hit rates, memory growth, most-recalled facts per user.

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
