class SearchResultsModel:
    
    def __init__(self, search_term, search_results):
        self.search_term = search_term
        self.search_results = search_results

    def get_search_results(self):
        return self.search_results

    def get_search_term(self):
        return self.search_term