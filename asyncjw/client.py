import asyncio

from .certification import Certification
from .http import HTTP 
from .item import Item
from .genre import Genre
from .provider import Provider
from .util import get_id

class Client:

    def __init__(self, country="US", *, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.http = HTTP(self, loop=loop)
        self.country = country
        self._genres = {}
        self._providers = {}
        self._certifications = {}
        self._initialized=False

    def __repr__(self):
        return f"<Client country={self.country!r} locale={self.locale!r}>"

    @property
    def locale(self):
        return self.http.locale

    @property
    def genres(self):
        return list(self._genres.values())
    
    @property
    def providers(self):
        return list(self._providers.values())

    @property
    def certifications(self):
        return {key: list(value.values()) for key, value in self._certifications.items()}

    async def _initialize(self):
        self._initialized=True
        data = await self.http.get_locale()

        match = [
            result for result in data
            if result['iso_3166_2'] == self.country
            or result['country'] == self.country
        ][0]

        self.http.locale = match["full_locale"]

        data = await self.http.get_genres()
        self._genres = {g["id"]: Genre(self, g) for g in data}

        data = await self.http.get_providers()
        self._providers = {p["id"]: Provider(self, p) for p in data}
    
        data = await self.http.get_certifications("movie")
        self._certifications["movie"] = {c["technical_name"]: Certification(self, c) for c in data}

        data = await self.http.get_certifications("show")
        self._certifications["show"] = {c["technical_name"]: Certification(self, c) for c in data}


    async def search(self, query=None, **params):
        payload = {
			"age_certifications":None,
			"content_types":None,
			"presentation_types":None,
			"providers":None,
			"genres":None,
			"languages":None,
			"release_year_from":None,
			"release_year_until":None,
			"monetization_types":None,
			"min_price":None,
			"max_price":None,
			"nationwide_cinema_releases_only":None,
			"scoring_filter_types":None,
			"cinema_release":None,
			"query":None,
			"page":None,
			"page_size":None,
			"timeline_type":None,
			"person_id":None
		}
        filtered = {key: get_id(value) for key, value in params.items() if key in payload.keys()}
        payload.update(filtered)
        payload.update({"query":query})

        data = await self.http.search(payload)
        return [Item(self, x) for x in data.get("items", [])]