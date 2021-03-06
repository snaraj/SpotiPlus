import spotipy
import pydantic

from typing import Dict, Union, List, TypedDict, Any
from spotipy.oauth2 import SpotifyOAuth


from spotiPlus.spotify.secrets import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    REDIRECT_URI,
    SCOPE,
)
from spotipy.exceptions import SpotifyException

# Spotify OAUTH2.0
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
    )
)


class User(pydantic.BaseModel):
    country: str
    display_name: str
    email: str
    explicit_content: dict[str, bool]
    external_urls: dict[str, str]
    followers: dict[str, Any]
    href: str
    id: str
    images: List[dict[str, Any]]
    product: str
    type: str
    uri: str


# ---> USER PROFILE FUNCTIONS:
# retrieves the current user authorized
def get_current_user() -> User:
    # creates an instance of User for type validation
    user: User = User(**sp.current_user())
    return user


# retrieves the current user profile picture link
def get_current_user_display_picture(current_user: User) -> str:
    return current_user.images[0]["url"]


# retrieves the current user display name
def get_current_user_display_name(current_user: User) -> str:
    return current_user.display_name


# ---> USER SAVED TRACKS FUNCTIONS:
# retrieve current user saved tracks
def get_current_user_saved_tracks(limit):
    current_user_saved_tracks = sp.current_user_saved_tracks(limit=limit)
    return current_user_saved_tracks


# get_current_user_saved_tracks returns json object, this function grabs the name of a track
def get_current_user_saved_track_name(track, index):
    return track["items"][index]["track"]["name"]


# get_current_user_saved_tracks return json object, this functions grabs the name of the artist
def get_current_user_saved_track_artist_name(track, index):
    return track["items"][index]["track"]["album"]["artists"][0]["name"]


# combines the previous functions above to get a list returning the
# following signature -> [artist, song]
def get_current_saved_tracks_list(limit):
    current_saved_tracks = get_current_user_saved_tracks(limit)
    saved_artist = []
    saved_song_name = []
    for i in range(limit):
        saved_artist.append(
            get_current_user_saved_track_artist_name(current_saved_tracks, i)
        )
        saved_song_name.append(
            get_current_user_saved_track_name(current_saved_tracks, i)
        )

    res = [saved_artist, saved_song_name]
    return res


class Playback(pydantic.BaseModel):
    actions: dict
    context: None
    currently_playing_type: str
    device: dict
    is_playing: bool
    item: dict
    progress_ms: int
    repeat_state: str
    shuffle_state: bool
    timestamp: int


# ---> USER CURRENT PLAYBLACK FUNCTIONS:
# get current playback:
def get_current_user_current_playback() -> Union[None, Playback]:
    current_playback = None
    try:
        current_playback = sp.current_playback()
    except TypeError:
        print("No current playback.")

    return current_playback


# grabs the song title for the current playback
def get_current_user_current_playback_song_title(current_playback: Playback) -> str:
    if current_playback:
        return current_playback["item"]["name"]
    else:
        return "Title Unavailable."


# grabs the song artist for the current playback
def get_current_user_current_playback_song_artist(current_playback):
    if current_playback:
        return current_playback["item"]["album"]["artists"][0]["name"]
    else:
        return "Artist Unavailable."


# get the current artist URI
def get_current_artist_uri(current_playback):
    if current_playback:
        return current_playback["item"]["album"]["artists"][0]["uri"]

    return None


def get_current_artist_id(current_playback):
    if current_playback:
        return current_playback["item"]["album"]["artists"][0]["id"]

    return None


# grabs the imagine for the current playback
def get_current_playback_image(current_playback):
    image_uri = "No Image Avaliable."
    try:
        image_uri = current_playback["item"]["album"]["images"][0]["url"]
    except TypeError:
        print("No song is currently playing.")
    return image_uri


# ---> USER'S TOP TRACKS & ARTIST:
# returns the user's top tracks
def get_current_user_top_tracks(limit):
    top_tracks = None
    try:
        top_tracks = sp.current_user_top_tracks(limit=limit)
    except TypeError:
        print("Top Tracks Unavailable.")

    return top_tracks


# returns the name of a top track
def get_current_user_top_track_name(top_tracks, index):
    if top_tracks:
        return top_tracks["items"][index]["name"]
    else:
        return "Top Track Name Unavailable."


def generate_top_track_list(limit):
    top_tracks = get_current_user_top_tracks(limit)
    top_tracks_list = []
    for i in range(limit):
        top_tracks_list.append(get_current_user_top_track_name(top_tracks, i))

    return top_tracks_list


# return the user's top artists
def get_current_user_top_artists(limit):
    top_artists = None
    try:
        top_artists = sp.current_user_top_artists(limit=limit)
    except TypeError:
        print("Top Artists Unavailable.")

    return top_artists


def get_current_user_top_artist_name(top_artist, index):
    if top_artist:
        return top_artist["items"][index]["name"]
    else:
        return "Top artist not found."


def generate_top_artist_list(limit):
    top_artists = get_current_user_top_artists(limit)
    top_artist_list = []
    for i in range(limit):
        top_artist_list.append(get_current_user_top_artist_name(top_artists, i))

    return top_artist_list


# returns the artist name of a top track
def get_current_user_top_track_artist(top_artist, index):
    if top_artist:
        return top_artist["items"][index]["artists"][0]["name"]
    else:
        return "Top Track Name Unavailable."


# implements sp.search()
def search(query, limit, type_content):
    return sp.search(query, limit=limit, type=type_content)


# gets a song uri. Implements sp.track()
def get_queue_uri(search_obj):
    response = search_obj["tracks"]["items"][0]["external_urls"]["spotify"]
    return sp.track(response)["uri"]


# implements sp.add_to_queue()
def add_to_queue(response_uri):
    sp.add_to_queue(response_uri)
    return


# skips the current playback to the next song
def next_track():
    try:
        sp.next_track()
    except SpotifyException:
        return "Cannot go to next track"


# goes back to the previous track
def previous_track():
    try:
        sp.previous_track()
    except SpotifyException:
        return "Cannot go to the previous track"


# button now pauses playback
def pause_playback():
    try:
        sp.pause_playback()
    except SpotifyException:
        return "Cannot pause current playback"


# button now resumes playback
def resume_playback():
    try:
        sp.start_playback()
    except SpotifyException:
        return "Cannot resume playback"


# generates an artist recommendation based on the current artist
def get_related_artists(artist_id):
    # list to be populated with related artists
    related_artists = []
    if artist_id is None:
        related_artists.append("No playback detected.")
    else:
        try:
            # artist_related_artits find related artist based on artist URI
            response = sp.artist_related_artists(artist_id)
        except SpotifyException:
            return "Cannot find current artist."

        # appends artist name to related artist list.
        for index, artist in enumerate(response["artists"]):
            related_artists.append(artist["name"])

    return related_artists
