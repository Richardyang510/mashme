import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv
import logging


logging.basicConfig(level=logging.INFO)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

AUDIO_FEATURES_URL = "https://api.spotify.com/v1/audio-features"
SEARCH_URL = "https://api.spotify.com/v1/search"

SPOTIFY_AUTH_TOKEN = os.environ.get("SPOTIFY_AUTH_TOKEN")


class SpotifyHelper:
    HEADER = {"Authorization": "Bearer " + SPOTIFY_AUTH_TOKEN}

    @staticmethod
    def getSongId(name, artist):
        """
        Gets the id of the first song that matches the search criteria
        """
        r = requests.get(SEARCH_URL, params={'q': name or '' + ' artist:' + artist or '', 'type': 'track'}, headers=SpotifyHelper.HEADER)
        logging.info(r)
        return r.json()['tracks']['items'][0]['id']

    @staticmethod
    def getAudioFeaturesByIds(ids):
        """
        Gets the audio features of the songs corresponding to the parameter ids
        A sample feature object looks like this:
        {
            "danceability": 0.808,
            "energy": 0.626,
            "key": 7,
            "loudness": -12.733,
            "mode": 1,
            "speechiness": 0.168,
            "acousticness": 0.00187,
            "instrumentalness": 0.159,
            "liveness": 0.376,
            "valence": 0.369,
            "tempo": 123.99,
            "type": "audio_features",
            "id": "4JpKVNYnVcJ8tuMKjAj50A",
            "uri": "spotify:track:4JpKVNYnVcJ8tuMKjAj50A",
            "track_href": "https://api.spotify.com/v1/tracks/4JpKVNYnVcJ8tuMKjAj50A",
            "analysis_url": "http://echonest-analysis.s3.amazonaws.com/TR/WhpYUARk1kNJ_qP0AdKGcDDFKOQTTgsOoINrqyPQjkUnbteuuBiyj_u94iFCSGzdxGiwqQ6d77f4QLL_8=/3/full.json?AWSAccessKeyId=AKIAJRDFEY23UEVW42BQ&Expires=1458063189&Signature=JRE8SDZStpNOdUsPN/PoS49FMtQ%3D",
            "duration_ms": 535223,
            "time_signature": 4
        }
        """
        r = requests.get(AUDIO_FEATURES_URL, params={'ids': ','.join(ids)}, headers=SpotifyHelper.HEADER)
        return r.json()['audio_features']


def sampleUsage():
    songList = [
        # [song name, artist]
        ['smooth', 'santana'],
        ['the sound of silence', 'simon']
    ]

    ids = [SpotifyHelper.getSongId(song[0], song[1]) for song in songList]
    features = SpotifyHelper.getAudioFeaturesByIds(ids)
    return features


# print(sampleUsage())
