# Kite Connect MCP Server

A Model Context Protocol (MCP) server that exposes Zerodha Kite Connect API for algorithmic trading, portfolio management, and market data access.

---

## Overview

The Kite Connect MCP Server provides stateless, multi-tenant access to Zerodha's trading platform:

- **Order Management** — Place, modify, cancel, and track orders
- **Portfolio Management** — View positions, holdings, and margins
- **Market Data** — Real-time quotes and historical candlestick data
- **User Profile** — Account information and exchange access

Perfect for:

- Algorithmic trading strategies
- Portfolio monitoring and rebalancing
- Market data analysis and backtesting
- Automated order execution

---

## Tools

<details>
<summary><code>kite_place_order</code> — Place buy/sell orders</summary>

Place market, limit, SL, or SL-M orders on NSE, BSE, NFO, or MCX.

**Inputs:**

- `api_key` (string, required) — Kite Connect API key
- `access_token` (string, required) — Access token from Kite login
- `tradingsymbol` (string, required) — Trading symbol (e.g., "INFY", "RELIANCE")
- `exchange` (string, required) — Exchange (NSE, BSE, NFO, MCX, CDS)
- `transaction_type` (string, required) — BUY or SELL
- `quantity` (integer, required) — Number of shares/units (≥1)
- `order_type` (string, optional) — MARKET, LIMIT, SL, SL-M (default: MARKET)
- `product` (string, optional) — MIS (intraday), CNC (delivery), NRML (overnight)
- `price` (float, optional) — Price for LIMIT orders
- `validity` (string, optional) — DAY or IOC (default: DAY)
- `disclosed_quantity` (integer, optional) — Disclosed quantity (≤ quantity)
- `trigger_price` (float, optional) — Trigger price for SL/SL-M orders
- `tag` (string, optional) — Custom tag for order tracking

**Output:**

```json
{
  "success": true,
  "order_id": "1234567890",
  "status": "placed",
  "message": "Order placed successfully. Order ID: 1234567890"
}