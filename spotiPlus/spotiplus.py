import spotipy
import requests

from spotiPlus.spotify.spotify_utils import get_current_saved_tracks_list, get_current_user_display_name, get_current_user, get_current_user_display_picture, get_current_user_current_playback_song_title, get_current_user_current_playback, get_current_user_current_playback_song_artist, get_current_user_top_tracks, generate_top_artist_list, generate_top_track_list, search, get_queue_uri, add_to_queue

from flask import render_template, Blueprint, url_for, redirect, request
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
from typing import Dict
from lyricsgenius import Genius


bp = Blueprint('', __name__, url_prefix='')


#setting up for lyricsgenius to grab lyrics
GENIUS_ACCESS_TOKEN = '6QGMcUYCz4eBOK1_tIwMCXaGk1CEpjpRrAOGcNKifCEb8i756uXv1wBhkgesQGHX'
genius = Genius(GENIUS_ACCESS_TOKEN)

#accessing genius API
genius_headers = {
	'Authorization' : 'Bearer ' + GENIUS_ACCESS_TOKEN,
}

def generate_payload(artist_name: str, song_name: str) -> Dict[str,str]:
	return {'q' : f'{artist_name} {song_name}'}

def get_song_lyrics_from_genius(artist_name: str, song_name: str) -> str:
	artist = genius.search_artist(artist_name, max_songs=1)
	song = genius.search_song(song_name, artist_name)
	return song.lyrics


# ---> populating the spoti+ template
#general
song_paths = []
saved_lyrics = []

# Working with saved tracks
saved_tracks_list = get_current_saved_tracks_list(1)
print(saved_tracks_list)
saved_recent_tracks = saved_tracks_list[0]
saved_recent_artist = saved_tracks_list[1]


# currently logged in user information:
user_display_name = get_current_user_display_name(get_current_user())
user_display_image = get_current_user_display_picture(get_current_user())

# current playback
current_playback_song_title = get_current_user_current_playback_song_title(get_current_user_current_playback())
current_playblack_song_artist = get_current_user_current_playback_song_artist(get_current_user_current_playback())

# user's top artist and songs
user_top_artist_list = generate_top_artist_list(5)
user_top_songs_list = generate_top_track_list(5)


#uses the artist and song name to grab the genius path to the song page.
for artist_name, song_name in zip(saved_recent_artist, saved_recent_tracks):
	payload = generate_payload(artist_name, song_name)
	search_response = requests.get('https://api.genius.com/search/', headers=genius_headers, params=payload)
	song_hits = search_response.json()['response']['hits']

	if song_hits:
		song_id = song_hits[0]['result']['id']
		song_path_response = requests.get(f'https://api.genius.com/songs/{song_id}', headers=genius_headers)
		song_path = song_path_response.json()['response']['song']['path']
		song_paths.append('https://genius.com'+song_path)
		saved_lyrics.append(get_song_lyrics_from_genius(artist_name, song_name))
	else:
		song_paths.append("No Genius page avaliable.")
		saved_lyrics.append('Lyrics not avaliable.')


#Variables being passed to the home.html template.
home_template_variables = {
	'songs' : saved_recent_tracks,
	'artists' : saved_recent_artist,
	'lyrics' : saved_lyrics,
	'paths' : song_paths,
	'user_display_name' : user_display_name,
	'user_display_image' : user_display_image,
	'current_playback_song_title' : current_playback_song_title,
	'current_playblack_song_artist' : current_playblack_song_artist,
	'current_user_top_tracks' : user_top_artist_list,
	'current_user_top_artist' : user_top_songs_list,
}

@bp.route('/', methods=['GET', 'POST'])
def spotify():
	#updating the queue. 
	if request.method == 'POST':
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


	return render_template('home/home.html', **home_template_variables, zip=zip)



# Use div class='lyrics' to scrape the lyrics from the genius website,
# display them next to the song in the table.

#create a control menu, next 



