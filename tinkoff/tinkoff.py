import os
from t_tech.invest import Client
from t_tech.invest import RealExchange
from t_tech.invest import SecurityTradingStatus
from dotenv import load_dotenv
from t_tech.invest import Client
from t_tech.invest import SecurityTradingStatus

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
      if share.trading_status
      != SecurityTradingStatus.SECURITY_TRADING_STATUS_NOT_AVAILABLE_FOR_TRADING
      and share.real_exchange == RealExchange.REAL_EXCHANGE_MOEX
    ]