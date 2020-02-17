from .object import Object


class SearchResults(Object):
    def __init__(self, client, data):
        self.client = client
        self._data = data
        self.__dict__.update(data)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"<SearchResults query={self.query!r}>"
