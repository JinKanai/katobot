import boto3
import random


class QuotesProviderByDynamoDb:
    def __init__(self):
        self.TABLE_NAME = "katobot"
        self.resource = boto3.resource("dynamodb")
        self.table = self.resource.Table(self.TABLE_NAME)

    def _get_item_counts(self):
        return self.table.item_count

    def get_quote(self):
        id = random.choice(range(self._get_item_counts()))
        q = self.table.get_item(
            Key={
                "id": id
            }
        )
        quote = q["Item"]["quote"].rstrip("\n")
        quote_dict = {
            "number": id,
            "content": quote
        }
        return quote_dict


def main():
    p = QuotesProviderByDynamoDb()
    print(p.get_quote())


if __name__ == '__main__':
    main()
