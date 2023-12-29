# -*- coding: utf-8 -*-

import boto3
import random
import os

from datetime import datetime
from boto3.dynamodb.conditions import Key


class QuotesProviderByDynamoDb:
    def __init__(self):
        # self.TABLE_NAME = "GoldenQuotes"
        self.TABLE_NAME = os.environ["DYNAMODB_TABLE"]
        self.resource = boto3.resource("dynamodb")
        # self.resource = boto3.resource(
        #    "dynamodb", endpoint_url="http://192.168.0.11:8000"
        # )
        self.table = self.resource.Table(self.TABLE_NAME)
        self.item_count = self.table.item_count

    def get_quote(self):
        today = datetime.today()
        # target は今日より三ヶ月前のUNIXTIME
        target = int(
            datetime.timestamp(datetime(today.year, today.month - 3, today.day))
        )

        # 三ヶ月以上前に発言した格言からランダムで一個取り出す
        quotes = self.table.query(
            IndexName="said_index",
            KeyConditionExpression=Key("author").eq("kato-bucho")
            & Key("said_at").lt(target),
        )
        quote_dict = random.choice(quotes["Items"])

        # 発言した格言のsaid_atを今日のタイムスタンプに変更
        option = {
            "Key": {"author": "kato-bucho", "id": quote_dict["id"]},
            "UpdateExpression": "set #said_at = :said_at",
            "ExpressionAttributeNames": {"#said_at": "said_at"},
            "ExpressionAttributeValues": {":said_at": int(datetime.timestamp(today))},
        }
        res = self.table.update_item(**option)

        return quote_dict


def test_func():
    d = QuotesProviderByDynamoDb()
    print(d.get_quote())


if __name__ == "__main__":
    import sys

    sys.exit(test_func())
