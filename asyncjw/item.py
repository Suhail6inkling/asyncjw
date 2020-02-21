from datetime import datetime, timedelta

from .object import Object
from .season import Season
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
        self.expanded = False

    def __repr__(self):
        return f"<Item title={self.title!r} id={self.id} type={self.type!r} expanded={self.expanded}>"

    async def expand(self):
        data = await self.client.http.get_item(self.id, self.type)

        self.__init__(self.client, data)
        self.backdrops = [
            image_url(x["backdrop_url"]) for x in data.get("backdrops", [])
        ]
        self.description = data.get("short_description")
        self.genres = [self.client._genres[x] for x in data.get("genre_ids", [])]
        self.age_rating = (
            data.get("age_certification")
            and self.client._certifications[self.type][data.get("age_certification")]
        )
        self.credits = data.get("credits")
        self.runtime = data.get("runtime")
        self.seasons = [Season(self, d) for d in data.get("seasons", [])]

        self.expanded = True
