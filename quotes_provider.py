from quotes_provider_by_file import QuotesProviderByFile


class QuoteProvider(QuotesProviderByFile):

    def __init__(self):
        super(QuoteProvider, self).__init__("./KatoQuotes.txt")

    def get_quote(self):
        return super().get_quote()
