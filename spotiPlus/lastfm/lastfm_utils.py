import requests
import pprint
import re

from spotiPlus.lastfm.secrets import LASTFM_API_KEY, LASTFM_SHARED_SECRET


def get_artist_summary(artist: str) -> str:
    summary = "Detailed information about the current artist is not yet avaliable."
    try:
        response = requests.get(
            f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist}&api_key={LASTFM_API_KEY}&format=json"
        )
        if response == "":
            return summary
        summary = response.json()["artist"]["bio"]["summary"]
        summary = re.sub("<[^<]+?>", "", summary)
        summary = summary.replace("Read more on Last.fm", "")
    except KeyError:
        return "Detailed information about the current artist is not yet avaliable."

    return summary


def get_track_summary(track: str, artist: str) -> str:
    summary = "Detailed information about the current track is not yet avaliable."
    try:
        response = requests.get(
            f"http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={LASTFM_API_KEY}&artist={artist}&track={track}&format=json"
        )
        summary = response.json()["track"]["wiki"]["summary"]
        summary = re.sub("<[^<]+?>", "", summary)
        summary = summary.replace("Read more on Last.fm", "")

    except KeyError:
        return "Detailed information about the current track is not yet avaliable."

    return summary
