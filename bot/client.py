import os
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from requests.exceptions import RequestException, ConnectionError, Timeout

logger = logging.getLogger("trading_bot")


class BinanceFuturesTestnetClient:
    def __init__(self, api_key: str = None, api_secret: str = None):
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")

        if not self.api_key or not self.api_secret:
            raise ValueError(
                "Missing API credentials. Set BINANCE_API_KEY and BINANCE_API_SECRET "
                "in your .env file, or pass them directly."
            )

        try:
            self.client = Client(self.api_key, self.api_secret, testnet=True)
            logger.debug("Binance Futures Testnet client initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize Binance client: {e}")
            raise

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None) -> dict:
        params = {
            "symbol": symbol,
            "side": side,
            "type": "STOP" if order_type == "STOP_LIMIT" else order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"

        if order_type == "STOP_LIMIT":
            params["price"] = price
            params["stopPrice"] = stop_price
            params["timeInForce"] = "GTC"

        logger.info(f"Order request: {params}")

        try:
            response = self.client.futures_create_order(**params)
            logger.info(f"Order response: {response}")
            return response

        except BinanceOrderException as e:
            logger.error(f"Order rejected by Binance: {e}")
            raise

        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e}")
            raise

        except (ConnectionError, Timeout) as e:
            logger.error(f"Network error while placing order: {e}")
            raise

        except RequestException as e:
            logger.error(f"Request error while placing order: {e}")
            raise