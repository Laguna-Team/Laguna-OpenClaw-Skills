# Laguna Workflow Examples

End-to-end scenarios showing how to combine Laguna commands.

## Scenario 1: First-Time Agent — Product Search to Link

User wants to find a deal and get an affiliate link.

**Step 1**: Search for the merchant.
```bash
python3 {baseDir}/scripts/laguna_client.py search-merchants --query "nike" --geo SG
```

**Step 2**: Get detailed rates.
```bash
python3 {baseDir}/scripts/laguna_client.py get-merchant-info --merchant-id nike --geo SG
```

Review the cashback rate, cookie duration, and payout days before proceeding.

**Step 3**: Mint the affiliate link. This auto-creates the agent account.
```bash
python3 {baseDir}/scripts/laguna_client.py mint-link --merchant-id nike --wallet 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18 --geo SG
```

**Step 4**: Share the returned `url` with the user. When someone purchases through it, the agent earns commission.

---

## Scenario 2: Category Browse — "What deals are available?"

User asks what Laguna offers without a specific merchant in mind.

**Step 1**: Browse categories.
```bash
python3 {baseDir}/scripts/laguna_client.py get-categories --geo US
```

Returns categories like `travel`, `fashion`, `electronics` with merchant counts and top cashback rates.

**Step 2**: Browse merchants in a category.
```bash
python3 {baseDir}/scripts/laguna_client.py search-merchants --category travel --geo US --sort cashback_rate --limit 5
```

**Step 3**: Present the top deals to the user, then mint links for whichever they choose.

---

## Scenario 3: Rate Comparison

User wants to compare cashback rates across similar merchants.

**Step 1**: Search broadly.
```bash
python3 {baseDir}/scripts/laguna_client.py search-merchants --category fashion --geo SG --sort cashback_rate --limit 10
```

**Step 2**: Get details for top contenders.
```bash
python3 {baseDir}/scripts/laguna_client.py get-merchant-info --merchant-id nike --geo SG
python3 {baseDir}/scripts/laguna_client.py get-merchant-info --merchant-id adidas --geo SG
```

**Step 3**: Compare rates, cookie days, and payout timelines. Present a comparison table to the user.

---

## Scenario 4: Earnings Check and Withdrawal

Agent wants to check balance and cash out.

**Step 1**: Quick balance check.
```bash
python3 {baseDir}/scripts/laguna_client.py get-dashboard --wallet 0x742d...bD18
```

**Step 2**: Check detailed conversions.
```bash
python3 {baseDir}/scripts/laguna_client.py get-dashboard --wallet 0x742d...bD18 --include conversions --status confirmed
```

**Step 3**: Withdraw available balance.
```bash
python3 {baseDir}/scripts/laguna_client.py withdraw --wallet 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18 --amount 50.00
```

**Step 4**: Check withdrawal status after 5–15 seconds.
```bash
python3 {baseDir}/scripts/laguna_client.py withdrawal-status --withdrawal-id "uuid-from-step-3"
```

When status is `completed`, the response includes `txHash` and a BaseScan link.

---

## Scenario 5: Deep Link to a Specific Product

User wants an affiliate link to a specific product page, not just the merchant homepage.

```bash
python3 {baseDir}/scripts/laguna_client.py mint-link \
  --merchant-id nike \
  --wallet 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18 \
  --target-url "https://www.nike.com/t/air-max-90-mens-shoes-abc123" \
  --geo US
```

The returned link redirects through the affiliate network to the exact product page while tracking the click for commission.

---

## Agent Instructions

### When the user asks about deals or shopping:
1. Ask which country they're shopping from (for geo filtering).
2. Use `search-merchants` or `get-categories` to find relevant deals.
3. Present results with cashback rates prominently displayed.
4. Offer to create affiliate links for merchants they're interested in.

### When the user asks to create a link:
1. Confirm you have their wallet address or email.
2. Get the merchant ID from a prior search (never guess the slug).
3. Run `mint-link` and share the returned URL.
4. Mention the commission rate and that earnings appear on their dashboard.

### When the user asks about earnings:
1. Run `get-dashboard` with their wallet address.
2. For a quick check, omit `--include`. For details, add `--include links,conversions,analytics`.
3. Explain pending vs. confirmed vs. available balance.

### When the user asks to withdraw:
1. Check available balance via `get-dashboard` first.
2. Confirm the wallet address and amount.
3. Run `withdraw`, then run `withdrawal-status` after 5–15 seconds.
4. Share the BaseScan transaction link when completed.

## Guardrails

- Never guess merchant IDs — always get them from `search-merchants` results.
- Never claim a withdrawal succeeded until `withdrawal-status` confirms `completed`.
- Always ask for the user's country when geo-specific rates matter.
- Do not expose internal network names or route details to users.
