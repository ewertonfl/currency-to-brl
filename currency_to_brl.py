import os
import json
import requests
from decimal import Decimal
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("AWESOME_API_KEY")

if not API_KEY:
    raise Exception("AWESOME_API_KEY was not found in the .env file.")

CURRENCIES = {
    "united_states": {
        "country": "United States",
        "currency": "USD",
        "currency_name": "US Dollar",
        "pair": "USD-BRL"
    },
    "argentina": {
        "country": "Argentina",
        "currency": "ARS",
        "currency_name": "Argentine Peso",
        "pair": "ARS-BRL"
    },
    "colombia": {
        "country": "Colombia",
        "currency": "COP",
        "currency_name": "Colombian Peso",
        "pair": "COP-BRL"
    },
    "peru": {
        "country": "Peru",
        "currency": "PEN",
        "currency_name": "Peruvian Sol",
        "pair": "PEN-BRL"
    },
    "ecuador": {
        "country": "Ecuador",
        "currency": "USD",
        "currency_name": "US Dollar",
        "pair": "USD-BRL"
    },
    "bolivia": {
        "country": "Bolivia",
        "currency": "BOB",
        "currency_name": "Bolivian Boliviano",
        "pair": "BOB-BRL"
    },
    "mexico": {
        "country": "Mexico",
        "currency": "MXN",
        "currency_name": "Mexican Peso",
        "pair": "MXN-BRL"
    },
    "paraguay": {
        "country": "Paraguay",
        "currency": "PYG",
        "currency_name": "Paraguayan Guarani",
        "pair": "PYG-BRL"
    },
    "chile": {
        "country": "Chile",
        "currency": "CLP",
        "currency_name": "Chilean Peso",
        "pair": "CLP-BRL"
    }
}


def decimal_to_string(value: Decimal, places: int | None = None) -> str:
    if places is not None:
        quantizer = Decimal("1." + ("0" * places))
        return str(value.quantize(quantizer))

    return str(value)


def fetch_exchange_rates() -> dict:
    pairs = ",".join(dict.fromkeys(currency_data["pair"] for currency_data in CURRENCIES.values()))

    url = f"https://economia.awesomeapi.com.br/json/last/{pairs}"

    headers = {
        "x-api-key": API_KEY
    }

    response = requests.get(url, headers=headers, timeout=15)

    if response.status_code != 200:
        raise Exception({
            "error": "Failed to fetch data from AwesomeAPI.",
            "status_code": response.status_code,
            "response": response.text
        })

    api_data = response.json()

    result = {
        "base": "BRL",
        "description": "Currency conversion values between LATAM currencies and Brazilian Real.",
        "source": "AwesomeAPI",
        "consulted_at": datetime.now().isoformat(),
        "quotes": []
    }

    for country_key, currency_data in CURRENCIES.items():
        api_key = currency_data["pair"].replace("-", "")

        quote = api_data.get(api_key)

        if not quote:
            result["quotes"].append({
                "country": currency_data["country"],
                "currency": currency_data["currency"],
                "pair": currency_data["pair"],
                "error": "Exchange rate was not returned by the API."
            })
            continue

        bid = Decimal(quote["bid"])
        ask = Decimal(quote["ask"])

        # 1 local currency = X BRL
        one_currency_to_brl = (bid + ask) / Decimal("2")

        # 1 BRL = X local currency
        one_brl_to_currency = Decimal("1") / one_currency_to_brl

        result["quotes"].append({
            "country": currency_data["country"],
            "currency": currency_data["currency"],
            "currency_name": currency_data["currency_name"],
            "pair": currency_data["pair"],

            "one_currency_to_brl": decimal_to_string(one_currency_to_brl),
            "one_brl_to_currency": decimal_to_string(one_brl_to_currency, 4),

            "bid": decimal_to_string(bid),
            "ask": decimal_to_string(ask),
            "high": quote.get("high"),
            "low": quote.get("low"),
            "variation": quote.get("varBid"),
            "variation_percent": quote.get("pctChange"),
            "quote_date": quote.get("create_date"),
            "timestamp": quote.get("timestamp")
        })

    return result


if __name__ == "__main__":
    exchange_rates = fetch_exchange_rates()
    print(json.dumps(exchange_rates, ensure_ascii=False, indent=2))