# -*- coding: utf-8 -*-

import boto3
import random


class QuotesProviderByDynamoDb:
    """
    dynamoDBに格納されている格言を扱うクラス
    """

    def __init__(self):
        """

        コンストラクタ
        dynamoDBのkatobotテーブルオブジェクトを取得

        """
        self.TABLE_NAME = "katobot-remaining"
        self.resource = boto3.resource("dynamodb")
        self.table = self.resource.Table(self.TABLE_NAME)
        self.item_count = self.table.item_count
        self.all_quotes = self.table.scan()

    def _get_not_said_quote(self):
        quotes = self._get_all_of_not_said_quotes()
        if not quotes:
            self._flush_is_said()
            quotes = self._get_all_of_not_said_quotes()
        quote = random.choice(quotes)
        return quote

    def _get_all_of_not_said_quotes(self):
        return [quote for quote in self.all_quotes["Items"] if not quote["isSaid"]]

    def get_quote(self):
        """

        格言を得るメソッド

        Returns:
            dict: [int,str] 格言の番号と格言を持った辞書

        """
        # 改行が含まれているので削除する
        quote = self._get_not_said_quote()
        content = quote["quote"].rstrip("\n")
        quote_dict = {
            "number": quote["id"],
            "content": content
        }

        quote["isSaid"] = 1
        self.table.put_item(
                Item=quote
        )
        return quote_dict

    def _flush_is_said(self):
        for quote in self.all_quotes["Items"]:
            quote["isSaid"] = 0
            self.table.put_item(
                    Item=quote
                    )
        return

def main():
    """
    テスト用関数
    """
    p = QuotesProviderByDynamoDb()
    quote = p.get_quote()
    print(quote)
    print(p.item_count)

if __name__ == '__main__':
    import sys
    sys.exit(main())
