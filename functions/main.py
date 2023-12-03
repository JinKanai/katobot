import json
import requests
import os

from quotes_provider_by_dynamodb import QuotesProviderByDynamoDb


def lambda_handler(event, context):
    """

    AWS lambdaから起動されるメイン関数

    Args:
        event (dict): 未使用
        context (dict): 未使用

    Returns:
        dict: HTTP responce

    """

    # kato = QuotesProviderByDynamoDb()
    kato = QuotesProviderByDynamoDb()
    quote = kato.get_quote()

    message = {
        "text": None,
        "attachments": [
            {
                "hoge": None
            }
        ]
    }

    message["text"]="【本日の加藤家家訓】 その{0}".format(str(quote["number"]))
    message["color"]="#ff0000"
    message["attachments"][0]["title"] = quote["content"]

    url = os.environ["MESSENGER_URL"]
    r = requests.post(url, data=json.dumps(message))
    # return r


def main():
    print(lambda_handler(None, None))


if __name__ == '__main__':
    import sys

    """
    テスト用main関数
    """
    sys.exit(main())
