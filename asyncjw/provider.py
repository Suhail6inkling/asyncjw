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

    
