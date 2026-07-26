# Memory Management Best Practices

How to use HIPPMEM effectively with your AI assistant.

## When to write memories

Write when the AI learns something that will matter in future sessions:

| Situation | Example |
|-----------|---------|
| **User preference** | "The user prefers Rust over Python for backend work." |
| **Architecture decision** | "Chose PostgreSQL with SKIP LOCKED for the task queue." |
| **Constraint discovered** | "Library X doesn't support async — can't use it." |
| **Bug root cause** | "The race condition was caused by a missing unique constraint." |
| **Correction** | "Previous claim about Redis was wrong — it DOES support exactly-once with consumer groups." |

Don't write:
- Transient conversation details ("user asked what time it is")
- Things the AI can infer from code or documents
- Already-documented project facts

## When to retrieve

| Trigger | Query pattern |
|---------|--------------|
| **New session starts** | "What is the current project context?" or domain-specific queries |
| **User mentions a past decision** | "Why did we choose [X] over [Y]?" |
| **User references something from history** | "What did we say about [topic]?" |
| **About to make a decision** | "What constraints are relevant to [decision]?" |

## Writing effective queries

HIPPMEM uses multi-channel recall (BM25 + entity + semantic + topic). Queries that work well:

✅ **Good:** "Why did we choose PostgreSQL as the message broker?"
→ Fires entity channel (PostgreSQL) + semantic channel (message broker) + causal (why)

✅ **Good:** "What are the user's preferences for development tools?"
→ Fires entity (development tools) + topic (preferences)

❌ **Weak:** "database"
→ Single keyword, no semantic context

❌ **Weak:** "Tell me everything"
→ Too vague for any channel

## Prompt templates

### Session start — context injection

```
Use retrieve_memories to recall relevant project context before we begin.
Focus on: recent decisions, user preferences, and active tasks.
```

### Session end — memory capture

```
Before we finish, use write_memory to record:
1. Key decisions made in this session
2. New facts or constraints discovered
3. Any corrections to previous understanding
Use appropriate content_type for each.
```

### Ongoing — decision tracking

```
Before making this decision, use retrieve_memories to check:
- Have we discussed this before?
- Are there relevant constraints?
- What was the user's preference on related topics?
```

## Content types

Use the right `content_type` for each memory — it affects retrieval quality:

| Type | When to use |
|------|------------|
| `Decision` | A choice was made |
| `Preference` | User expressed a preference |
| `ProjectKnowledge` | General project fact |
| `Correction` | Fixing a previous mistake |
| `TaskState` | Current status of a task |
| `Event` | Something that happened |
| `Reflection` | Meta-analysis or insight |
