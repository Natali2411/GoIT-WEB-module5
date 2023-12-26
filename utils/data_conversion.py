from __future__ import annotations


def get_tabulate_rate(rates: list[dict], currencies: list[str]):
    adapted_rates = []
    for rate_idx, rate_date in enumerate(rates):
        for currency_idx, currency_data in enumerate(rate_date["exchangeRate"]):
            if currency_data["currency"] in currencies:
                adapted_rates.append(
                    [
                        rate_date["date"],
                        currency_data["currency"],
                        currency_data["saleRateNB"],
                        currency_data["purchaseRateNB"],
                    ]
                )
    return adapted_rates


def get_rate_dict(rate_date: dict, currencies: list[str]) -> dict:
    return {
        rate_date["date"]: {
            rate["currency"]: {
                "purchase": rate["purchaseRateNB"],
                "sale": rate["saleRateNB"],
            }
            for rate in rate_date["exchangeRate"]
            if rate["currency"] in currencies
        }
    }


def adapt_exchange_json(
    rates: list[dict], currencies: tuple[str] | list[str]
) -> list[dict]:
    adapted_rates = []
    for rate_date in rates:
        adapted_rates.append(get_rate_dict(rate_date=rate_date, currencies=currencies))
    return adapted_rates

