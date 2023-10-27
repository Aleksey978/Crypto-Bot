import json
import requests
from config import keys


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote, base, amount):
        if quote == base:
            raise ConvertionException(f"Невозвожно перевести {quote} в {quote}")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {quote}")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"Не удалось обработать количество валюты {amount}")

        res = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(res.content)[keys[base]]
        total_base *= amount
        return total_base
