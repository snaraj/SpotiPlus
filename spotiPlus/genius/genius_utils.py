import requests

from spotiPlus.genius.secrets import GENIUS_ACCESS_TOKEN
from lyricsgenius import Genius
from typing import Dict, List

genius = Genius(GENIUS_ACCESS_TOKEN)

headers = {
	'Authorization' : 'Bearer ' + GENIUS_ACCESS_TOKEN,
}

song_paths = []

def generate_payload(artist_name: str, song_name: str) -> Dict[str,str]:
	return {'q' : f'{artist_name} {song_name}'}

def get_song_lyrics(artist_name: str, song_name: str) -> str:
	lyrics = 'No lyrics avaliable.'
	
	if artist_name == 'Artist Unavailable.' or song_name == 'Title Unavailable.':
		return lyrics
	else: 
		artist = genius.search_artist(artist_name, max_songs=1, allow_name_change=True)
		song = genius.search_song(song_name, artist_name)
		lyrics = song.lyrics
		lyrics = clean_lyrics(lyrics)
	
	return lyrics

def clean_lyrics(lyrics: str) -> str:
	lyrics = lyrics.lstrip()
	lyrics = lyrics.rstrip()
	lyrics = lyrics.replace('more142EmbedShare URLCopyEmbedCopy', '')
	lyrics = lyrics.replace('URLCopyEmbedCopy', '')
	lyrics = lyrics.replace('EmbedShare', '')

	return lyrics

def get_genius_path(artists_list: List[str], songs_list: List[str]) -> List[str]:
	
	paths = []

	for song, artist in zip(artists_list, songs_list):
		
		payload = generate_payload(artist, song)
		search_response = requests.get('https://api.genius.com/search/', headers=headers, params=payload)
		song_hits = search_response.json()['response']['hits']

		if song_hits:
			song_id = song_hits[0]['result']['id']
			song_path_response = requests.get(f'https://api.genius.com/songs/{song_id}', headers=headers)
			song_path = song_path_response.json()['response']['song']['path']
			paths.append('https://genius.com'+song_path)
		else:
			paths.append(f"No Genius page avaliable for {song} by {artist}.")

	return paths

















