# OpenClaw Laguna 🦞

Affiliate commerce for autonomous agents. Earn USDC commissions by routing users to merchant deals.

## Features

- **Search & Browse**: Find merchants by name, category, or country with cashback rates
- **Mint Links**: Create tracked affiliate links that earn USDC commission on purchases
- **Track Earnings**: Dashboard with balance, conversions, and analytics
- **Withdraw USDC**: Cash out commissions to your wallet on Base chain

## Installation

```bash
export LAGUNA_MCP_URL="https://agents-dev.laguna.network/mcp"
```

## Quick Start

```bash
# Browse top cashback deals
python scripts/laguna_client.py search-merchants --sort cashback_rate

# Search for a specific merchant
python scripts/laguna_client.py search-merchants --query "nike" --geo SG

# Get merchant details
python scripts/laguna_client.py get-merchant-info --merchant-id nike

# Create an affiliate link
python scripts/laguna_client.py mint-link --merchant-id nike --wallet 0x742d...bD18

# Check your earnings
python scripts/laguna_client.py get-dashboard --wallet 0x742d...bD18
```

> **Note**: For detailed workflow examples, see [`./references/workflows.md`](./references/workflows.md).

## Available Commands

| Command               | Description                                |
| --------------------- | ------------------------------------------ |
| `search-merchants`    | Search or browse affiliate merchants       |
| `get-categories`      | Browse merchant categories with counts     |
| `get-merchant-info`   | Get merchant details and cashback rates    |
| `mint-link`           | Create an affiliate tracking link          |
| `get-dashboard`       | View agent balance, links, and conversions |
| `withdraw`            | Request USDC withdrawal to wallet          |
| `withdrawal-status`   | Check withdrawal transaction status        |

## Links

- [Laguna](https://laguna.network)
