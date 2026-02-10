---
name: discourse-distiller
description: Automate the transformation of AI agent discourse trends from the Nexus into publishable Substack drafts and social media content. Use when the user needs to convert trending narratives into revenue-generating SEO content for The Shell Pile.
---

# Discourse Distiller 🥃

This skill automates the production of high-quality Substack drafts and social content based on trending narratives identified by the Nexus Agent Discourse Tracker.

## Core Workflow

1.  **Analyze Trends:** Scan the latest Nexus sync data for narratives with rising engagement scores.
2.  **Distill Narrative:** Use the `distill_narrative.py` script to synthesize raw data (X posts, Discord messages, news) into a structured outline.
3.  **Draft Content:** Apply the brand voice from `substack_voice.md` to generate a full Substack article draft.
4.  **Visualize:** Generate FLUX-ready image prompts for the header and inline assets.
5.  **Deliver:** Save the output to `/deliverables/content/` for human review.

## Scripts

### `scripts/distill_narrative.py`
Synthesizes multi-source discourse data into a coherent narrative arc.
Usage: `python3 scripts/distill_narrative.py --topic "ClawPhone" --limit 50`

## References

### `references/substack_voice.md`
Guidelines for *The Shell Pile* brand voice: Playful, analytical, future-focused, and "agent-native."

## When to Use
- When a new narrative spikes on the Nexus dashboard.
- When it's publication day (Wednesday/Saturday) and a draft is needed.
- When a viral thread needs a deeper technical breakdown for the community.
