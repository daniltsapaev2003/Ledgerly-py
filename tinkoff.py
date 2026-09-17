import os

from dotenv import load_dotenv
from t_tech.invest import Client

load_dotenv()

TINKOFF_TOKEN = os.getenv("TINKOFF_TOKEN")

def get_shares():
    if not TINKOFF_TOKEN:
        raise RuntimeError("TINKOFF_TOKEN не найден в .env")

    with Client(TINKOFF_TOKEN) as client:
        response = client.instruments.shares()

    return [
    share
    for share in response.instruments
    if share.api_trade_available_flag
]