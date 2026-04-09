---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Pub-Sub Message Patterns

## Quick Reference

| Pattern | Use |
|---------|-----|
| **Topic broadcast** | Chat rooms, notifications |
| **Fan-out** | Redis Pub/Sub, NATS, SNS+SQS |

**Ordering:** Per-partition order if using Kafka; WS itself unordered unless designed.

## Code Examples

```text
Topic: notifications.user.{userId}
Payload: { "type": "mention", "id": "..." }
```

## Deep Dive Sources

- [Enterprise Integration Patterns — Publish-Subscribe](https://www.enterpriseintegrationpatterns.com/patterns/messaging/PublishSubscribeChannel.html)
