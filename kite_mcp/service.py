import logging
from typing import Any, Dict, List, Optional

from fastmcp_credentials import get_credentials
from kiteconnect import KiteConnect

logger = logging.getLogger("kite-mcp-server")


def get_kite_client() -> "KiteClient":
    cred = get_credentials()
    api_key = cred.fields.get("api_key")
    access_token = cred.fields.get("access_token")
    if not api_key:
        raise ValueError("No 'api_key' found in credentials")
    if not access_token:
        raise ValueError("No 'access_token' found in credentials")
    return KiteClient(api_key=api_key, access_token=access_token)


class KiteClient:
    """Client for Zerodha Kite Connect API."""

    def __init__(self, api_key: str, access_token: str):
        """Initialize Kite Connect client.

        Args:
            api_key: Kite Connect API key
            access_token: Access token obtained after login
        """
        self.api_key = api_key
        self.access_token = access_token
        self.kite = KiteConnect(api_key=api_key)
        self.kite.set_access_token(access_token)

    # Orders

    def place_order(
        self,
        tradingsymbol: str,
        exchange: str,
        transaction_type: str,
        quantity: int,
        order_type: str = "MARKET",
        product: str = "MIS",
        price: Optional[float] = None,
        validity: str = "DAY",
        disclosed_quantity: Optional[int] = None,
        trigger_price: Optional[float] = None,
        squareoff_value: Optional[float] = None,
        stoploss_value: Optional[float] = None,
        trailing_stoploss: Optional[float] = None,
        tag: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Place an order."""
        params = {
            "tradingsymbol": tradingsymbol,
            "exchange": exchange,
            "transaction_type": transaction_type,
            "quantity": quantity,
            "order_type": order_type,
            "product": product,
            "validity": validity,
        }

        if price is not None:
            params["price"] = price
        if disclosed_quantity is not None:
            params["disclosed_quantity"] = disclosed_quantity
        if trigger_price is not None:
            params["trigger_price"] = trigger_price
        if squareoff_value is not None:
            params["squareoff_value"] = squareoff_value
        if stoploss_value is not None:
            params["stoploss_value"] = stoploss_value
        if trailing_stoploss is not None:
            params["trailing_stoploss"] = trailing_stoploss
        if tag is not None:
            params["tag"] = tag

        order_id = self.kite.place_order(**params)
        return {"order_id": order_id, "status": "placed"}

    def get_orders(self) -> List[Dict[str, Any]]:
        """Get all orders."""
        return self.kite.orders()

    def get_order(self, order_id: str) -> Dict[str, Any]:
        """Get order details."""
        return self.kite.order(order_id)

    def modify_order(
        self,
        order_id: str,
        quantity: Optional[int] = None,
        price: Optional[float] = None,
        order_type: Optional[str] = None,
        trigger_price: Optional[float] = None,
        validity: Optional[str] = None,
        disclosed_quantity: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Modify an existing order."""
        params = {"order_id": order_id}
        if quantity is not None:
            params["quantity"] = quantity
        if price is not None:
            params["price"] = price
        if order_type is not None:
            params["order_type"] = order_type
        if trigger_price is not None:
            params["trigger_price"] = trigger_price
        if validity is not None:
            params["validity"] = validity
        if disclosed_quantity is not None:
            params["disclosed_quantity"] = disclosed_quantity

        order_id = self.kite.modify_order(**params)
        return {"order_id": order_id, "status": "modified"}

    def cancel_order(self, order_id: str, variety: str = "regular") -> Dict[str, Any]:
        """Cancel an order."""
        self.kite.cancel_order(order_id, variety=variety)
        return {"order_id": order_id, "status": "cancelled"}

    # Positions

    def get_positions(self) -> Dict[str, Any]:
        """Get all positions."""
        return self.kite.positions()

    # Holdings

    def get_holdings(self) -> List[Dict[str, Any]]:
        """Get all holdings."""
        return self.kite.holdings()

    # Market Data

    def get_quote(self, instruments: List[str]) -> Dict[str, Any]:
        """Get market quotes for instruments."""
        return self.kite.quote(instruments)

    def get_historical_data(
        self,
        instrument_token: str,
        from_date: str,
        to_date: str,
        interval: str = "day",
        continuous: bool = False,
        oi: bool = False,
    ) -> List[Dict[str, Any]]:
        """Get historical data for an instrument."""
        return self.kite.historical_data(
            instrument_token=instrument_token,
            from_date=from_date,
            to_date=to_date,
            interval=interval,
            continuous=continuous,
            oi=oi,
        )

    def get_instruments(self, exchange: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get instrument list."""
        instruments = self.kite.instruments()
        if exchange:
            instruments = [i for i in instruments if i["exchange"] == exchange]
        return instruments

    # Profile

    def get_profile(self) -> Dict[str, Any]:
        """Get user profile."""
        return self.kite.profile()

    def get_margins(self) -> Dict[str, Any]:
        """Get user margins."""
        return self.kite.margins()
