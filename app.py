import json
import ftx  # type: ignore
import os
import time
import pandas as pd

from pprint import pprint
from dotenv import load_dotenv

print("Getting market data...")
print()

load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
subaccount_name = os.getenv("SUBACCOUNT_NAME")

with open('config.json', 'r') as f:
    config = json.load(f)

minVolume24h = config["minVolume24h"]
minVolatility = config["minVolatility"]

client = ftx.FtxClient(api_key=api_key, api_secret=api_secret, subaccount_name=subaccount_name)

markets = client.get_futures()

tradeableMarkets = []  # type: list

endTime = int(time.time())
startTime = endTime - 86400

for market in markets:

    bid = market["bid"]
    ask = market["ask"]
    volume = market["volumeUsd24h"]

    if market["perpetual"] and market["enabled"] and (volume > minVolume24h):
        name = market["name"]

        hours = client.get_historical_data(market_name=name, resolution=3600, limit=24, start_time=startTime, end_time=endTime)

        low = 0
        high = 0

        for hour in hours:
            if hour["high"] > high:
                high = hour["high"]
            if hour["low"] < low or low == 0:
                low = hour["low"]

        volatility = ((high / low) - 1) * 100

        if volatility > minVolatility:
            tradeableMarket = {}
            tradeableMarket["name"] = name
            tradeableMarket["volatility"] = round(volatility, 2)
            tradeableMarket["volumeM"] = round(volume / 1000000, 0)
            tradeableMarkets.append(tradeableMarket)

df = pd.DataFrame(tradeableMarkets)
df.sort_values(by='volatility', inplace=True, ascending=False)

print(df)
