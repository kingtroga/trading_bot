VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_LIMIT"}


class ValidationError(Exception):
    pass


def validate_symbol(symbol: str) -> str:
    if not symbol or not symbol.isalnum():
        raise ValidationError(f"Invalid symbol: '{symbol}'. Expected format like 'BTCUSDT'.")
    return symbol.upper()


def validate_side(side: str) -> str:
    side = side.upper()
    if side not in VALID_SIDES:
        raise ValidationError(f"Invalid side: '{side}'. Must be one of {VALID_SIDES}.")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError(f"Invalid order type: '{order_type}'. Must be one of {VALID_ORDER_TYPES}.")
    return order_type


def validate_quantity(quantity: float) -> float:
    if quantity is None or quantity <= 0:
        raise ValidationError(f"Invalid quantity: '{quantity}'. Must be a positive number.")
    return quantity


def validate_price(price, order_type: str):
    if order_type in ("LIMIT", "STOP_LIMIT"):
        if price is None or price <= 0:
            raise ValidationError(f"Price is required and must be positive for {order_type} orders.")
    return price


def validate_stop_price(stop_price, order_type: str):
    if order_type == "STOP_LIMIT":
        if stop_price is None or stop_price <= 0:
            raise ValidationError("Stop price is required and must be positive for STOP_LIMIT orders.")
    return stop_price


def validate_order_input(symbol: str, side: str, order_type: str, quantity: float, price=None, stop_price=None) -> dict:
    clean_symbol = validate_symbol(symbol)
    clean_side = validate_side(side)
    clean_order_type = validate_order_type(order_type)
    clean_quantity = validate_quantity(quantity)
    clean_price = validate_price(price, clean_order_type)
    clean_stop_price = validate_stop_price(stop_price, clean_order_type)

    return {
        "symbol": clean_symbol,
        "side": clean_side,
        "order_type": clean_order_type,
        "quantity": clean_quantity,
        "price": clean_price,
        "stop_price": clean_stop_price,
    }