import boto3
import sys

TABLE_NAME = "katobot"


def main():
    try:
        with open("./KatoQuotes.txt", "r") as f:
            quotes = f.readlines()
    except IOError as e:
        print("File I/O Error! Abort.")
        print(e)
        return 1

    try:
        dynamo_db = boto3.resource("dynamodb")
        table = dynamo_db.Table(TABLE_NAME)
        with table.batch_writer() as batch:
            for i, quote in enumerate(quotes):
                batch.put_item(
                    Item={
                        "id": i + 1,
                        "quote": quote
                    }
                )
                print("threw to {0} dynamoDB! id:{1} quote:{2}".format(TABLE_NAME, i, quote))
    except Exception as e:
        print("some ERROR was detected. Abort.")
        print(e)
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
