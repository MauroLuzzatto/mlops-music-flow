from music_flow import SpotifyAPI


class BatchSpotifyAPI(SpotifyAPI):
    def __init__(self):
        super().__init__()

    def get_batch_audio_features(self, track_ids: list[str]):
        if len(track_ids) > 100:
            raise Exception("too many values requested")

        ids_string = ",".join(track_ids)
        url = f"https://api.spotify.com/v1/audio-features?ids={ids_string}"
        response, status_code = self.get_request(url)
        return response, status_code

    def get_batch_tracks(self, track_ids: list[str]):
        if len(track_ids) > 50:
            raise Exception("too many values requested")

        ids_string = ",".join(track_ids)
        url = f"https://api.spotify.com/v1/tracks?ids={ids_string}"
        response, status_code = self.get_request(url)
        return response, status_code

    def get_batch_artists(self, artist_ids: list[str]):
        if len(artist_ids) > 50:
            raise Exception("too many values requested")

        ids_string = ",".join(set(artist_ids))
        url = f"https://api.spotify.com/v1/artists?ids={ids_string}"
        response, status_code = self.get_request(url)
        return response, status_code

    @staticmethod
    def convert_batch_response_to_dict(responses) -> dict:
        try:
            output_dict = {audio["id"]: audio for audio in responses}
        except:
            output_dict = {}
        return output_dict


if __name__ == "__main__":
    from pprint import pprint

    multi = BatchSpotifyAPI()
    ids = ["1qRpqv3I1t1kRol36KAfEi", "4knd2gQyr2DTRLfJDHcyMS"]
    response, status_code = multi.get_batch_audio_features(ids)
    pprint(response)

    response, status_code = multi.get_multiple_tracks(ids)
    print(response)

    # output = [audio["id"] for audio in response["audio_features"]]
    # print(output)

    # output_dict = {audio["id"]: audio for audio in response["audio_features"]}
    # pprint(output_dict)
