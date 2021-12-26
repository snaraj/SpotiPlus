import spotipy
import requests

from spotiPlus.spotify.spotify_utils import *
from spotiPlus.genius.genius_utils import *
from spotiPlus.lastfm.lastfm_utils import *

from flask import render_template, Blueprint, url_for, redirect, request, jsonify
from typing import Dict

from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException

bp = Blueprint("", __name__, url_prefix="")

# set of variables that get called throughout the app
# dictionary holding information about current playback
current_playback = get_current_user_current_playback()
# get the uri of the current artist
artist_uri = get_current_artist_uri(current_playback)
artist_id = get_current_artist_id(current_playback)
# get the current user
current_user = get_current_user()

# current user info
user_display_name = get_current_user_display_name(current_user)
user_display_image = get_current_user_display_picture(current_user)

# current playback
current_playback_song_title = get_current_user_current_playback_song_title(
    current_playback
)
current_playback_song_artist = get_current_user_current_playback_song_artist(
    current_playback
)
current_playback_image_uri = get_current_playback_image(current_playback)

# saved tracks by recent
saved_tracks_list = get_current_saved_tracks_list(1)
saved_recent_tracks = saved_tracks_list[0]
saved_recent_artist = saved_tracks_list[1]

# song paths to genius pages for most recent saved songs
song_paths = get_genius_path(saved_recent_artist, saved_recent_tracks)

# recommended artists and songs based on current playback
recommended_artist = get_related_artists(artist_uri)

# current song lyrics from genius
current_song_lyrics = get_song_lyrics(
    current_playback_song_artist, current_playback_song_title
)

# top songs and artist from current user
user_top_artist_list = generate_top_artist_list(5)
user_top_songs_list = generate_top_track_list(5)

# generates artist and track summary from LastFM API:
artist_summary = get_artist_summary(current_playback_song_artist)
song_summary = get_track_summary(
    current_playback_song_title, current_playback_song_artist
)

# variables being passed to the home.html template.
home_template_variables = {
    "songs": saved_recent_tracks,
    "artists": saved_recent_artist,
    "current_song_lyrics": current_song_lyrics,
    "current_playback_image_uri": current_playback_image_uri,
    "paths": song_paths,
    "user_display_name": user_display_name,
    "user_display_image": user_display_image,
    "current_playback_song_title": current_playback_song_title,
    "current_playback_song_artist": current_playback_song_artist,
    "current_user_top_tracks": user_top_artist_list,
    "current_user_top_artist": user_top_songs_list,
    "artist_summary": artist_summary,
    "song_summary": song_summary,
    "recommended_artist": recommended_artist,
}

#AJAX route
@bp.route('/update_playback', methods=['POST'])
def updateplayback():
    #update current playback information
    current_playback = get_current_user_current_playback()
    current_playback_song_title = get_current_user_current_playback_song_title(current_playback)
    current_playback_song_artist = get_current_user_current_playback_song_artist(current_playback)
    current_playback_image_uri = get_current_playback_image(current_playback)

    #update current playback song and artist information
    artist_summary = get_artist_summary(current_playback_song_artist)
    song_summary = get_track_summary(current_playback_song_title, current_playback_song_artist)

    #update lyrics
    current_song_lyrics = get_song_lyrics(current_playback_song_artist, current_playback_song_title)

    #update recommendations
    artist_uri = get_current_artist_uri(current_playback)
    recommended_artist = get_related_artists(artist_uri)

    new_song_info = {
        "current_playback_song_title": current_playback_song_title,
        "current_playback_song_artist": current_playback_song_artist,
        "current_playback_image_uri": current_playback_image_uri,
    }

    return jsonify('', render_template('home/current_playback_model.html'), new_song_info) 

@bp.route("/", methods=["GET", "POST"])
def spotify():
    # updating the queue.
    if request.method == "POST":
        if request.form["Submit"] == "Queue":
            song_name = request.form["song_name"]
            artist_name = request.form["artist_name"]
            search_query = song_name + " " + artist_name
            search_response = search(search_query, 1, "track")

            # handles not finding the right song on queue.
            if search_response["tracks"]["total"] != 0:
                try:
                    add_to_queue(get_queue_uri(search_response))
                except SpotifyException:
                    print("No device playing.")
            else:
                print("No song found.")

        # skipping to the next song
        if request.form["Submit"] == ">>":
            next_track()
        # previous song
        if request.form["Submit"] == "<<":
            previous_track()
        # pause playback
        if request.form["Submit"] == "pause":
            pause_playback()
        # resume playback
        if request.form["Submit"] == "play":
            resume_playback()

    return render_template("home/home.html", **home_template_variables, zip=zip)
