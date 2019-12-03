from quotes_provider import QuoteProvider
from tocaro_handler import TocaroHandler


def lambda_handler(event, context):
    harukas = QuoteProvider()

    tocaro = TocaroHandler()
    quote = harukas.get_quote()

    tocaro.set_text("【本日の加藤家家訓】 その{0}".format(str(quote["number"])))
    tocaro.set_color("danger")

    title = quote["content"]
    tocaro.set_attachments(
        [
            {
                "title": title,
                "value": "家訓の説明（必要であれば）"
            }
        ]
    )

    r = tocaro.send2tocaro()
    return r


if __name__ == '__main__':
    print(lambda_handler(None, None))
