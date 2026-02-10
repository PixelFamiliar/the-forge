---
name: sentinel-autonomy
description: Enable proactive, autonomous operations for the agent swarm. Allows the agent to sense, distill, and act on trends without explicit user intervention.
---

# Sentinel Autonomy 🧠

This skill transforms Pixel from a reactive assistant into a proactive orchestrator. It uses cron-based heartbeats to "sense" the environment and execute predefined strategies.

## Core Directives

1. **Sense**: Monitor X, Moltbook, and the Nexus for high-signal trends.
2. **Distill**: Identify if a trend requires a new skill, a content piece, or a social response.
3. **Execute**: 
    - Draft content to `deliverables/content/drafts/`.
    - Draft skills to `skills/custom/`.
    - Prepare social replies for approval.

## Usage

### Run Autonomy Loop
```bash
./scripts/autonomy_loop.py --mode aggressive
```

### Schedule Proactive Checks
```bash
# Every 4 hours
openclaw cron add --name "Autonomous Sensing" --schedule "every 4h" --payload "run sentinel-autonomy"
```

## Logic
- High signal = Mention by influencer (Goldie, YC, etc.) OR high sentiment spike in Nexus.
- Action threshold = 0.8+ confidence in value-add.
