from postkun.slack import SlackHandler
from quotes_provider_by_dynamodb import QuotesProviderByDynamoDb
from quotes_provider_dummy import QuotesProviderDummy


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
    kato = QuotesProviderDummy() 
    quote = kato.get_quote()

    messenger = SlackHandler()
    messenger.set_pre_text("【本日の加藤家家訓】 その{0}".format(str(quote["number"])))
    messenger.set_color("#ff0000")

    title = quote["content"]
    messenger.set_attachments(
        [
            {
                "title": title,
                "value": None
            }
        ]
    )

    r = messenger.post_message()
    return r


def main():
    print(lambda_handler(None, None))


if __name__ == '__main__':
    import sys

    """
    テスト用main関数
    """
    sys.exit(main())
