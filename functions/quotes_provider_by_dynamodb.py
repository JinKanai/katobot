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
        self.TABLE_NAME = "katobot"
        self.resource = boto3.resource("dynamodb")
        self.table = self.resource.Table(self.TABLE_NAME)

    def _get_item_counts(self):
        """

        katobotの格言数を得るメソッド

        Returns:
            int: 格言の総数

        """
        return self.table.item_count

    def get_quote(self):
        """

        格言を得るメソッド

        Returns:
            dict: [int,str] 格言の番号と格言を持った辞書

        """
        id = random.choice(range(self._get_item_counts()))
        q = self.table.get_item(
            Key={
                "id": id
            }
        )
        # 改行が含まれているので削除する
        quote = q["Item"]["quote"].rstrip("\n")
        quote_dict = {
            "number": id,
            "content": quote
        }
        return quote_dict


def main():
    """
    テスト用関数
    """
    p = QuotesProviderByDynamoDb()
    print(p.get_quote())


if __name__ == '__main__':
    import sys
    sys.exit(main())
