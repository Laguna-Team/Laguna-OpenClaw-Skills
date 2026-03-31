#!/usr/bin/env python3
"""
OpenClaw Laguna - MCP API Client
Affiliate commerce for autonomous agents. Earn USDC commissions via Laguna.

Calls Laguna MCP tools over Streamable HTTP (JSON-RPC over POST).

Usage:
    python laguna_client.py search-merchants [--query <q>] [--category <cat>] [--geo <CC>] [--sort <s>] [--limit <n>]
    python laguna_client.py get-categories [--geo <CC>]
    python laguna_client.py get-merchant-info --merchant-id <slug> [--geo <CC>]
    python laguna_client.py mint-link --merchant-id <slug> [--wallet <addr>] [--email <email>] [--target-url <url>] [--geo <CC>]
    python laguna_client.py get-dashboard [--wallet <addr>] [--email <email>] [--include links,conversions,analytics] [--status <s>] [--from <iso>] [--to <iso>] [--merchant-id <slug>] [--limit <n>]
    python laguna_client.py withdraw --wallet <addr> [--amount <n>]
    python laguna_client.py withdrawal-status --withdrawal-id <uuid>
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional


class LagunaClient:
    """OpenClaw Laguna - MCP API Client over Streamable HTTP."""

    def __init__(self, mcp_url: Optional[str] = None):
        """Initialize with MCP server URL."""
        self.mcp_url = mcp_url or os.environ.get("LAGUNA_MCP_URL")
        if not self.mcp_url:
            raise ValueError(
                "LAGUNA_MCP_URL is required. Set via environment variable or pass to constructor.\n"
                "Example: export LAGUNA_MCP_URL='https://agents-dev.laguna.network/mcp'"
            )
        self._request_id = 0

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def _call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call an MCP tool via JSON-RPC over HTTP POST."""
        # Filter out None values
        arguments = {k: v for k, v in arguments.items() if v is not None}

        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments,
            },
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "OpenClaw-Laguna/1.0",
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.mcp_url, data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                body = json.loads(response.read().decode("utf-8"))

                # JSON-RPC response: extract result
                if "error" in body:
                    return {"success": False, "error": body["error"]}

                result = body.get("result", {})
                # MCP tool results have content array with text items
                content_items = result.get("content", [])
                is_error = result.get("isError", False)

                texts = []
                for item in content_items:
                    if item.get("type") == "text":
                        texts.append(item["text"])

                combined = "\n".join(texts)
                try:
                    parsed = json.loads(combined)
                except (json.JSONDecodeError, TypeError):
                    parsed = {"raw": combined}

                if is_error:
                    return {"success": False, "error": parsed}
                return {"success": True, "data": parsed}

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            try:
                err = json.loads(error_body)
            except json.JSONDecodeError:
                err = {"code": str(e.code), "message": error_body}
            return {"success": False, "error": err}
        except urllib.error.URLError as e:
            return {"success": False, "error": {"code": "NETWORK_ERROR", "message": str(e.reason)}}

    # ==================== Discovery Tools ====================

    def search_merchants(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        geo: Optional[str] = None,
        sort: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Search or browse affiliate merchants. All params optional."""
        return self._call_tool("search_merchants", {
            "query": query,
            "category": category,
            "geo": geo,
            "sort": sort,
            "limit": limit,
        })

    def get_categories(self, geo: Optional[str] = None) -> Dict[str, Any]:
        """Browse merchant categories with counts and top rates."""
        return self._call_tool("get_categories", {"geo": geo})

    def get_merchant_info(self, merchant_id: str, geo: Optional[str] = None) -> Dict[str, Any]:
        """Get detailed merchant info including cashback rates."""
        return self._call_tool("get_merchant_info", {
            "merchant_id": merchant_id,
            "geo": geo,
        })

    # ==================== Agent Tools ====================

    def mint_link(
        self,
        merchant_id: str,
        wallet_address: Optional[str] = None,
        email: Optional[str] = None,
        target_url: Optional[str] = None,
        geo: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create an affiliate tracking link. Auto-provisions agent on first use."""
        return self._call_tool("mint_link", {
            "wallet_address": wallet_address,
            "email": email,
            "merchant_id": merchant_id,
            "target_url": target_url,
            "geo": geo,
        })

    def get_dashboard(
        self,
        wallet_address: Optional[str] = None,
        email: Optional[str] = None,
        include: Optional[list] = None,
        conversion_status: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        merchant_id: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        """View agent dashboard with balance and performance data."""
        return self._call_tool("get_dashboard", {
            "wallet_address": wallet_address,
            "email": email,
            "include": include,
            "conversion_status": conversion_status,
            "from": from_date,
            "to": to_date,
            "merchant_id": merchant_id,
            "limit": limit,
        })

    def withdraw(
        self,
        wallet_address: str,
        amount: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Request USDC withdrawal to wallet. Omit amount for full balance."""
        return self._call_tool("withdraw", {
            "wallet_address": wallet_address,
            "amount": amount,
        })

    def get_withdrawal_status(self, withdrawal_id: str) -> Dict[str, Any]:
        """Check withdrawal status by ID."""
        return self._call_tool("get_withdrawal_status", {
            "withdrawal_id": withdrawal_id,
        })


# ==================== CLI Interface ====================

def _print_json(data: Any) -> None:
    """Pretty-print JSON output."""
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw Laguna - Affiliate Commerce MCP Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # search-merchants
    sp = subparsers.add_parser("search-merchants", help="Search or browse affiliate merchants")
    sp.add_argument("--query", "-q", help="Fuzzy search query (min 2 chars)")
    sp.add_argument("--category", "-c", help="Category filter (e.g., travel, fashion)")
    sp.add_argument("--geo", "-g", help="ISO country code (e.g., SG, US)")
    sp.add_argument("--sort", "-s", choices=["relevance", "cashback_rate", "name"], help="Sort order")
    sp.add_argument("--limit", "-l", type=int, help="Max results (default 10, max 50)")

    # get-categories
    sp = subparsers.add_parser("get-categories", help="Browse merchant categories")
    sp.add_argument("--geo", "-g", help="ISO country code")

    # get-merchant-info
    sp = subparsers.add_parser("get-merchant-info", help="Get detailed merchant info")
    sp.add_argument("--merchant-id", "-m", required=True, help="Merchant slug (e.g., nike, trip-com)")
    sp.add_argument("--geo", "-g", help="ISO country code")

    # mint-link
    sp = subparsers.add_parser("mint-link", help="Create an affiliate tracking link")
    sp.add_argument("--merchant-id", "-m", required=True, help="Merchant slug")
    sp.add_argument("--wallet", "-w", help="Wallet address (EVM/TON/Solana)")
    sp.add_argument("--email", "-e", help="Email address (alternative to wallet)")
    sp.add_argument("--target-url", "-t", help="Deep link to specific product page")
    sp.add_argument("--geo", "-g", help="ISO country code")

    # get-dashboard
    sp = subparsers.add_parser("get-dashboard", help="View agent dashboard")
    sp.add_argument("--wallet", "-w", help="Wallet address")
    sp.add_argument("--email", "-e", help="Email address")
    sp.add_argument("--include", "-i", help="Sections: links,conversions,analytics (comma-separated)")
    sp.add_argument("--status", help="Filter conversions: pending/confirmed/paid/rejected")
    sp.add_argument("--from", dest="from_date", help="Start date (ISO 8601)")
    sp.add_argument("--to", dest="to_date", help="End date (ISO 8601)")
    sp.add_argument("--merchant-id", "-m", help="Filter by merchant slug")
    sp.add_argument("--limit", "-l", type=int, help="Max results (default 20, max 100)")

    # withdraw
    sp = subparsers.add_parser("withdraw", help="Request USDC withdrawal")
    sp.add_argument("--wallet", "-w", required=True, help="Wallet address")
    sp.add_argument("--amount", "-a", type=float, help="Amount in USDC (default: full balance)")

    # withdrawal-status
    sp = subparsers.add_parser("withdrawal-status", help="Check withdrawal status")
    sp.add_argument("--withdrawal-id", "-id", required=True, help="Withdrawal UUID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        client = LagunaClient()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.command == "search-merchants":
        result = client.search_merchants(
            query=args.query,
            category=args.category,
            geo=args.geo,
            sort=args.sort,
            limit=args.limit,
        )

    elif args.command == "get-categories":
        result = client.get_categories(geo=args.geo)

    elif args.command == "get-merchant-info":
        result = client.get_merchant_info(
            merchant_id=args.merchant_id,
            geo=args.geo,
        )

    elif args.command == "mint-link":
        if not args.wallet and not args.email:
            print("Error: --wallet or --email is required", file=sys.stderr)
            sys.exit(1)
        result = client.mint_link(
            merchant_id=args.merchant_id,
            wallet_address=args.wallet,
            email=args.email,
            target_url=args.target_url,
            geo=args.geo,
        )

    elif args.command == "get-dashboard":
        if not args.wallet and not args.email:
            print("Error: --wallet or --email is required", file=sys.stderr)
            sys.exit(1)
        include = args.include.split(",") if args.include else None
        result = client.get_dashboard(
            wallet_address=args.wallet,
            email=args.email,
            include=include,
            conversion_status=args.status,
            from_date=args.from_date,
            to_date=args.to_date,
            merchant_id=args.merchant_id,
            limit=args.limit,
        )

    elif args.command == "withdraw":
        result = client.withdraw(
            wallet_address=args.wallet,
            amount=args.amount,
        )

    elif args.command == "withdrawal-status":
        result = client.get_withdrawal_status(
            withdrawal_id=args.withdrawal_id,
        )

    else:
        parser.print_help()
        sys.exit(1)

    _print_json(result)

    if not result.get("success", False):
        sys.exit(1)


if __name__ == "__main__":
    main()
