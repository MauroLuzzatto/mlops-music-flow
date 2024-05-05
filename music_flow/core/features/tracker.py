from typing import Optional, Tuple
import logging
import logging.config
from dataclasses import dataclass
from typing import Callable, Optional, Tuple

from music_flow.config import settings
from music_flow.core.spotify_api import SpotifyAPI

# from music_flow.core.features.models.audio_features import AudioFeatures

# from music_flow.core.features.track import Track

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


spotify_api = SpotifyAPI()


@dataclass
class Endpoint:
    """Class for defintion the API endpoints that called."""

    name: str
    func: Callable
    description: str


class Tracker:
    def __init__(
        self,
        name: str,
        artist: str,
        track_id: Optional[str] = None,
        artist_id: Optional[str] = None,
    ):
        self.name = name
        self.artist = artist  # should this be a list of artists?

        if track_id:
            self.track_id: str = track_id
        if artist_id:
            self.artist_id: str = artist_id

        if not track_id or not artist_id:
            response, status_code = self._search_track()
            if not track_id:
                self.track_id = self._get_track_id(response)
            if not artist_id:
                self.artist_id = self._get_artist_id(response)

        # collect all the responses from the API
        # self._responses = {}
        # for name, call_endpoint in [
        #     ("track", self._get_track),
        #     # ("audio_features", self._get_audio_features),
        #     # ("audio_analysis", self._get_audio_analysis),
        #     # ("artist", self._get_artist),
        # ]:
        #     response, status_code = call_endpoint()
        #     self._responses[name] = {
        #         "response": response,
        #         "status_code": status_code,
        #     }

        # self.artist_dict = self.get_artist_data(self._responses["artist"]["response"])
        # self.audio_features = AudioFeatures(
        #     **self._responses["audio_features"]["response"]
        # )
        # self.track = Track(**self._responses["track"]["response"])

    def _search_track(self) -> Tuple[dict, int]:
        url = spotify_api.search_track_url(self.name, self.artist)
        response, status_code = spotify_api.get_request(url)
        logger.debug(f"status_code: {status_code}")
        return response, status_code

    def _get_track_id(self, response) -> Optional[str]:
        """get the track_id from the Spotify API for a given track"""

        track_id = None
        try:
            track_id = response["tracks"]["items"][0]["id"]
        except (IndexError, KeyError):
            logger.debug("Failed to get track_id from Spotify API.")
        return track_id

    def _get_artist_id(self, response) -> Tuple[Optional[str], int]:
        artist_id = None
        try:
            artist_id = response["tracks"]["items"][0]["artists"][0]["id"]
        except (IndexError, KeyError):
            logger.debug("Failed to get artist_id from Spotify API.")
        return artist_id

    def _get_track(self) -> Tuple[dict, int]:
        """get the track data from the Spotify API for a given track"""
        endpoint_name = "track"
        response, status_code = spotify_api.get_track(self.track_id)
        logger.debug(f"endpoint: {endpoint_name}, status_code: {status_code}")
        return response, status_code

    # def _get_audio_features(self) -> Tuple[dict, int]:
    #     """wip"""
    #     endpoint_name = "audio_features"
    #     response, status_code = spotify_api.get_audio_features(self.track_id)
    #     logger.debug(f"endpoint: {endpoint_name}, status_code: {status_code}")
    #     return response, status_code

    # def _get_audio_analysis(self) -> Tuple[dict, int]:
    #     """wip"""
    #     endpoint_name = "audio_analysis"
    #     response, status_code = spotify_api.get_audio_analysis(self.track_id)
    #     logger.debug(f"endpoint: {endpoint_name}, status_code: {status_code}")
    #     return response, status_code

    # def _get_artist(self) -> Tuple[dict, int]:
    #     """wip"""
    #     endpoint_name = "artist"
    #     response, status_code = spotify_api.get_artist(self.artist_id)
    #     logger.debug(f"endpoint: {endpoint_name}, status_code: {status_code}")
    #     return response, status_code

    # def get_artist_data(self, response: dict) -> dict:

    #     artist_dict = {
    #         "name": response["name"],
    #         "followers": response["followers"]["total"],
    #         "genres": response["genres"],
    #         "popularity": response["popularity"],
    #     }

    #     return artist_dict

    # def _extract_metadata(response: dict) -> dict:
    #     """get the song data from the spotify api track response for a given track"""
    #     try:
    #         metadata = {
    #             "name": response["name"],
    #             "album": response["album"]["name"],
    #             "artist": [_artist["name"] for _artist in response["album"]["artists"]],
    #         }
    #     except (IndexError, KeyError) as e:
    #         print(f"Error: could not get the metadata - {e}")
    #         logger.debug("Failed to extract metadata from Spotify API.")
    #     return metadata


if __name__ == "__main__":
    # tracker = Tracker("The Less I Know The Better", "Tame Impala")
    tracker = Tracker("Dancing in the Moonlight", "Toploader")

    print(tracker.track_id)
    print(tracker.artist_id)
    # print(tracker._get_track())
    # print(tracker._get_audio_features())
    # print(tracker._get_audio_analysis())
    # print(tracker.artist_dict)
    # print(tracker.audio_features)
    print(tracker.track)

    import json

    print(json.dumps(tracker._responses["audio_analysis"]["response"]))

    from music_flow.core.features.models.track import Track

    # print(Track(**tracker._responses["track"]["response"]))


# Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.
