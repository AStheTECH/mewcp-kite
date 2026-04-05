from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


class OrderRequest(TypedDict, total=False):
    """Order request parameters."""

    tradingsymbol: str
    exchange: str
    transaction_type: str  # BUY or SELL
    quantity: int
    price: Optional[float]
    order_type: str  # MARKET, LIMIT, SL, SL-M
    product: str  # MIS, CNC, NRML
    variety: str  # regular, co, amo, iceberg
    validity: str  # DAY, IOC
    disclosed_quantity: Optional[int]
    trigger_price: Optional[float]
    squareoff_value: Optional[float]
    stoploss_value: Optional[float]
    trailing_stoploss: Optional[float]
    tag: Optional[str]


class OrderInfo(TypedDict):
    """Order information from Kite."""

    order_id: str
    order_tag: Optional[str]
    exchange_order_id: Optional[str]
    tradingsymbol: str
    status: str
    status_message: Optional[str]
    order_timestamp: str
    exchange_timestamp: Optional[str]
    quantity: int
    filled_quantity: int
    pending_quantity: int
    price: float
    average_price: float
    transaction_type: str
    order_type: str
    product: str
    variety: str


class Position(TypedDict):
    """Position information."""

    tradingsymbol: str
    exchange: str
    quantity: int
    overnight_quantity: int
    multiplier: float
    product: str
    day_buy_quantity: float
    day_buy_price: float
    day_sell_quantity: float
    day_sell_price: float
    buy_price: float
    sell_price: float
    buy_quantity: int
    sell_quantity: int
    pnl: float
    net_value: float
    buy_m2m: float
    sell_m2m: float
    m2m: float
    unrealised: float
    realised: float


class Holding(TypedDict):
    """Holding information."""

    tradingsymbol: str
    exchange: str
    isin: str
    t1_quantity: int
    realised_quantity: int
    authorised_quantity: int
    quantity: int
    average_price: float
    last_price: float
    close_price: float
    pnl: float
    day_change: float
    day_change_percentage: float


class Quote(TypedDict):
    """Market quote information."""

    tradingsymbol: str
    exchange: str
    mode: str
    last_price: float
    last_quantity: int
    last_trade_time: str
    oi: int
    oi_day_high: int
    oi_day_low: int
    net_change: float
    volume: int
    average_price: float
    buy_quantity: int
    sell_quantity: int
    upper_circuit_limit: float
    lower_circuit_limit: float
    timestamp: str
    depth: Dict[str, Any]


class Profile(TypedDict):
    """User profile information."""

    user_id: str
    user_name: str
    user_type: str
    email: str
    phone: str
    broker: str
    exchanges: List[str]
    products: List[str]
    order_types: List[str]
    avatar_url: Optional[str]
