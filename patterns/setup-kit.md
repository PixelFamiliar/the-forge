---
name: setup-kit
description: Automated setup kit for new OpenClaw users. Generates boilerplate configuration files (SOUL, IDENTITY, AGENTS) and installs a starter skill pack.
---

# OpenClaw Setup Kit 🛠️

This skill enables the rapid deployment of a professional OpenClaw configuration.

## Workflow

1. **Information Gathering**: Collect user name, niche (e.g., SEO, E-commerce, Trading), and desired agent vibe.
2. **Boilerplate Generation**: Create customized `SOUL.md`, `IDENTITY.md`, and `AGENTS.md` files.
3. **Starter Skill Installation**: Install core skills (Bird, Brave, Local File Management).
4. **Validation**: Run a status check to ensure the new agent is healthy.

## Usage

### Initialize New Setup
```bash
./scripts/generate_setup.py --name "User Name" --niche "SEO" --vibe "Professional"
```

## Integration Points

- **Nexus**: Automatically registers the new agent to the local Nexus dashboard for monitoring.
