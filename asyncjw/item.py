from datetime import datetime, timedelta

from .object import Object
from .util import image_url, path_url

class Item(Object):
    def __init__(self, client, data):
        self.client = client

        self.id = data.get("id")
        self.title = data.get("title")
        self.type = data.get("object_type")
        self.release_year = data.get("original_release_year")
        self.path = path_url(data.get("full_path"))
        self.poster = image_url(data.get("poster"))
        self.popularity = data.get("tmdb_popularity")
        self.offers = []
        lrd = data.get("localized_release_date")
        if lrd:
            self.release_date = datetime.strptime(lrd, "%Y-%m-%d")
        else:
            self.release_date = None

        for x in data.get("offers", []):
            id = x["provider_id"]
            provider = self.client._providers[id]

            self.offers.append(provider.from_item(self, x))
        
        self._data = data
        
    def __repr__(self):
        return f"<Item title={self.title!r} id={self.id} type={self.type!r}>"
    