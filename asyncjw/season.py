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
    
    def __repr__(self):
        return f"<Season title={self.title!r} number={self.number} id={self.id} show={self.show!r}>"

