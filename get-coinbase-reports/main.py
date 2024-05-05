import json
import os
from json2html import *
from coinbase.rest import RESTClient
import boto3
from botocore.exceptions import ClientError

key_name = os.environ.get("COINBASE_KEY_NAME")
key_secret = os.environ.get("COINBASE_KEY_SECRET")
portfolio_uuid = os.environ.get("PORTFOLIO_UUID")
recipient_email_list = json.loads(os.environ.get("RECIPIENT_EMAIL_LIST"))
sender_email_address = os.environ.get("SENDER_EMAIL_ADDRESS")


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

    message = {
        'Subject': {'Data': "Test"},
        'Body': {
            'Html': {
                'Data': report_html
            }
        }
    }

    try:
        response = ses_client.send_email(
            Source=sender_email_address,
            Destination={
                'ToAddresses': recipient_email_list
            },
            Message=message
        )
    except ClientError as e:
        print(e)
    else:
        print("email sent!")

def main():
    message = createReport()
    emailReport(message)



if __name__ == '__main__':
    main()
