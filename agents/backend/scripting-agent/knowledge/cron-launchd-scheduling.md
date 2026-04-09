---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Cron and launchd Scheduling

## Quick Reference

| System | File |
|--------|------|
| **cron** | `crontab -e` — `min hour dom mon dow user command` |
| **systemd timer** | Linux service units |
| **launchd** | macOS `~/Library/LaunchAgents/*.plist` |

**Timezone:** cron often server local — document explicitly.

**2025–2026:** Prefer orchestrator (K8s CronJob, GitHub Actions schedule) for cloud-native.

## Patterns & Decision Matrix

| Need | Use |
|------|-----|
| Single user Mac | launchd |
| Server | systemd timer or cron |

## Anti-Patterns

| Bad | Why |
|-----|-----|
| Overlapping long job | Use `flock` or lockfile |

## Code Examples

```cron
0 */6 * * * /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1
```

## Deep Dive Sources

- [cron — man page](https://man7.org/linux/man-pages/man5/crontab.5.html)
- [Apple — launchd](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html)
