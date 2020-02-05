def image_url(url):
    if not url:
        return
    
    base = "https://images.justwatch.com"

    if "poster" in url:
        profile = "s592"
    else:
        profile = "s100"
    
    return base + url.format(profile=profile)

def path_url(url):
    if not url:
        return
    
    base = "http://justwatch.com"

    return base + url
