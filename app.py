import json
import ftx  # type: ignore
import os
import time
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
subaccount_name = os.getenv("SUBACCOUNT_NAME")

'''
with open('config.json', 'r') as f:
    config = json.load(f)
'''

client = ftx.FtxClient(api_key=api_key, api_secret=api_secret, subaccount_name=subaccount_name)

markets = client.get_futures()

# pprint(markets)

endTime = int(time.time())
startTime = endTime - 86400

for market in markets:
    name = market["name"]

    if market["perpetual"] and market["enabled"]:
        hours = client.get_historical_data(market_name=name, resolution=3600, limit=24, start_time=startTime, end_time=endTime)

        low = 0
        high = 0

        for hour in hours:
            if hour["high"] > high:
                high = hour["high"]
            if hour["low"] < low or low == 0:
                low = hour["low"]

        # TO DO: Add data to Dict List
        # TO DO: Sort List by volatility

        print(name)
        print("High:", high)
        print("Low:", low)
        print("Vola:", ((high / low) - 1) * 100)
        print()
