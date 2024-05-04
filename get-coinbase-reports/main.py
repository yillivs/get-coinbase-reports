import json
import os
from coinbase.rest import RESTClient

key_name = os.environ.get("COINBASE_KEY_NAME")
key_secret = os.environ.get("COINBASE_KEY_SECRET")
portfolio_uuid = os.environ.get("PORTFOLIO_UUID")

def getPortfolioBreakdown():
    client = RESTClient()
    breakdown = client.get_portfolio_breakdown(portfolio_uuid)['breakdown']
    return breakdown

def main():
    obj = json.dumps(getPortfolioBreakdown(), indent=4)
    print(obj)


if __name__ == '__main__':
    main()
