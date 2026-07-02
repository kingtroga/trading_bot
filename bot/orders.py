import logging
from bot.validators import validate_order_input, ValidationError
from bot.client import BinanceFuturesTestnetClient

logger = logging.getLogger("trading_bot")


def print_order_summary(params: dict):
    print("\nOrder Request Summary")
    print("----------------------")
    for key, value in params.items():
        if value is not None:
            print(f"{key}: {value}")
    print()


def print_order_result(response: dict):
    print("Order Response")
    print("---------------")
    print(f"orderId:      {response.get('orderId')}")
    print(f"status:       {response.get('status')}")
    print(f"executedQty:  {response.get('executedQty')}")
    avg_price = response.get('avgPrice')
    if avg_price:
        print(f"avgPrice:     {avg_price}")
    print()


def execute_order(symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
    try:
        params = validate_order_input(symbol, side, order_type, quantity, price, stop_price)
    except ValidationError as e:
        logger.error(f"Validation failed: {e}")
        print(f"Input error: {e}")
        return None

    print_order_summary(params)

    try:
        client = BinanceFuturesTestnetClient()
    except ValueError as e:
        logger.error(f"Client setup failed: {e}")
        print(f"Setup error: {e}")
        return None

    try:
        response = client.place_order(
            symbol=params["symbol"],
            side=params["side"],
            order_type=params["order_type"],
            quantity=params["quantity"],
            price=params["price"],
            stop_price=params["stop_price"],
        )
        print_order_result(response)
        print("Order placed successfully.\n")
        return response

    except Exception as e:
        print(f"Order failed: {e}\n")
        return None