import asyncio
import aiohttp


class Request:
    base = "https://apis.justwatch.com/content"

    def __init__(self, method, endpoint, **kwargs):
        self.method = method

        self.params = kwargs.pop("params", None)
        self.data = kwargs.pop("data", None)
        self.json = kwargs.pop("json", None)
        self.headers = kwargs.pop("headers", None)

        if endpoint:
            endpoint = endpoint.lstrip("/")
            self.url = f"{self.base}/{endpoint}"

    @property
    def kwargs(self):
        return dict(
            params=self.params, data=self.data, json=self.json, headers=self.headers
        )


class HTTP:
    def __init__(self, client, *, session=None, loop=None):
        self.client = client
        self.loop = loop or asyncio.get_event_loop()
        self.session = session or aiohttp.ClientSession(loop=self.loop)
        self.locale = None

    async def request(self, req, *, override=False):
        if not self.locale and not override:
            await self.client._initialize()
        async with self.session.request(
            req.method, req.url.format(locale=self.locale), **req.kwargs
        ) as resp:
            if resp.status == 200:
                return await resp.json()
            resp.raise_for_status()

    async def get_locale(self):
        return await self.request(Request("GET", "locales/state"), override=True)

    async def search(self, payload):
        return await self.request(
            Request("POST", "titles/{locale}/popular", json=payload)
        )

    async def get_genres(self):
        return await self.request(Request("GET", "genres/locale/{locale}"))

    async def get_providers(self):
        return await self.request(Request("GET", "providers/locale/{locale}"))

    async def get_certifications(self, content_type):
        params = dict(country=self.client.country, object_type=content_type)
        return await self.request(Request("GET", "age_certifications", params=params))

    async def get_item(self, id, content_type):
        return await self.request(
            Request(
                "GET",
                "titles/{content_type}/{id}/locale/{{locale}}".format(
                    content_type=content_type, id=id
                ),
            )
        )

    async def get_season(self, id):
        return await self.request(
            Request("GET", "titles/show_season/{id}/locale/{{locale}}".format(id=id))
        )
