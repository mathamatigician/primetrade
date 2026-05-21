# Binance Futures Testnet Trading Bot

Small Python CLI application for placing MARKET and LIMIT orders on Binance USDT-M Futures Testnet.

## Setup

1. Create and activate a Binance Futures Testnet account.
2. Generate API credentials.
3. Create and activate a virtual environment


4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create a `.env` file from the example:

```bash
cp .env.example .env
```

6. Add your Binance Futures Testnet credentials to `.env`.

The default API base URL is `https://testnet.binancefuture.com`.

## Run Examples

Market order:

```bash
python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

Limit order:

```bash
python -m bot.cli --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 120000
```

## Tests

To run test, execute the following:

```bash
docker run --rm --entrypoint python tradebot -m unittest discover -s tests
```

## Docker

Build the image:

```bash
docker build -t binance-futures-bot .
```

Run a market order:

```bash
docker run --rm `
  --env-file .env `
  -v "${PWD}\logs:/app/logs" `
  binance-futures-bot --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

Run a limit order:

```bash
docker run --rm `
  --env-file .env `
  -v "${PWD}\logs:/app/logs" `
  binance-futures-bot --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 120000
```

## Logs

The app writes API requests, responses, and errors to:

```text
logs/trading_bot.log
```

Submit log output from at least one MARKET order and one LIMIT order with the assignment.

## Assumptions

- This project uses direct REST calls through Python's standard library.
- Only USDT-M Futures Testnet symbols are accepted.
- LIMIT orders use `timeInForce=GTC`.
- API credentials are loaded from `.env` using `python-dotenv`; real environment variables also work.
