PDF_CHUNK = {"size": 800, "overlap": 100}
HTML_CHUNK = {"size": 1000, "overlap": 120}
YOUTUBE_CHUNK = {"size": 700, "overlap": 70}


def for_source(source: str) -> dict:
    s = source.lower()
    if s == "pdf":
        return PDF_CHUNK
    if s == "html":
        return HTML_CHUNK
    if s == "youtube":
        return YOUTUBE_CHUNK
    return {"size": 800, "overlap": 100}
