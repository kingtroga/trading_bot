import argparse
import sys

from bot.logging_config import setup_logging
from bot.orders import execute_order

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Ensure environment variables are set manually.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Simplified trading bot for Binance Futures Testnet (USDT-M)."
    )
    parser.add_argument("--symbol", required=True, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL", "buy", "sell"], help="Order side")
    parser.add_argument("--type", required=True, dest="order_type",
                         choices=["MARKET", "LIMIT", "STOP_LIMIT", "market", "limit", "stop_limit"],
                         help="Order type")
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument("--price", required=False, type=float, default=None,
                         help="Order price, required for LIMIT and STOP_LIMIT")
    parser.add_argument("--stop-price", required=False, type=float, default=None, dest="stop_price",
                         help="Trigger price, required for STOP_LIMIT")
    return parser


def main():
    logger = setup_logging()
    parser = build_parser()
    args = parser.parse_args()

    logger.debug(f"CLI args received: {vars(args)}")

    result = execute_order(
        symbol=args.symbol,
        side=args.side,
        order_type=args.order_type.upper(),
        quantity=args.quantity,
        price=args.price,
        stop_price=args.stop_price,
    )

    if result is None:
        sys.exit(1)


if __name__ == "__main__":
    main()