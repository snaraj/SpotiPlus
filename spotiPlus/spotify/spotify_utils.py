import spotipy
#remove during production
import pprint
from typing import Dict, Union, List

from spotipy.oauth2 import SpotifyOAuth
from spotiPlus.spotify.secrets import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, REDIRECT_URI, SCOPE
from spotipy.exceptions import SpotifyException

#Spotify OAUTH2.0
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
	client_id=SPOTIFY_CLIENT_ID, 
	client_secret=SPOTIFY_CLIENT_SECRET, 
	redirect_uri=REDIRECT_URI, 
	scope=SCOPE))

# ---> USER PROFILE FUNCTIONS:
#retrieves the current user
def get_current_user() -> Dict[str, str]:
	#json object with detailed information about current logged in user
	current_user = sp.current_user()
	return current_user

#retrieves the current user profile picture
def get_current_user_display_picture(current_user: Dict[str, str]) -> str:
	return current_user['images'][0]['url']

#retrieves the current user display name
def get_current_user_display_name(current_user: Dict[str, str]) -> str:
	return current_user['display_name']

# ---> USER SAVED TRACKS FUNCTIONS:
#retrieve current user saved tracks
def get_current_user_saved_tracks(limit: int) -> Dict[str, str]:
	current_user_saved_tracks = sp.current_user_saved_tracks(limit=limit)
	return current_user_saved_tracks

#get_current_user_saved_tracks returns json object, this function grabs the name of a track
def get_current_user_saved_track_name(track: Dict[str, str], index: int) -> str:
	return track['items'][index]['track']['name']

#get_current_user_saved_tracks return json object, this functions grabs the name of the artist
def get_current_user_saved_track_artist_name(track: Dict[str, str], index: int) -> str:
	return track['items'][index]['track']['album']['artists'][0]['name']

#combines the previous functions above to get a list of [artist, song]
def get_current_saved_tracks_list(limit: int) -> List:
	current_saved_tracks = get_current_user_saved_tracks(limit)
	saved_artist = []
	saved_song_name = []
	for i in range(limit):
		saved_artist.append(get_current_user_saved_track_artist_name(current_saved_tracks, i))
		saved_song_name.append(get_current_user_saved_track_name(current_saved_tracks, i))
	
	res = [saved_artist, saved_song_name]
	return res

# ---> USER CURRENT PLAYBLACK FUNCTIONS:
#get current playback:
def get_current_user_current_playback() -> Union[Dict[str, str], None]:
	current_playback = None
	try:
		current_playback = sp.current_playback()
	except TypeError:
		print('No current playback.')
	
	return current_playback

#grabs the song title for the current playback
def get_current_user_current_playback_song_title(current_playback: Dict[str, str]) -> str:
	if current_playback:
		return current_playback['item']['name']
	else:
		return 'Title Unavailable.'

#grabs the song artist for the current playback
def get_current_user_current_playback_song_artist(current_playback: Dict[str, str]) -> str:
	if current_playback:
		return current_playback['item']['album']['artists'][0]['name']
	else:
		return 'Artist Unavailable.'

#grabs the imagine for the current playback
def get_current_playback_image(current_playback: Dict[str, str]) -> str:
	image_uri = 'No Image Avaliable.'
	try:
		image_uri = current_playback['item']['album']['images'][0]['url']
	except TypeError:
		print('No song is currently playing.')
	return image_uri

# ---> USER'S TOP TRACKS & ARTIST:
#returns the user's top tracks
def get_current_user_top_tracks(limit: int) -> Union[Dict[str, str], None]:
	top_tracks = None
	try:
		top_tracks = sp.current_user_top_tracks(limit=limit)
	except TypeError:
		print('Top Tracks Unavailable.')

	return top_tracks

#returns the name of a top track
def get_current_user_top_track_name(top_tracks: Dict[str, str], index: int) -> str:
	if top_tracks:
		return top_tracks['items'][index]['name']
	else:
		return 'Top Track Name Unavailable.'

def generate_top_track_list(limit: int) -> List[str]:
	top_tracks = get_current_user_top_tracks(limit)
	top_tracks_list = []
	for i in range(limit):
		top_tracks_list.append(get_current_user_top_track_name(top_tracks, i))

	return top_tracks_list

#return the user's top artists
def get_current_user_top_artists(limit: int) -> Union[Dict[str, str], None]:
	top_artists = None
	try:
		top_artists = sp.current_user_top_artists(limit=limit)
	except TypeError:
		print('Top Artists Unavailable.')

	return top_artists

def get_current_user_top_artist_name(top_artist: Dict[str, str], index) -> str:
	if top_artist:
		return top_artist['items'][index]['name']
	else:
		return 'Top artist not found.'

def generate_top_artist_list(limit: int) -> List[str]:
	top_artists = get_current_user_top_artists(limit)
	top_artist_list = []
	for i in range(limit):
		top_artist_list.append(get_current_user_top_artist_name(top_artists, i))

	return top_artist_list

#returns the artist name of a top track
def get_current_user_top_track_artist(top_artist: Dict[str, str], index: int) -> str:
	if top_artist:
		return top_artist['items'][index]['artists'][0]['name']
	else:
		return 'Top Track Name Unavailable.'

#implements sp.search()
def search(query: str, limit: str, type_content: str) -> str:
	return sp.search(query, limit=limit, type=type_content)

#gets a song uri. Implements sp.track()
def get_queue_uri(search_obj: Dict[str, str]) -> str:
	response = search_obj['tracks']['items'][0]['external_urls']['spotify']
	return sp.track(response)['uri']

#implements sp.add_to_queue() 
def add_to_queue(response_uri: str) -> None:
	sp.add_to_queue(response_uri)
	return 

#skips the current playback to the next song
def next_track() -> None:
	try:
		sp.next_track()
	except SpotifyException:
		return 'Cannot go to next track'

#goes back to the previous track
def previous_track() -> None:
	try:
		sp.previous_track()
	except SpotifyException:
		return 'Cannot go to the previous track'

def pause_playback() -> None:
	try:
		sp.pause_playback()
	except SpotifyException:
		return 'Cannot pause current playback'

def resume_playback() -> None:
	try:
		sp.start_playback()
	except SpotifyException:
		return 'Cannot resume playback'












