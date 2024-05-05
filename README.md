# Cryptocurrency Portfolio Report Generator

This script generates a report of cryptocurrency portfolio balances and sends it via email. It is designed to be run as an AWS Lambda function triggered by an event.

## Dependencies

- `json`: Python module for parsing and serializing JSON data.
- `os`: Python module providing a portable way of using operating system-dependent functionality.
- `datetime`: Python module for manipulating dates and times.
- `json2html`: Python library to convert JSON data to HTML tables.
- `coinbase-advanced-py`: Python library for interacting with the Coinbase API.
- `boto3`: AWS SDK for Python (Boto3) to interact with AWS services.
- `botocore`: Low-level interface to AWS services.

## Usage

1. Set up AWS Lambda function with appropriate permissions to access SES and other required services.
2. Configure environment variables:
   - `PORTFOLIO_UUID`: Unique identifier for the cryptocurrency portfolio.
   - `RECIPIENT_EMAIL_LIST`:  string representing a list of recipient email addresses.
   - `SENDER_EMAIL_ADDRESS`: Sender email address for the report email.
   - `COINBASE_API_KEY`: API key to access Coinbase API's.
   - `COINBASE_API_SECRET`: API secret to access Coinbase API's.
3. Trigger the Lambda function either manually or via an event.
4. The function fetches the portfolio breakdown using the Coinbase API, formats the data into an HTML email body, and sends the report via Amazon SES.

## Lambda Handler

The Lambda function is triggered by an event and executes the `lambda_handler` function defined in `lambda_function.py`. This function orchestrates the generation and email delivery of the cryptocurrency portfolio report.

## Credits

- [Coinbase Advanced Python API](https://github.com/coinbase/coinbase-advanced-py)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [json2html Documentation](https://pypi.org/project/json2html/)

---
