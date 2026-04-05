import json
import logging

from fastmcp import FastMCP
from pydantic import Field

from .service import KiteClient

logger = logging.getLogger("kite-mcp-server")


def register_tools(mcp: FastMCP) -> None:
    """Register all Kite Connect MCP tools."""

    @mcp.tool(
        name="kite_place_order",
        description="Place an order on Zerodha Kite. Supports market, limit, SL, and SL-M orders.",
    )
    async def kite_place_order(
        api_key: str = Field(..., description="Kite Connect API key"),
        access_token: str = Field(..., description="Access token from Kite login"),
        tradingsymbol: str = Field(
            ..., description="Trading symbol (e.g., 'INFY', 'RELIANCE')"
        ),
        exchange: str = Field(..., description="Exchange (NSE, BSE, NFO, MCX)"),
        transaction_type: str = Field(..., description="BUY or SELL"),
        quantity: int = Field(..., description="Number of shares/units", ge=1),
        order_type: str = Field(
            default="MARKET", description="MARKET, LIMIT, SL, SL-M"
        ),
        product: str = Field(
            default="MIS",
            description="MIS (intraday), CNC (delivery), NRML (overnight)",
        ),
        price: float = Field(default=None, description="Price for LIMIT orders", ge=0),
        validity: str = Field(default="DAY", description="DAY or IOC"),
        disclosed_quantity: int = Field(
            default=None, description="Disclosed quantity", ge=1
        ),
        trigger_price: float = Field(
            default=None, description="Trigger price for SL/SL-M orders", ge=0
        ),
        tag: str = Field(default=None, description="Tag for order tracking"),
    ) -> str:
        """Place an order."""
        try:
            client = KiteClient(api_key, access_token)
            result = client.place_order(
                tradingsymbol=tradingsymbol,
                exchange=exchange,
                transaction_type=transaction_type,
                quantity=quantity,
                order_type=order_type,
                product=product,
                price=price,
                validity=validity,
                disclosed_quantity=disclosed_quantity,
                trigger_price=trigger_price,
                tag=tag,
            )

            output = {
                "success": True,
                "order_id": result.get("order_id"),
                "status": result.get("status"),
                "message": f"Order placed successfully. Order ID: {result.get('order_id')}",
            }
            logger.info(f"Order placed: {result.get('order_id')} for {tradingsymbol}")
            return json.dumps(output, indent=2)
        except Exception as e:
            logger.error(f"Failed to place order: {e}", exc_info=True)
            return json.dumps({"success": False, "error": str(e)})

    @mcp.tool(
        name="kite_get_orders",
        description="Get all orders for the user. Returns order details including status, quantity, price.",
    )
    async def kite_get_orders(
        api_key: str = Field(..., description="Kite Connect API key"),
        access_token: str = Field(..., description="Access token from Kite login"),
    ) -> str:
        """Get all orders."""
        try:
            client = KiteClient(api_key, access_token)
            orders = client.get_orders()

            output = {
                "success": True,
                "count": len(orders),
                "orders": [
                    {
                        "order_id": o.get("order_id"),
                        "tradingsymbol": o.get("tradingsymbol"),
                        "status": o.get("status"),
                        "transaction_type": o.get("transaction_type"),
                        "quantity": o.get("quantity"),
                        "filled_quantity": o.get("filled_quantity"),
                        "average_price": o.get("average_price"),
                        "order_timestamp": o.get("order_timestamp"),
                    }
                    for o in orders
                ],
            }
            logger.info(f"Retrieved {len(orders)} orders")
            return json.dumps(output, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to get orders: {e}", exc_info=True)
            return json.dumps({"success": False, "error": str(e)})

    @mcp.tool(
        name="kite_cancel_order",
        description="Cancel an existing order by order ID.",
    )
    async def kite_cancel_order(
        api_key: str = Field(..., description="Kite Connect API key"),
        access_token: str = Field(..., description="Access token from Kite login"),
        order_id: str = Field(..., description="Order ID to cancel"),
        variety: str = Field(
            default="regular", description="Order variety (regular, co, amo, iceberg)"
        ),
    ) -> str:
        """Cancel an order."""
        try:
            client = KiteClient(api_key, access_token)
            result = client.cancel_order(order_id, variety=variety)

            output = {
                "success": True,
                "order_id": order_id,
                "status": result.get("status", "cancelled"),
                "message": f"Order {order_id} cancelled successfully",
            }
            logger.info(f"Order cancelled: {order_id}")
            return json.dumps(output, indent=2)
        except Exception as e:
            logger.error(f"Failed to cancel order {order_id}: {e}", exc_info=True)
            return json.dumps({"success": False, "error": str(e)})

    @mcp.tool(
        name="kite_get_positions",
        description="Get all positions (day and overnight) for the user.",
    )
    async def kite_get_positions(
        api_key: str = Field(..., description="Kite Connect API key"),
        access_token: str = Field(..., description="Access token from Kite login"),
    ) -> str:
        """Get positions."""
        try:
            client = KiteClient(api_key, access_token)
            positions = client.get_positions()

            output = {
                "success": True,
                "day_positions": [
                    {
                        "tradingsymbol": p.get("tradingsymbol"),
                        "quantity": p.get("quantity"),
                        "pnl": p.get("pnl"),
                        "buy_price": p.get("buy_price"),
                        "sell_price": p.get("sell_price"),
                    }
                    for p in positions.get("day", [])
                ],
                "net_positions": [
                    {
                        "tradingsymbol": p.get("tradingsymbol"),
                        "quantity": p.get("quantity"),
                        "pnl": p.get("pnl"),
                        "unrealised": p.get("unrealised"),
                        "m2m": p.get("m2m"),
                    }
                    for p in positions.get("net", [])
                ],
            }
            logger.info(
                f"Retrieved positions: {len(output['day_positions'])} day, {len(output['net_positions'])} net"
            )
            return json.dumps(output, indent=2)
        except Exception as e:
            logger.error(f"Failed to get positions: {e}", exc_info=True)
            return json.dumps({"success": False, "error": str(e)})

    @mcp.tool(
        name="kite_get_holdings",
        description="Get all holdings (delivery portfolio) for the user.",
    )
    async def kite_get_holdings(
        api_key: str = Field(..., description="Kite Connect API key"),
        access_token: str = Field(..., description="Access token from Kite login"),
    ) -> str:
        """Get holdings."""
        try:
            client = KiteClient(api_key, access_token)
            holdings = client.get_holdings()

            output = {
                "success": True,
                "count": len(holdings),
                "holdings": [
                    {
                        "tradingsymbol": h.get("tradingsymbol"),
                        "quantity": h.get("quantity"),
                        "average_price": h.get("average_price"),
                        "last_price": h.get("last_price"),
                        "pnl": h.get("pnl"),
                        "day_change_percentage": h.get("day_change_percentage"),
                    }
                    for h in holdings
                ],
            }
            logger.info(f"Retrieved {len(holdings)} holdings")
            return json.dumps(output, indent=2)
        except Exception as e:
            logger.error(f"Failed to get holdings: {e}", exc_info=True)
            return json.dumps({"success": False, "error": str(e)})

    @mcp.tool(
        name="kite_get_quote",
        description="Get real-time market quotes for one or more instruments.",
    )
    async def kite_get_quote(
        api_key: str = Field(..., description="Kite Connect API key"),
        access_token: str = Field(..., description="Access token from Kite login"),
        instruments: str = Field(
            ...,
            description="Comma-separated instrument tokens or symbols (e.g., 'NSE:INFY,NSE:RELIANCE')",
        ),
    ) -> str:
        """Get market quotes."""
        try:
            client = KiteClient(api_key, access_token)
            instrument_list = [i.strip() for i in instruments.split(",")]
            quotes = client.get_quote(instrument_list)

            output = {"success": True, "count": len(quotes), "quotes": {}}

            for symbol, data in quotes.items():
                output["quotes"][symbol] = {
                    "last_price": data.get("last_price"),
                    "volume": data.get("volume"),
                    "change": data.get("net_change"),
                    "upper_circuit": data.get("upper_circuit_limit"),
                    "lower_circuit": data.get("lower_circuit_limit"),
                    "timestamp": data.get("timestamp"),
                }

            logger.info(f"Retrieved quotes for {len(quotes)} instruments")
            return json.dumps(output, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to get quotes: {e}", exc_info=True)
            return json.dumps({"success": False, "error": str(e)})

    @mcp.tool(
        name="kite_get_profile",
        description="Get user profile information including name, email, phone, and exchange access.",
    )
    async def kite_get_profile(
        api_key: str = Field(..., description="Kite Connect API key"),
        access_token: str = Field(..., description="Access token from Kite login"),
    ) -> str:
        """Get user profile."""
        try:
            client = KiteClient(api_key, access_token)
            profile = client.get_profile()

            output = {
                "success": True,
                "user_id": profile.get("user_id"),
                "user_name": profile.get("user_name"),
                "user_type": profile.get("user_type"),
                "email": profile.get("email"),
                "phone": profile.get("phone"),
                "exchanges": profile.get("exchanges"),
                "products": profile.get("products"),
                "order_types": profile.get("order_types"),
            }
            logger.info(f"Retrieved profile for user: {profile.get('user_id')}")
            return json.dumps(output, indent=2)
        except Exception as e:
            logger.error(f"Failed to get profile: {e}", exc_info=True)
            return json.dumps({"success": False, "error": str(e)})

    @mcp.tool(
        name="kite_get_margins",
        description="Get user margins (available, utilized, and total).",
    )
    async def kite_get_margins(
        api_key: str = Field(..., description="Kite Connect API key"),
        access_token: str = Field(..., description="Access token from Kite login"),
    ) -> str:
        """Get margins."""
        try:
            client = KiteClient(api_key, access_token)
            margins = client.get_margins()

            output = {
                "success": True,
                "equity": margins.get("equity"),
                "commodity": margins.get("commodity"),
            }
            logger.info("Retrieved margins")
            return json.dumps(output, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to get margins: {e}", exc_info=True)
            return json.dumps({"success": False, "error": str(e)})

    @mcp.tool(
        name="kite_get_historical_data",
        description="Get historical candlestick data for an instrument.",
    )
    async def kite_get_historical_data(
        api_key: str = Field(..., description="Kite Connect API key"),
        access_token: str = Field(..., description="Access token from Kite login"),
        instrument_token: str = Field(
            ...,
            description="Instrument token (use kite_get_instruments to find tokens)",
        ),
        from_date: str = Field(..., description="Start date (YYYY-MM-DD)"),
        to_date: str = Field(..., description="End date (YYYY-MM-DD)"),
        interval: str = Field(
            default="day",
            description="Interval: minute, day, 5minute, 15minute, 30minute, 60minute",
        ),
    ) -> str:
        """Get historical data."""
        try:
            client = KiteClient(api_key, access_token)
            data = client.get_historical_data(
                instrument_token=instrument_token,
                from_date=from_date,
                to_date=to_date,
                interval=interval,
            )

            output = {
                "success": True,
                "count": len(data),
                "interval": interval,
                "data": data[:100] if len(data) > 100 else data,  # Limit to 100 candles
            }
            logger.info(
                f"Retrieved {len(data)} candles for instrument {instrument_token}"
            )
            return json.dumps(output, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to get historical data: {e}", exc_info=True)
            return json.dumps({"success": False, "error": str(e)})

    @mcp.tool(
        name="kite_get_instruments",
        description="Get list of all instruments or filter by exchange.",
    )
    async def kite_get_instruments(
        api_key: str = Field(..., description="Kite Connect API key"),
        access_token: str = Field(..., description="Access token from Kite login"),
        exchange: str = Field(
            default=None, description="Filter by exchange (NSE, BSE, NFO, MCX, CDS)"
        ),
        limit: int = Field(
            default=100,
            description="Maximum number of instruments to return",
            ge=1,
            le=1000,
        ),
    ) -> str:
        """Get instrument list."""
        try:
            client = KiteClient(api_key, access_token)
            instruments = client.get_instruments(exchange=exchange)

            # Limit results
            if limit and len(instruments) > limit:
                instruments = instruments[:limit]

            output = {
                "success": True,
                "count": len(instruments),
                "exchange": exchange,
                "instruments": [
                    {
                        "tradingsymbol": i.get("tradingsymbol"),
                        "instrument_token": i.get("instrument_token"),
                        "exchange": i.get("exchange"),
                        "segment": i.get("segment"),
                        "name": i.get("name"),
                    }
                    for i in instruments
                ],
            }
            logger.info(f"Retrieved {len(instruments)} instruments")
            return json.dumps(output, indent=2)
        except Exception as e:
            logger.error(f"Failed to get instruments: {e}", exc_info=True)
            return json.dumps({"success": False, "error": str(e)})

    @mcp.tool(
        name="kite_health_check",
        description="Check server readiness and basic connectivity.",
    )
    def kite_health_check() -> str:
        """Health check endpoint."""
        return json.dumps(
            {
                "status": "ok",
                "server": "CL Kite Connect MCP Server",
                "type": "third-party-integration",
                "auth_required": True,
                "supports": [
                    "orders",
                    "positions",
                    "holdings",
                    "quotes",
                    "historical_data",
                ],
            }
        )
