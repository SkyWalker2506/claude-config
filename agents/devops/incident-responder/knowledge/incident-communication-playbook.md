# Incident Communication Playbook

## Structured Incident Response Workflow

### Phase 1: Detection and Triage (0-5 min)
1. Confirm the incident is real (not a false alarm)
2. Assess scope: what systems/users are affected?
3. Assign severity (P0/P1/P2/P3)
4. Notify incident commander and on-call team

### Phase 2: Contain and Diagnose (5-30 min)
1. Stop the bleeding — isolate affected components if possible
2. Collect evidence: logs, metrics, error rates, timestamps
3. Form initial hypothesis: what changed recently?
   - Recent deploys (check in last 24h)
   - Configuration changes
   - Infrastructure changes
   - Traffic spikes
4. Communicate status to stakeholders

### Phase 3: Resolve (30 min - hours)
1. Execute fix or rollback plan
2. Verify resolution with monitoring
3. Document timeline of events
4. Confirm with affected users/teams

### Phase 4: Post-Incident (24-72h)
1. Write post-mortem (blameless)
2. Identify root cause (5 Whys)
3. Document action items with owners and deadlines
4. Share learnings with broader team

## Severity Matrix

| Level | Description | Response Time | Example |
|-------|-------------|--------------|---------|
| P0 | Complete outage, all users | Immediate, 24/7 | Site down |
| P1 | Major feature broken, most users | <30 min business hours | Auth failing |
| P2 | Degraded performance, partial impact | <2h business hours | Slow queries |
| P3 | Minor issue, workaround exists | Next business day | UI glitch |

## Status Update Template

For external/stakeholder communication:
```
[TIME] Status Update - [INCIDENT NAME]

Impact: {what users are experiencing}
Status: {Investigating / Identified / Monitoring / Resolved}
Next update: {time}

Details: {brief technical summary appropriate to audience}
```

## Post-Mortem Template

```markdown
# Post-Mortem: [Incident Name]
Date: 
Duration: 
Severity: 

## Summary
{2-3 sentence description of what happened and impact}

## Timeline
| Time | Event |
|------|-------|
| HH:MM | Issue first detected |
| HH:MM | On-call paged |
| HH:MM | Root cause identified |
| HH:MM | Fix deployed |
| HH:MM | Incident resolved |

## Root Cause
{The 5 Whys analysis}

## Impact
- Users affected: N
- Duration: X minutes
- Revenue impact: $Y (if known)

## What Went Well
- 

## What Went Poorly
- 

## Action Items
| Item | Owner | Due Date |
|------|-------|---------|
| | | |
```

## Rollback Decision Framework

Rollback when:
- Root cause is a recent deploy
- Fix is unknown or will take >30 min
- P0/P1 severity with user impact
- Rollback is clean (no data migration)

Don't rollback when:
- Schema migration has already run
- Rollback would cause different breakage
- Issue is infrastructure (not code)
- Fix is 5 minutes away
