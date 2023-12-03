class QuotesProviderDummy:
    
    def __init__(self):
         self.quote_dict = {
            "number": 666,
            "content": 'テストの名言'
        }
    
    def get_quote(self) :
        return self.quote_dict
