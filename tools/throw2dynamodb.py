import boto3
import csv

QUOTES_FILE = "./KatoQuotes.csv"
TABLE_NAME = "goldenQuotes"
LSI_NAME = "said_index"


def main():
    dynamodb_client = boto3.client("dynamodb")
    # dynamodb = boto3.client("dynamodb", endpoint_url="http://192.168.0.11:8000")

    # create table
    make_table = True
    t = dynamodb_client.list_tables()
    for table_name in t["TableNames"]:
        print(table_name)
        if TABLE_NAME == table_name:
            make_table = False
            print("{0} is already exist.".format(TABLE_NAME))
            break

    if make_table:
        dynamodb_client.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "author", "KeyType": "HASH"},
                {"AttributeName": "id", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "author", "AttributeType": "S"},
                {"AttributeName": "id", "AttributeType": "N"},
                {"AttributeName": "said_at", "AttributeType": "N"},
            ],
            LocalSecondaryIndexes=[
                {
                    "IndexName": LSI_NAME,
                    "KeySchema": [
                        {"AttributeName": "author", "KeyType": "HASH"},
                        {"AttributeName": "said_at", "KeyType": "RANGE"},
                    ],
                    "Projection": {
                        "ProjectionType": "INCLUDE",
                        "NonKeyAttributes": ["quote"],
                    },
                }
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )

    # wait for makiing table
    print("wating...")
    waiter = dynamodb_client.get_waiter("table_exists")
    waiter.wait(
        TableName=TABLE_NAME,
    )

    # open file handle for source data
    try:
        with open(QUOTES_FILE, "r") as f:
            quotes = [i for i in csv.reader(f)]
        print(quotes)
    except IOError as e:
        print("File I/O Error! Abort.")
        print(e)
        return 1

    # batch write to table
    # dynamodb = boto3.resource("dynamodb")
    # dynamodb = boto3.resource("dynamodb", endpoint_url="http://192.168.0.11:8000")
    dynamodb_resource = boto3.resource("dynamodb")
    try:
        table = dynamodb_resource.Table(TABLE_NAME)
        with table.batch_writer() as batch:
            for i, quote in enumerate(quotes):
                batch.put_item(
                    Item={
                        "author": "kato-bucho",
                        "said_at": i,
                        "quote": quote[0],
                        "id": i + 1,
                    }
                )
    except Exception as e:
        print("some ERROR was detected. Abort.")
        print(e)
        return 1

    f.close()
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
