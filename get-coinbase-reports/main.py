import http.client
import os

from coinbase import jwt_generator

key_name = os.environ.get("COINBASE_KEY_NAME")
key_secret = os.environ.get("COINBASE_KEY_SECRET")


def createReport():
    conn = http.client.HTTPSConnection("api.exchange.coinbase.com")
    payload = ''
    headers = {
        'Content-Type': 'application/json',
        'cb-access-timestamp': time.time()
    }
    conn.request("POST", "/reports", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
def main():
    createReport()

if __name__ == '__main__':
    main()
