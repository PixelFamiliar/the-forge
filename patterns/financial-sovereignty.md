---
name: financial-sovereignty
description: Manage and monitor agent-controlled capital within strict safety limits (Cap Gate). Tracks ROI, float, and transaction health.
---

# Financial Sovereignty 💰🛡️

This skill governs the squad's "Pocket Money." It ensures the agent swarm has the liquidity to execute arbitrage while maintaining strict "Fortress Mac" security.

## Core Directives

1.  **Cap Gate Enforcement:** Never exceed the defined float limit (e.g., $100 USDC).
2.  **Telemetry:** Feeds real-time wallet balance and ROI metrics to the **Nexus Finance Widget**.
3.  **Security:** Only interacts with the vault-injected `BASE_WALLET_PRIVATE_KEY`. Plaintext keys are strictly prohibited.

## Integration

- **Dashboard:** `FinanceWidget.tsx` (Nexus UI)
- **Arbitrage:** Feeds liquidity data to `polymarket-direct`.

## Status
- **Widget:** Live in Dev
- **Logic:** Pending Wallet Initialization
