**Trade smarter with Zerodha Kite — orders, positions, holdings, and live market data via MCP.**

A Model Context Protocol (MCP) server that exposes Zerodha Kite Connect's API for trading, portfolio management, and market data retrieval.


## Overview

The Kite Connect MCP Server provides full access to Zerodha's trading platform:

- Place, modify, and cancel equity and derivatives orders
- Fetch real-time quotes, historical candlestick data, and instrument lists
- Monitor positions, holdings, margins, and user profile

Perfect for:

- Automating trading workflows through an AI assistant
- Building portfolio monitoring and analysis pipelines
- Querying live and historical market data programmatically


## Tools

<details>
<summary><code>kite_place_order</code> — Place an order on Zerodha Kite</summary>

Place a market, limit, SL, or SL-M order for any NSE/BSE/NFO/MCX instrument.

**Inputs:**
```
- `tradingsymbol` (string, required) — Trading symbol (e.g., 'INFY', 'RELIANCE')
- `exchange` (string, required) — Exchange: NSE, BSE, NFO, MCX
- `transaction_type` (string, required) — BUY or SELL
- `quantity` (integer, required) — Number of shares/units (min 1)
- `order_type` (string, optional) — MARKET, LIMIT, SL, SL-M (default: MARKET)
- `product` (string, optional) — MIS (intraday), CNC (delivery), NRML (overnight) (default: MIS)
- `price` (float, optional) — Price for LIMIT orders
- `validity` (string, optional) — DAY or IOC (default: DAY)
- `disclosed_quantity` (integer, optional) — Disclosed quantity
- `trigger_price` (float, optional) — Trigger price for SL/SL-M orders
- `tag` (string, optional) — Tag for order tracking
```

**Output:**
```json
{
  "success": true,
  "order_id": "230914000012345",
  "status": "placed",
  "message": "Order placed successfully. Order ID: 230914000012345"
}
```

</details>


<details>
<summary><code>kite_get_orders</code> — Get all orders for the user</summary>

Returns all orders for the session including status, quantity, price, and timestamps.

**Inputs:**
```
(none)
```

**Output:**
```json
{
  "success": true,
  "count": 2,
  "orders": [
    {
      "order_id": "230914000012345",
      "tradingsymbol": "INFY",
      "status": "COMPLETE",
      "transaction_type": "BUY",
      "quantity": 10,
      "filled_quantity": 10,
      "average_price": 1452.5,
      "order_timestamp": "2023-09-14 10:32:00"
    }
  ]
}
```

</details>


<details>
<summary><code>kite_cancel_order</code> — Cancel an existing order</summary>

Cancel a pending order by its order ID.

**Inputs:**
```
- `order_id` (string, required) — Order ID to cancel
- `variety` (string, optional) — Order variety: regular, co, amo, iceberg (default: regular)
```

**Output:**
```json
{
  "success": true,
  "order_id": "230914000012345",
  "status": "cancelled",
  "message": "Order 230914000012345 cancelled successfully"
}
```

</details>


<details>
<summary><code>kite_get_positions</code> — Get all open positions</summary>

Returns day and net positions with P&L, buy/sell prices, and M2M values.

**Inputs:**
```
(none)
```

**Output:**
```json
{
  "success": true,
  "day_positions": [
    { "tradingsymbol": "INFY", "quantity": 10, "pnl": 250.0, "buy_price": 1450.0, "sell_price": 0.0 }
  ],
  "net_positions": [
    { "tradingsymbol": "INFY", "quantity": 10, "pnl": 250.0, "unrealised": 250.0, "m2m": 250.0 }
  ]
}
```

</details>


<details>
<summary><code>kite_get_holdings</code> — Get delivery portfolio holdings</summary>

Returns all long-term holdings with average price, last price, and P&L.

**Inputs:**
```
(none)
```

**Output:**
```json
{
  "success": true,
  "count": 3,
  "holdings": [
    {
      "tradingsymbol": "RELIANCE",
      "quantity": 5,
      "average_price": 2400.0,
      "last_price": 2520.0,
      "pnl": 600.0,
      "day_change_percentage": 0.85
    }
  ]
}
```

</details>


<details>
<summary><code>kite_get_quote</code> — Get real-time market quotes</summary>

Fetch live quotes for one or more instruments including last price, volume, and circuit limits.

**Inputs:**
```
- `instruments` (string, required) — Comma-separated instrument symbols (e.g., 'NSE:INFY,NSE:RELIANCE')
```

**Output:**
```json
{
  "success": true,
  "count": 1,
  "quotes": {
    "NSE:INFY": {
      "last_price": 1452.5,
      "volume": 1234567,
      "change": 12.5,
      "upper_circuit": 1597.75,
      "lower_circuit": 1307.25,
      "timestamp": "2023-09-14 15:29:59"
    }
  }
}
```

</details>


<details>
<summary><code>kite_get_historical_data</code> — Get historical candlestick data</summary>

Fetch OHLCV candlestick data for any instrument over a date range and interval. Returns up to 100 candles.

