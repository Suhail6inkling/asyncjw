from .episode import Episode
from .object import Object
from .util import image_url, path_url


class Season(Object):
    def __init__(self, show, data):
        self.client = show.client
        self.show = show

        self.number = data.get("season_number")
        self.title = data.get("title")
        self.type = "show_season"
        self.id = data.get("id")
        self.poster = image_url(data.get("poster"))
        self.path = path_url(data.get("full_path"))
        self.expanded = False

        self._data = data

    def __repr__(self):
        return f"<Season title={self.title!r} number={self.number} id={self.id} show={self.show!r} expanded={self.expanded}>"

    async def expand(self):
        data = await self.client.http.get_season(self.id)
        self.__init__(self.show, data)
        self.backdrops = [
            image_url(x["backdrop_url"]) for x in data.get("backdrops", [])
        ]
        self.popularity = data.get("tmdb_popularity")

        self.credits = data.get("credits")
        self.genres = [self.client._genres[x] for x in data.get("genre_ids", [])]

        self.episodes = [Episode(self, x) for x in data.get("episodes", [])]

        self.offers = []

        for x in data.get("offers", []):
            id = x["provider_id"]
            provider = self.client._providers[id]

            self.offers.append(provider.from_item(self, x))

        self.expanded = True
