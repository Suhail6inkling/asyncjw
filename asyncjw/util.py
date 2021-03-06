def image_url(url):
    if not url:
        return

    base = "https://images.justwatch.com"

    if "poster" in url:
        profile = "s592"
    elif "backdrop" in url:
        profile = "s1440"
    else:
        profile = "s100"

    return base + url.format(profile=profile)


def path_url(url):
    if not url:
        return

    base = "http://justwatch.com"

    return base + url


def get_id(obj):
    from .provider import Provider
    from .genre import Genre
    from .certification import Certification

    if isinstance(obj, (Provider, Genre)):
        return obj.short
    elif isinstance(obj, Certification):
        return obj.name
    elif isinstance(obj, list):
        return [get_id(x) for x in obj]
    else:
        return obj
        


async def multi_country(default, *others):
    
    from .client import Client as cls
    
    
    clients = {}
    
    origin = cls(default)
    
    await origin._initialize()
    
    clients[default] = origin
    
    genres, providers, certifications = origin._genres, origin._providers, orgin._certifications
    
    for country in others:
        client = cls(country)
        
        clients[country] = client
        
        client._genres, client._providers, client._certifications = genres, providers, certifications
    
    return clients
        
        
