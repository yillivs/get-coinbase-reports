import json
import os
from datetime import date

from json2html import *
from coinbase.rest import RESTClient
import boto3
from botocore.exceptions import ClientError

portfolio_uuid = os.environ.get("PORTFOLIO_UUID")
recipient_email_list = json.loads(os.environ.get("RECIPIENT_EMAIL_LIST"))
sender_email_address = os.environ.get("SENDER_EMAIL_ADDRESS")


def getPortfolioBreakdown():
    client = RESTClient()
    result = client.get_portfolio_breakdown(portfolio_uuid)['breakdown']['portfolio_balances']
    keys_to_remove = ['perp_unrealized_pnl', 'futures_unrealized_pnl', 'total_futures_balance']
    for key in keys_to_remove:
        if key in result:
            result.pop(key)
    result = json2html.convert(result)
    return result

def getFormattedHtml(report, current_date):
    email_body = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }}
            .container {{
                width: 80%;
                margin: 0 auto;
                padding: 20px;
                background-color: #f7f7f7;
            }}
            .content {{
                background-color: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #333;
                margin-top: 0;
            }}
            p {{
                color: #666;
                margin-bottom: 0;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
            <h1>Brassert Cryptocurrency Balances Report {current_date}</h1>
            </div>
            <div class="content">
                {report}
            </div>
        </div>
    </body>
    </html>
    """
    return email_body

def emailReport(report_html):
    ses_client = boto3.client('ses', region_name='us-east-1')
    current_date = date.today().strftime("%m/%d/%Y")

    message = {
        'Subject': {'Data': "Brassert Cryptocurrency Balances Report " + current_date},
        'Body': {
            'Html': {
                'Data': getFormattedHtml(report_html, current_date)
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
        return response

def lambda_handler(event, context):
    message = getPortfolioBreakdown()
    return emailReport(message)
