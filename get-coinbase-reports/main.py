import json
import os
from coinbase.rest import RESTClient

key_name = os.environ.get("COINBASE_KEY_NAME")
key_secret = os.environ.get("COINBASE_KEY_SECRET")

def getPortfolioBreakdown():
    client = RESTClient()
    breakdown = client.get_portfolio_breakdown("fe02815f-af68-536c-89f2-74613329224e")
    return breakdown

def main():
    print(getPortfolioBreakdown())


if __name__ == '__main__':
    main()
