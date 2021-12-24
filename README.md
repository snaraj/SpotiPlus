# SpotiPlus - Enhanced Spotify Experience
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Description

SpotiPlus aims to enhance the spotify user experience by creating a data rich dashboard. The dashboard integrates the ability to manipulate current playback and a user's queue. Information about the current playback is then sent to other API's in exchange for song lyrics with annotations and a detailed description of the artist and song.

## Installation
##### Note: this project assumes a default python version of 3 or later. It has not been tested on any 2.x distribution.

1. Setting up our environment
	1. I like to use a tool called [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) to manage my virtual environments.

	![virtual env setup](https://github.com/snaraj/SpotiPlus/blob/master/assets/images/virtual_env_setup1.png?raw=true)

	2. After installing the virtual environment, we need to install our dependencies for this project. First, run ```npm install``` and then run ```pip install -r requirements.txt``` while on the root of the project.

2. Setting up environment variables
	1. Since this project is made using Flask, and our app name is not app.py, we need to tell Flask the name of the app. We also need to let Flask know that we are working on a development environment.

	![Flask set up](https://github.com/snaraj/SpotiPlus/blob/master/assets/images/flask_setup_1.png?raw=true)

3. Installing tailwindCSS
	1. Lastly, we need to make sure that our CSS is working properly. Simply run the command ```npm install -D tailwindcss``` while on the root of the project.


## Usage
1. To run the app enter ```flask run``` on the root folder.
![flask run](https://github.com/snaraj/SpotiPlus/blob/master/assets/images/flask%20run.png?raw=true)

2. If this is your first time using spotiPlus, you will be automatically redirected to spotify's authentication page, sign in.

3. Once logged in, you will be redirected back to spotiPlus's dashboard, when nothing is playing, it will look like this.

![No playback](https://github.com/snaraj/SpotiPlus/blob/master/assets/images/no%20playback%20dashboard.png?raw=true)

4. On the contrary, with playback the app will look like this.

![playback](https://github.com/snaraj/SpotiPlus/blob/master/assets/images/playback%20dashboard.png?raw=true)

5. Using the queue is simple, just type an artist and a song.

![queue](https://github.com/snaraj/SpotiPlus/blob/master/assets/images/queue%20new%20song.png?raw=true)

## Credits
List of relevant links:
 - Spotify API: https://developer.spotify.com/documentation/web-api/
 - SpotiPy Library: https://spotipy.readthedocs.io/en/2.19.0/
 - Genius API: https://docs.genius.com/
 - LastFM API: https://www.last.fm/api
 - Flask Docs: https://flask.palletsprojects.com/en/2.0.x/