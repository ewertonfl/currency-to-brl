# Currency to BRL

A simple Python script that fetches current exchange rates from AwesomeAPI and returns currency conversion values to Brazilian Real in JSON format.

The project was created to quickly compare exchange rates from USD and selected LATAM currencies against BRL, including both conversion directions:

```txt
1 foreign currency = X BRL
1 BRL = X foreign currency
```

## Supported countries and currencies

| Country | Currency | Pair |
|---|---:|---:|
| United States | USD | USD-BRL |
| Argentina | ARS | ARS-BRL |
| Colombia | COP | COP-BRL |
| Peru | PEN | PEN-BRL |
| Ecuador | USD | USD-BRL |
| Bolivia | BOB | BOB-BRL |
| Mexico | MXN | MXN-BRL |
| Paraguay | PYG | PYG-BRL |
| Chile | CLP | CLP-BRL |

> Note: Ecuador uses USD as its official currency.

## What this script does

The script:

- Reads an AwesomeAPI key from the `.env` file.
- Requests the latest exchange rates from AwesomeAPI.
- Converts the returned values into a clean JSON structure.
- Returns both exchange directions:
  - foreign currency to BRL
  - BRL to foreign currency
- Includes bid, ask, high, low, variation, percentage variation, quote date, and timestamp.

## Requirements

- Python 3.10+
- An AwesomeAPI API key

## Create an AwesomeAPI key

Create your free AwesomeAPI key using the official documentation:

https://docs.awesomeapi.com.br/instrucoes-api-key

## Installation

Clone the repository:

```bash
git clone https://github.com/ewertonfl/currency-to-brl.git
cd currency-to-brl
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment variables

Create a `.env` file in the project root:

```env
AWESOME_API_KEY=your_api_key_here
```

You can use `.env.example` as a reference:

```env
AWESOME_API_KEY=your_api_key_here
```

> Important: never commit your real `.env` file. Only commit `.env.example`.

## Usage

Run:

```bash
python currency_to_brl.py
```

The script will print a JSON response with the current exchange rates.

## Example output

```json
{
  "base": "BRL",
  "description": "Currency conversion values between LATAM currencies and Brazilian Real.",
  "source": "AwesomeAPI",
  "consulted_at": "2026-05-05T15:07:58.986103",
  "quotes": [
    {
      "country": "Colombia",
      "currency": "COP",
      "currency_name": "Colombian Peso",
      "pair": "COP-BRL",
      "one_currency_to_brl": "0.00132448",
      "one_brl_to_currency": "755.0133",
      "bid": "0.00132295",
      "ask": "0.00132601",
      "high": "0.00136922",
      "low": "0.00131763",
      "variation": "-0.000045",
      "variation_percent": "-3.322808",
      "quote_date": "2026-05-05 14:48:10",
      "timestamp": "1778003290"
    }
  ]
}
```

## Field explanation

### `one_currency_to_brl`

Represents how much 1 unit of the foreign currency is worth in BRL.

Example:

```txt
1 COP = 0.00132448 BRL
```

### `one_brl_to_currency`

Represents how much 1 BRL is worth in the foreign currency.

Example:

```txt
1 BRL = 755.0133 COP
```

This field is useful when comparing against systems that store exchange rates as:

```txt
BRL -> foreign currency
```

## Exchange rate direction

AwesomeAPI returns exchange rates in this direction:

```txt
1 foreign currency = X BRL
```

This project also calculates the inverse direction:

```txt
1 BRL = X foreign currency
```

The inverse value is calculated as:

```txt
1 / one_currency_to_brl
```

Example:

```txt
1 COP = 0.00132448 BRL
1 BRL = 755.0133 COP
```

## Project structure

```txt
currency-to-brl/
├── currency_to_brl.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
└── LICENSE
```

## Dependencies

The project uses:

```txt
requests
python-dotenv
```

Install them with:

```bash
pip install -r requirements.txt
```

## Important notes

Some currencies may not update at the exact same timestamp because exchange rate availability depends on the provider and market liquidity.

Currencies with lower liquidity may return older quote timestamps compared to major currencies such as USD or MXN.

For commercial, accounting, tax, or financial-critical usage, always validate AwesomeAPI's current terms, limits, and commercial usage conditions before using this data in production.

## License

MIT