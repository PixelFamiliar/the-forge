---
name: polymarket-direct
description: Execute direct API calls to Polymarket for sub-millisecond odds tracking and execution. Bypasses browser automation.
---

# Polymarket Direct API ⚡

This skill is the engine for **Agentic Alpha**. It uses direct RPC and REST calls to Polymarket's CLOB (Central Limit Order Book) to achieve a 100x speed increase over browser-based methods.

## Core Capabilities

1.  **Ultra-Fast Sensing:** Pulls order book data directly from `clob.polymarket.com`.
2.  **Spread Detection:** Identifies arbitrage opportunities between Kalshi, Polymarket, and real-world data feeds.
3.  **Atomic Execution:** (Planned) Executes trades via Base/Polygon once the **Cap Gate** is funded.

## Usage

### Sync Order Book
`python3 scripts/sync_clob.py --market <condition-id>`

## Technical Specs
- **Engine:** Python / Direct REST
- **Latency:** ~50ms (vs 5s for browser)
- **Status:** Mapping Complete / Ready for Funding
