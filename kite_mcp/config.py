import logging

# Kite Connect API Configuration
KITE_API_BASE = "https://api.kite.trade"
KITE_LOGIN_URL = "https://kite.zerodha.com/connect/login"

# API Endpoints (for reference)
KITE_ORDERS_ENDPOINT = f"{KITE_API_BASE}/orders"
KITE_POSITIONS_ENDPOINT = f"{KITE_API_BASE}/portfolio/positions"
KITE_HOLDINGS_ENDPOINT = f"{KITE_API_BASE}/portfolio/holdings"
KITE_MARGINS_ENDPOINT = f"{KITE_API_BASE}/user/margins"

# Default values
DEFAULT_EXCHANGE = "NSE"
DEFAULT_PRODUCT = "MIS"  # Margin Intraday Squareoff
DEFAULT_VARIETY = "regular"
DEFAULT_TRANSACTION_TYPE = "BUY"

# Exchange mapping
EXCHANGES = {
    "NSE": "NSE",
    "BSE": "BSE",
    "NFO": "NFO",  # Futures & Options
    "CDS": "CDS",  # Currency Derivatives
    "MCX": "MCX",  # Commodity
}


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
