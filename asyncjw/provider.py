from .object import Object
from .util import image_url


class Provider(Object):
    def __init__(self, client, data):
        self.client = client

        self.id = data.get("id")
        self.name = data.get("clear_name")
        self.short = data.get("short_name")
        self.technical = data.get("technical_name")
        self.icon_url = image_url(data.get("icon_url"))

        self._data = data

    def __repr__(self):
        return f"<Provider name={self.name!r} id={self.id}>"

    def __eq__(self, other):
        if isinstance(other, Provider):
            return self.id == other.id
        return super().__eq__(other)

    def from_item(self, item, data):
        return ExpandedProvider(self.client, self._data, item, data)


class ExpandedProvider(Provider):
    def __init__(self, client, provider_data, item, item_data):
        super().__init__(client, provider_data)

        self.item = item

        self.currency = item_data.get("currency")
        self._type = item_data.get("monetization_type")
        self.definition = item_data.get("presentation_type")
        self.element_count = item_data.get("element_count")
        self.price = item_data.get("retail_price")
        urls = item_data.get("urls")
        self.url = urls and urls.get("standard_web")

        self._data_ext = item_data

    def __repr__(self):
        return f"<ExpandedProvider name={self.name!r} id={self.id} item={self.item!r} type={self.type!r}>"

    @property
    def type(self):
        conversion = {"flatrate": "Subscription", "ads": "Subscription (Ads)"}

        return conversion.get(self._type, self._type.title())
