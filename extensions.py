import os
import requests
from config import exchanges
from dotenv import load_dotenv

load_dotenv(".env")

_api_key = os.getenv("EXCHANGE_API_KEY")


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, symbol, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена.")
        try:
            symbol_key = exchanges[symbol.lower()]
        except KeyError:
            raise APIException(f"Валюта {symbol} не найдена.")

        if base_key == symbol_key:
            raise APIException(f"Названия валют должны быть уникальны.")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Некорретное количество валюты")

        request = requests.get(f"https://currate.ru/api/?get=rates&pairs={base_key}{symbol_key}&key={_api_key}")
        response = request.json()
        new_price = round(float(response["data"][f"{base_key}{symbol_key}"]) * amount, 3)
        message = f"Цена {amount} {base} в {symbol} : {new_price}"
        return message