**Inputs:**
```
- `instrument_token` (string, required) — Instrument token (use kite_get_instruments to find tokens)
- `from_date` (string, required) — Start date (YYYY-MM-DD)
- `to_date` (string, required) — End date (YYYY-MM-DD)
- `interval` (string, optional) — minute, day, 5minute, 15minute, 30minute, 60minute (default: day)
```

**Output:**
```json
{
  "success": true,
  "count": 5,
  "interval": "day",
  "data": [
    { "date": "2023-09-14", "open": 1440.0, "high": 1460.0, "low": 1435.0, "close": 1452.5, "volume": 1234567 }
  ]
}
```

</details>


<details>
<summary><code>kite_get_instruments</code> — Get tradable instrument list</summary>

Returns instruments available for trading, optionally filtered by exchange. Returns up to 1000 results.

**Inputs:**
```
- `exchange` (string, optional) — Filter by exchange: NSE, BSE, NFO, MCX, CDS
- `limit` (integer, optional) — Maximum results to return, 1–1000 (default: 100)
```

**Output:**
```json
{
  "success": true,
  "count": 100,
  "exchange": "NSE",
  "instruments": [
    { "tradingsymbol": "INFY", "instrument_token": "408065", "exchange": "NSE", "segment": "NSE", "name": "INFOSYS" }
  ]
}
```

</details>


<details>
<summary><code>kite_get_profile</code> — Get user profile</summary>

Returns the authenticated user's profile including name, email, phone, and enabled exchanges and products.

**Inputs:**
```
(none)
```

**Output:**
```json
{
  "success": true,
  "user_id": "AB1234",
  "user_name": "John Doe",
  "user_type": "individual",
  "email": "john@example.com",
  "phone": "9876543210",
  "exchanges": ["NSE", "BSE", "NFO"],
  "products": ["CNC", "MIS", "NRML"],
  "order_types": ["MARKET", "LIMIT", "SL", "SL-M"]
}
```

</details>


<details>
<summary><code>kite_get_margins</code> — Get account margins</summary>

Returns available, utilized, and total margins for equity and commodity segments.

**Inputs:**
```
(none)
```

**Output:**
```json
{
  "success": true,
  "equity": { "available": { "cash": 50000.0 }, "utilised": { "debits": 12000.0 } },
  "commodity": { "available": { "cash": 10000.0 }, "utilised": { "debits": 0.0 } }
}
```

</details>


<details>
<summary><code>kite_health_check</code> — Check server readiness</summary>

Returns server status and supported capability list. Does not require credentials.

**Inputs:**
```
(none)
```

**Output:**
```json
{
  "status": "ok",
  "server": "CL Kite Connect MCP Server",
  "type": "third-party-integration",
  "auth_required": true,
  "supports": ["orders", "positions", "holdings", "quotes", "historical_data"]
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Order Types</strong></summary>

- `MARKET` — Execute immediately at the best available price
- `LIMIT` — Execute at a specified price or better; requires `price`
- `SL` — Stop-loss limit order; requires both `trigger_price` and `price`
- `SL-M` — Stop-loss market order; requires `trigger_price` only

</details>

<details>
<summary><strong>Product Codes</strong></summary>

- `MIS` — Margin Intraday Square-off; must be closed before market end
- `CNC` — Cash and Carry; for delivery/long-term holding
- `NRML` — Normal; for overnight F&O positions

</details>

<details>
<summary><strong>Instrument Token</strong></summary>

**Finding a token:**
```
Use kite_get_instruments with the exchange filter, then read the instrument_token field.
Example: { "tradingsymbol": "INFY", "instrument_token": "408065", "exchange": "NSE" }
```

**Quote symbol format:**
```
{EXCHANGE}:{TRADINGSYMBOL}
Example: NSE:INFY
```

</details>


## Getting Your Kite Connect Credentials

<details>
<summary><strong>Steps</strong></summary>

1. Go to [Kite Connect Developer Console](https://developers.kite.trade/)
2. Create an app to get your **API Key** and **API Secret**
3. Complete the login flow to obtain an **Access Token** (valid for one trading day)
4. Both `api_key` and `access_token` are required — provide them as static credential fields

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** Credentials not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_API_KEY` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check that the credential is active in your MewCP account

</details>

<details>
<summary><strong>Insufficient Credits</strong></summary>

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No Kite Connect credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Add your Kite Connect `api_key` and `access_token` as a static credential
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check parameter types match expected values

</details>

<details>
<summary><strong>Server Not Found</strong></summary>

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `{server-name}/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>Kite Connect API Error</strong></summary>

- **Cause:** Upstream Kite Connect API returned an error
- **Solution:**
  1. Check Kite Connect service status at [Kite Status Page](https://status.zerodha.com/)
  2. Verify your access token is valid and not expired (tokens expire at end of trading day)
  3. Review the error message for specific details

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[Kite Connect API Documentation](https://kite.trade/docs/connect/v3/)** — Official API reference
- **[Kite Connect API Reference](https://kite.trade/docs/connect/v3/user/)** — Complete endpoint reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling

</details>
