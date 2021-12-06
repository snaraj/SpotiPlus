import spotipy
import requests

from spotiPlus.spotify.spotify_utils import *
from spotiPlus.genius.genius_utils import *
from spotiPlus.lastfm.lastfm_utils import *

from flask import render_template, Blueprint, url_for, redirect, request
from typing import Dict

from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException


bp = Blueprint('', __name__, url_prefix='')

# saved tracks by recent
saved_tracks_list = get_current_saved_tracks_list(1)
saved_recent_tracks = saved_tracks_list[0]
saved_recent_artist = saved_tracks_list[1]

# song paths to genius pages for most recent saved songs
song_paths = get_genius_path(saved_recent_artist, saved_recent_tracks)

# current user info
user_display_name = get_current_user_display_name(get_current_user())
user_display_image = get_current_user_display_picture(get_current_user())

# current playback
current_playback_song_title = get_current_user_current_playback_song_title(get_current_user_current_playback())
current_playblack_song_artist = get_current_user_current_playback_song_artist(get_current_user_current_playback())
current_playback_image_uri = get_current_playback_image(get_current_user_current_playback())

# current song lyrics from genius
current_song_lyrics = get_song_lyrics(current_playblack_song_artist, current_playback_song_title)


# current user top artist and songs
user_top_artist_list = generate_top_artist_list(5)
user_top_songs_list = generate_top_track_list(5)

#last fm artist and song summary:
artist_summary = get_artist_summary(current_playblack_song_artist)
song_summary = get_track_summary(current_playback_song_title, current_playblack_song_artist)


# variables being passed to the home.html template.
home_template_variables = {
	'songs' : saved_recent_tracks,
	'artists' : saved_recent_artist,
	'current_song_lyrics' : current_song_lyrics,
	'current_playback_image_uri' : current_playback_image_uri,
	'paths' : song_paths,
	'user_display_name' : user_display_name,
	'user_display_image' : user_display_image,
	'current_playback_song_title' : current_playback_song_title,
	'current_playblack_song_artist' : current_playblack_song_artist,
	'current_user_top_tracks' : user_top_artist_list,
	'current_user_top_artist' : user_top_songs_list,
	'artist_summary' : artist_summary,
	'song_summary' : song_summary,
}

@bp.route('/', methods=['GET', 'POST'])
def spotify():
	#updating the queue. 
	if request.method == 'POST':
		if request.form['Submit'] == 'queue_submit':
			song_name = request.form['song_name']
			artist_name = request.form['artist_name']
			search_query = song_name + ' ' + artist_name
			search_response = search(search_query, 1, 'track')
			
			#handles not finding the right song on queue.
			if search_response['tracks']['total'] != 0:
				try:
					add_to_queue(get_queue_uri(search_response))
				except SpotifyException:
					print('No device playing.')
			else:
				print('No song found.')

		#skipping to the next song
		if request.form['Submit'] == '>>':
			next_track()
		#previous song
		if request.form['Submit'] == '<<':
			previous_track()
		#pause playback
		if request.form['Submit'] == 'pause':
			pause_playback()
		#resume playback
		if request.form['Submit'] == 'play':
			resume_playback()

	return render_template('home/home.html', **home_template_variables, zip=zip)




