from .object import Object


class Certification(Object):
    def __init__(self, client, data):
        self.client = client

        self.name = data.get("technical_name")
        self.id = data.get("id")
        self.description = data.get("description")
        self.type = data.get("object_type")
        self.country = data.get("country")

    def __repr__(self):
        return f"<Certification name={self.name!r} id={self.id}>"
