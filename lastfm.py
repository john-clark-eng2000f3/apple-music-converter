import json
import time
import urllib.error
import urllib.parse
import urllib.request

LASTFM_API = "https://ws.audioscrobbler.com/2.0/"

class LastFmError(Exception):
    pass

def _get(method, params, api_key):
    query = {
        "method": method,
        "api_key": api_key,
        "format": "json",
    }
    query.update(params)
    url = f"{LASTFM_API}?{urllib.parse.urlencode(query)}"

    req = urllib.request.Request(url)
    req.add_header("User-Agent", "convert/0.1")

    retries = 0
    while True:
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode()
        except urllib.error.HTTPError as e:
            if e.code == 429 and retries < 3:
                retries += 1
                time.sleep(2 ** retries)
                continue
            raise LastFmError(f"http {e.code}")
        except Exception as e:
            raise LastFmError(str(e))
        break

    # print(f"body: {body[:200]}")  # debug
    data = json.loads(body)
    if data.get("error"):
        raise LastFmError(data.get("message", "unknown error"))
    return data

def fetch_recent_tracks(user, api_key, limit=200):
    tracks = []
    page = 1
    total_pages = 1

    while page <= total_pages:
        data = _get("user.getrecenttracks", {
            "user": user,
            "limit": limit,
            "page": page,
        }, api_key)

        recent = data.get("recenttracks", {})
        if not recent:
            break
        attr = recent.get("@attr", {})
        total_pages = int(attr.get("totalPages", 1))

        for item in recent.get("track", []):
            if item.get("@attr", {}).get("nowplaying"):
                continue
            tracks.append({
                "artist": item.get("artist", {}).get("#text", ""),
                "track": item.get("name", ""),
                "album": item.get("album", {}).get("#text", ""),
                "timestamp": int(item.get("date", {}).get("uts", 0)),
            })

        page += 1
        if page <= total_pages:
            time.sleep(0.25)

    return tracks
