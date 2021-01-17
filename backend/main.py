from flask import Flask, escape, request
import mysql_helper
import json
import ytdl_helper
from spotifyHelper import SpotifyHelper
import stem_creation_spleeter
import gcp_storage_helper
import audio_manip
from os import listdir
from os.path import isfile, join

BUCKET_NAME = "dropdowns-stems"

app = Flask(__name__)


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/smooth-test')
def smooth_test():
    urls = [
        'https://storage.googleapis.com/download/storage/v1/b/dropdowns-stems/o/Smooth_133_5.mp3?alt=media',
        'https://storage.googleapis.com/download/storage/v1/b/dropdowns-stems/o/Smooth_100_11.mp3?alt=media'
    ]
    return ','.join(urls)

@app.route('/mix/<query>', methods=['POST'])
def mix(query):
    print("The user has entered: " + query)
    queries = query.split(';')

    for q in queries:
        title, artist = q.split(',')
        yt_metadata = ytdl_helper.download(title + " " + artist)

        # get {'id': 'Ce1r05SSbwA', 'artist': 'Santana', 'track': 'Smooth'} or None

        if yt_metadata is None:
            # raise error
            pass

        youtube_id = yt_metadata["id"]

        spotify_id = SpotifyHelper.getSongId(yt_metadata["track"], yt_metadata["artist"])
        spotify_features = SpotifyHelper.getAudioFeaturesByIds([spotify_id])

        tempo = spotify_features[0]["tempo"]
        song_key = spotify_features[0]["key"]
        is_minor = not bool(spotify_features[0]["mode"])


        mysql_helper.insert_song(youtube_id, spotify_id, yt_metadata["track"], yt_metadata["artist"],
                                tempo, song_key, is_minor)

        stem_creation_spleeter.split_song(f"{youtube_id}.mp3", f"output")

        stems_path = f"output/{youtube_id}/"

        only_files = [f for f in listdir(stems_path) if isfile(join(stems_path, f))]

        for file in only_files:
            stem_type = file.split(".")[0]
            mp3_file = audio_manip.dump_wav(file)
            file_path = stems_path + mp3_file
            gcp_storage_helper.upload_blob(BUCKET_NAME, file_path, file_path)
            gcp_storage_helper.post_upload(youtube_id, BUCKET_NAME, stem_type, file_path, file_path, tempo, song_key, yt_metadata["duration"])

    return json.dumps([])


@app.route('/cached-songs')
def getCachedSongs():
    status, songList = mysql_helper.fetch_song_list()
    if not status:
        return json.dumps([])
    else:
        return json.dumps(songList)


app.run()