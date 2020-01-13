from tocaro_handler import TocaroHandler
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

    kato = QuotesProviderByDynamoDb()
    tocaro = TocaroHandler()

    quote = kato.get_quote()

    tocaro.set_text("【本日の加藤家家訓】 その{0}".format(str(quote["number"])))
    tocaro.set_color("danger")

    title = quote["content"]
    tocaro.set_attachments(
        [
            {
                "title": title,
                "value": None
            }
        ]
    )

    r = tocaro.send2tocaro()
    return r


if __name__ == '__main__':
    """
    テスト用main
    """
    print(lambda_handler(None, None))
