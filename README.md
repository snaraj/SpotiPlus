# SpotiPlus - Enhanced Spotify Experience
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Description

SpotiPlus aims to enhance the spotify user experience by creating a data rich dashboard. The dashboard integrates the ability to manipulate current playback and a user's queue. Information about the current playback is then sent to other API's in exchange for song lyrics with annotations and a detailed description of the artist and song.

## Installation
##### Note: this project assumes a default python version of 3 or later. It has not been tested on any 2.x distribution.

1. Setting up our environment.
	1. I like to use a tool called [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) to manage my virtual environments.

	![virtual env setup](https://github.com/snaraj/SpotiPlus/blob/master/assets/images/virtual_env_setup1.png?raw=true)

	2. After installing the virtual environment, we need to install our dependencies for this project. First, run ```npm install``` and then run ```pip install requirements.txt``` while on the root of the project.
