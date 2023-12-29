import json
import requests
import os

from quotes_provider_by_dynamodb import QuotesProviderByDynamoDb
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()


def lambda_handler(event, context):
    kato = QuotesProviderByDynamoDb()
    quote = kato.get_quote()
    print(quote)

    message = {
        "username": "katbot the GOLDEN QUOTES from kato-bucho",
        "text": "【本日の加藤家家訓】 その{0}".format(str(quote["id"])),
        "color": "#ff0000",
        "attachments": [{"title": quote["quote"]}],
    }
    url = os.environ["MESSENGER_URL"]
    r = requests.post(url, data=json.dumps(message))
    # return r


def test_func():
    print(lambda_handler(None, None))


if __name__ == "__main__":
    import sys

    sys.exit(test_func())
