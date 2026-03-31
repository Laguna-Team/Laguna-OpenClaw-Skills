---
name: Laguna Affiliate Commerce
description: "Laguna affiliate commerce API: search merchants, browse categories, get merchant info and cashback rates, mint affiliate tracking links, view agent dashboard with balance and conversions, withdraw USDC commissions, and check withdrawal status. Use when the user asks about cashback deals, affiliate links, merchant search, earning crypto commissions, USDC payouts, or shopping rewards."
homepage: https://laguna.network
metadata: {"openclaw":{"emoji":"🦞","requires":{"bins":["python3"],"env":["LAGUNA_MCP_URL"]},"primaryEnv":"LAGUNA_MCP_URL"}}
---

# OpenClaw Laguna 🦞

**Affiliate commerce for autonomous agents. Earn USDC commissions by routing users to merchant deals.**

One API connection. Full affiliate commerce stack.

## What Can You Do?

### Find Deals
```text
"Find me the best cashback deals for travel in Singapore"
```

### Compare Rates
```text
"What's the cashback rate for Nike vs Adidas?"
```

### Create Affiliate Links
```text
"Create an affiliate link for Trip.com"
```

### Track Earnings
```text
"Show me my dashboard — how much USDC have I earned?"
```

### Cash Out
```text
"Withdraw my USDC balance to my wallet"
```

## Quick Start

```bash
export LAGUNA_MCP_URL="https://agents-dev.laguna.network/mcp"
```

## Python Client

### Discovery (No Identity Required)

```bash
# Browse all categories
python3 {baseDir}/scripts/laguna_client.py get-categories

# Browse categories filtered by country
python3 {baseDir}/scripts/laguna_client.py get-categories --geo SG

# Search merchants by name
python3 {baseDir}/scripts/laguna_client.py search-merchants --query "nike"

# Browse top cashback deals (no query = browse mode)
python3 {baseDir}/scripts/laguna_client.py search-merchants --sort cashback_rate --limit 10

# Search by category and country
python3 {baseDir}/scripts/laguna_client.py search-merchants --category travel --geo SG --limit 5

# Get detailed merchant info and rates
python3 {baseDir}/scripts/laguna_client.py get-merchant-info --merchant-id nike
python3 {baseDir}/scripts/laguna_client.py get-merchant-info --merchant-id trip-com --geo SG
```

### Agent Operations (Identity Required)

```bash
# Create an affiliate link (auto-provisions agent on first use)
python3 {baseDir}/scripts/laguna_client.py mint-link --merchant-id nike --wallet 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18

# Deep link to a specific product page
python3 {baseDir}/scripts/laguna_client.py mint-link --merchant-id nike --wallet 0x742d...bD18 --target-url "https://www.nike.com/running-shoes" --geo US

# Use email instead of wallet
python3 {baseDir}/scripts/laguna_client.py mint-link --merchant-id trip-com --email agent@example.com --geo SG

# Quick balance check
python3 {baseDir}/scripts/laguna_client.py get-dashboard --wallet 0x742d...bD18

# Full dashboard with links, conversions, and analytics
python3 {baseDir}/scripts/laguna_client.py get-dashboard --wallet 0x742d...bD18 --include links,conversions,analytics

# Filter conversions by status
python3 {baseDir}/scripts/laguna_client.py get-dashboard --wallet 0x742d...bD18 --include conversions --status confirmed

# Withdraw full balance
python3 {baseDir}/scripts/laguna_client.py withdraw --wallet 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18

# Withdraw specific amount
python3 {baseDir}/scripts/laguna_client.py withdraw --wallet 0x742d...bD18 --amount 50.00

# Check withdrawal status (call 5-15 seconds after withdraw)
python3 {baseDir}/scripts/laguna_client.py withdrawal-status --withdrawal-id "uuid-from-withdraw"
```

## Core Workflow

1. **Browse** → `get-categories` to see what's available
2. **Search** → `search-merchants` to find merchants by name, category, or geo
3. **Inspect** → `get-merchant-info` for detailed rates and terms
4. **Mint** → `mint-link` to create a tracked affiliate link (auto-provisions your agent)
5. **Track** → `get-dashboard` to monitor earnings and conversions
6. **Withdraw** → `withdraw` to cash out USDC to your wallet

## API Endpoints Reference

| Command | Description | Key Params |
|---------|-------------|------------|
| `search-merchants` | Search or browse merchants | `--query`, `--category`, `--geo`, `--sort`, `--limit` |
| `get-categories` | Browse merchant categories | `--geo` |
| `get-merchant-info` | Detailed merchant info + rates | `--merchant-id` (required), `--geo` |
| `mint-link` | Create affiliate tracking link | `--merchant-id` (required), `--wallet` or `--email` |
| `get-dashboard` | Agent balance + performance | `--wallet` or `--email`, `--include`, `--status` |
| `withdraw` | Request USDC withdrawal | `--wallet` (required), `--amount` |
| `withdrawal-status` | Check withdrawal tx status | `--withdrawal-id` (required) |

## Key Concepts

- **Agent auto-provisioning**: Agent account created automatically on first `mint-link`. No separate registration.
- **Commission lifecycle**: Pending (30–90 days merchant window) → Confirmed → Available → Withdrawn.
- **Merchant IDs**: Lowercase hyphen-separated slugs (`nike`, `trip-com`, `i-herb`). Always get from `search-merchants`.
- **Geo filtering**: ISO 3166-1 alpha-2 codes (`SG`, `US`, `JP`). Filters merchants/rates by country.
- **Wallet formats**: EVM (`0x` + 40 hex), TON (`EQ`/`UQ` prefix), Solana (base58, 32-44 chars).
- **Withdrawal**: Currently Base chain (EVM wallets). 1% fee. TON/Solana coming soon.
- **Rate limits**: 100 requests per minute per IP.

## Error Handling

| Error | What to Do |
|-------|-----------|
| `IDENTITY_REQUIRED` | Provide `--wallet` or `--email` |
| `MERCHANT_NOT_FOUND` | Check slug via `search-merchants` |
| `INSUFFICIENT_BALANCE` | Check balance via `get-dashboard` first |
| `429 Too Many Requests` | Wait `retryAfter` seconds, limit is 100/min |
| Empty search results | Broaden query, remove `--geo`/`--category` filters |

## Detailed Workflows

For end-to-end scenarios and advanced usage patterns, see `{baseDir}/references/workflows.md`.

## Pricing

Free to use. Laguna takes a commission split from affiliate networks — agents keep the net rate shown in merchant info.

## Get Started

1. Set environment variable: `export LAGUNA_MCP_URL="https://agents-dev.laguna.network/mcp"`
2. Run: `python3 {baseDir}/scripts/laguna_client.py search-merchants --query "nike"`

## Links

- [Laguna](https://laguna.network)
