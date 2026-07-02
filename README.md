# Trading Bot (Binance Futures Testnet)

A simple Python CLI application that places MARKET, LIMIT, and STOP_LIMIT orders on Binance Futures Testnet (USDT-M), with structured code, logging, and input validation.

## Project Structure

trading_bot/
  bot/
    __init__.py
    client.py
    orders.py
    validators.py
    logging_config.py
  cli.py
  logs/
  README.md
  requirements.txt

## Setup

1. Register on Binance Futures Testnet: https://testnet.binancefuture.com 
2. Generate an API key and secret with futures trading permission enabled
3. Clone this repo, then create and activate a virtual environment:

   python -m venv .venv
   .venv\Scripts\activate

4. Install dependencies:

   pip install -r requirements.txt

5. Create a `.env` file in the project root:

   BINANCE_API_KEY=your_api_key_here
   BINANCE_API_SECRET=your_api_secret_here

## How to Run

Place a MARKET order:

   python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

Place a LIMIT order:

   python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 60000

Place a STOP_LIMIT order:

   python cli.py --symbol BTCUSDT --side SELL --type STOP_LIMIT --quantity 0.01 --price 60000 --stop-price 59500

Logs for every request and response are written to `logs/trading_bot.log`.

## Assumptions

- MARKET, LIMIT, and STOP_LIMIT order types are implemented. STOP_LIMIT is included as a bonus beyond the core requirement of MARKET and LIMIT.
- Quantity and price validation is handled locally before hitting the API. Exchange-side rules, such as minimum price bands or lot size, are surfaced through the API error and logged, not pre-validated locally.
- Credentials are loaded from a `.env` file rather than passed as CLI flags, to avoid secrets in shell history or process lists.
- Tested against Binance Futures Testnet (USDT-M) only, not mainnet.
- Order status may show as NEW rather than FILLED on testnet, since the testnet matching engine does not always fill immediately. Request and response logging still confirm correctness of the API interaction.

## Error Handling

The app handles and logs:
- Invalid CLI input (bad symbol, side, order type, missing price for LIMIT or STOP_LIMIT)
- Missing or invalid API credentials
- Binance API errors (for example, price outside allowed band, invalid quantity)
- Network or connection failures