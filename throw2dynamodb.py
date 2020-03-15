import boto3
import sys
import csv

TABLE_NAME = "katobot-remaining"


def main():
    try:
        with open("./KatoQuotes.csv", "r") as f:
            quotes = [i for i in csv.reader(f)]
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
                        "isSaid": int(quote[1]),
                        "quote": quote[0]
                    }
                )
                print("threw to {0} dynamoDB! id:{1} quote:{2}".format(
                    TABLE_NAME, i, quote[0]))
    except Exception as e:
        print("some ERROR was detected. Abort.")
        print(e)
        return 1

    f.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
