import random


class QuotesProviderByFile:

    def __init__(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            self.kato_quotes = f.readlines()

    def get_quote(self):
        quote = random.choice(list(enumerate(self.kato_quotes)))
        quote_dict = {
            "number": quote[0] + 1,
            "content": quote[1]
        }
        return quote_dict


if __name__ == '__main__':
    q = QuotesProviderByFile("./KatoQuotes.txt")
    print(q.get_quote())
