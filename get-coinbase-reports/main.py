import os
from json2html import *
from coinbase.rest import RESTClient
import boto3
from botocore.exceptions import ClientError

key_name = os.environ.get("COINBASE_KEY_NAME")
key_secret = os.environ.get("COINBASE_KEY_SECRET")
portfolio_uuid = os.environ.get("PORTFOLIO_UUID")
recipient_email_list = os.environ.get("RECIPIENT_EMAIL_LIST")


def getPortfolioBreakdown():
    client = RESTClient()
    breakdown = client.get_portfolio_breakdown(portfolio_uuid)['breakdown']['portfolio_balances']

    keys_to_remove = ['perp_unrealized_pnl', 'futures_unrealized_pnl', 'total_futures_balance']

    for key in keys_to_remove:
        if key in breakdown:
            breakdown.pop(key)
    return breakdown

def createReport():
    html_breakdown = json2html.convert(getPortfolioBreakdown())
    return html_breakdown


def emailReport(report_html):
    ses_client = boto3.client('ses', region_name='us-east-1')

    try:
        response = ses_client.send_email(
            Source='trickquestionis@gmail.com',
            Destination={
                'ToAddresses': [recipient_email_list]
            },
            Message=report_html
        )
    except ClientError as e:
        print(e)
    else:
        print("email sent!")

def main():
    message = createReport()
 #   emailReport(message)



if __name__ == '__main__':
    main()
