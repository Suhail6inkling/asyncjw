from datetime import timedelta
from .object import Object
from .util import image_url


class Episode(Object):
    def __init__(self, season, data):
        self.season = season
        self.show = season.show
        self.client = season.client

        self.id = data.get("id")
        self.title = data.get("title")
        self.type = "show_episode"
        self.poster = image_url(data.get("poster"))
        self.description = data.get("short_description")
        self.runtime = data.get("runtime") and timedelta(minutes=data.get("runtime"))
        self.number = data.get("episode_number")

        self.offers = []

        for x in data.get("offers", []):
            id = x["provider_id"]
            provider = self.client._providers[id]

            self.offers.append(provider.from_item(self, x))

    def __repr__(self):
        return f"<Episode title={self.title!r} number={self.number} id={self.id} seaosn={self.season!r}>"
