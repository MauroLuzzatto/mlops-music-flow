import json
import logging
import os
import time
from typing import Tuple, Optional

import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from requests.utils import requote_uri
from urllib3.util.retry import Retry
from functools import lru_cache

from music_flow.core.utils import path_env

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

load_dotenv(path_env)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise Exception("CLIENT_ID or CLIENT_SECRET not set in .env file")

status_codes = []


class SpotifyAPI:
    def __init__(self):
        self.headers = self.get_headers()
        retry = Retry(connect=1, backoff_factor=0.5)
        self.adapter = HTTPAdapter(max_retries=retry)

    def get_headers(self):
        grant_type = "client_credentials"
        body_params = {"grant_type": grant_type}
        auth = (CLIENT_ID, CLIENT_SECRET)

        url = "https://accounts.spotify.com/api/token"
        response = requests.post(url, data=body_params, auth=auth, verify=True)  # type: ignore

        if response.status_code != 200:
            print("bad credentials")
            print(response)
            exit(1)

        token = json.loads(response.text)["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        return headers

    @lru_cache(maxsize=None)
    def get_request(self, url: str, max_retries: int = 3, rate_limit: int = 1):
        """TODO: move to Base class
        Fetches data from the specified URL while respecting the rate limit.

        Args:
            url (str): The URL of the API endpoint.
            rate_limit (int): The desired rate limit in requests per second (default: 1).
            max_retries (int): The maximum number of retries if rate limit is exceeded (default: 3).

        Returns:
            Tuple(dict, int): The JSON response from the API and the status code

        """

        retries = 0
        start_time = time.time()

        while True:
            with requests.Session() as session:
                session.mount("https://", self.adapter)
                response = session.get(url=url, headers=self.headers)

            if response.status_code == 200 or response.status_code == 404:
                return response.json(), response.status_code

            if response.status_code == 429 or response.status_code == 503:
                if retries >= max_retries:
                    raise Exception("Rate limit exceeded after multiple retries.")

                print(response)
                print("retry")
                retry_after = int(response.headers.get("Retry-After", 1))
                logger.debug(retry_after)
                print("retry_after", retry_after)

                elapsed_time = time.time() - start_time

                # Calculate the time to sleep based on the rate limit and elapsed time
                sleep_time = (
                    max(0, (retries + 1) / rate_limit - elapsed_time) + retry_after + 1
                )
                time.sleep("sleep_time", sleep_time / 60)
                retries += 1
                continue

            print(response.status_code)
            print(response.headers)
            print(response.json())

            raise Exception(f"Request failed with status code {response.status_code}.")

    def get_post(self, url: str, params=None):
        """TODO: move to Base class"""
        if not params:
            params = {}

        with requests.Session() as session:
            session.mount("https://", self.adapter)
            response = session.post(url=url, headers=self.headers, json=params)
        return response.json(), response.status_code

    def get_playlists(self, user_id: str):
        # Second step – make a request tox any of the playlists endpoint. Make sure to set a valid value for <spotify_user>.
        url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
        response, status_code = self.get_request(url)
        return response, status_code

    def get_playlist_items(self, playlist_id: str, limit=100, offset=0):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit={limit}&offset={offset}"
        response, status_code = self.get_request(url)
        return response, status_code

    def get_track_info(self, track, artist, limit=4):
        url = f"https://api.spotify.com/v1/search?q=track:{track}%20artist:{artist}&limit={limit}&type=track"
        response, status_code = self.get_request(url)
        return response, status_code

    def get_track(self, track_id: str):
        url = f"https://api.spotify.com/v1/tracks/{track_id}"
        response, status_code = self.get_request(url)
        return response, status_code

    def get_audio_features(self, track_id: str):
        url = f"https://api.spotify.com/v1/audio-features/{track_id}"
        response, status_code = self.get_request(url)
        return response, status_code

    def get_albums(self, track_id: str):
        url = f"https://api.spotify.com/v1/albums/{track_id}"
        response, status_code = self.get_request(url)
        return response, status_code

    def get_artist(self, artist_id: str) -> Tuple[dict, int]:
        url = f"https://api.spotify.com/v1/artists/{artist_id}"
        response, status_code = self.get_request(url)
        return response, status_code

    def search_track_url(
        self, track: str, artist: Optional[str] = None, limit: int = 5
    ) -> str:

        # TODO: would be better to send the parameters as a dict
        # params = {
        #     'resource_id': '8ea44bc4-22ba-4386-b84c-1494ab28964b',
        # }
        # response = requests.get('http://www.example.com/', params=params)

        search_type = "track"
        artist = "" if not artist else artist
        track = "" if not track else track
        track = self.clean_string(track)
        artist = self.clean_string(artist)
        url = f"https://api.spotify.com/v1/search?q=track:{track} artist:{artist}&type={search_type}&limit={limit}"
        return url

    def get_audio_analysis(self, id: str):
        url = f"https://api.spotify.com/v1/audio-analysis/{id}"
        response, status_code = self.get_request(url)
        return response, status_code

    @staticmethod
    def clean_string(string):
        return requote_uri(string)
