from flask import Flask, escape, request
import mysql_helper
import json
import ytdl_helper
from spotifyHelper import SpotifyHelper
import stem_creation_spleeter
import gcp_storage_helper
import audio_manip
from os import listdir
from os.path import isfile, join, join, dirname
import os
from dotenv import load_dotenv
import logging

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

BUCKET_NAME = os.environ.get("GCP_BUCKET_NAME")

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


# song_dst will be transformed to match song_src key and tempo
def transform_song(song_src_yt_id, song_dst_yt_id):
    _, _, src_track, src_artist, src_tempo, src_key, src_is_minor = mysql_helper.fetch_song(song_src_yt_id)
    _, _, dst_track, dst_artist, dst_tempo, dst_key, dst_is_minor = mysql_helper.fetch_song(song_dst_yt_id)

    # fetch source stems
    src_stems_exist, src_stems = mysql_helper.fetch_stems(song_src_yt_id, src_tempo, src_key, src_is_minor)

    if not src_stems_exist:
        # this is a big problem lmao F
        pass

    # check if dst stems exist
    dst_stems_exist, dst_stems = mysql_helper.fetch_stems(song_dst_yt_id, src_tempo, src_key, src_is_minor)

    if not dst_stems_exist:
        # fetch original stems
        logging.info("Could not find transformed stems, making it")
        _, dst_stems = mysql_helper.fetch_stems(song_dst_yt_id, dst_tempo, dst_key, dst_is_minor)

        for _, stem_type, bucket_name, file_name, stem_key, stem_tempo, _ in dst_stems:
            file_path = file_name.split(".")[0]
            transformed_stem = \
                audio_manip.transform(file_path, stem_tempo, src_tempo, stem_key, src_key, new_key_minor=src_is_minor)
            gcp_storage_helper.upload_blob(BUCKET_NAME, transformed_stem, transformed_stem)
            gcp_storage_helper.post_upload(song_dst_yt_id, bucket_name, stem_type, transformed_stem, transformed_stem,
                                           src_tempo, src_key, 0)

    logging.info("Fetching transformed stems")
    _, dst_stems = mysql_helper.fetch_stems(song_dst_yt_id, src_tempo, src_key, src_is_minor)
    output = []

    for _, stem_type, bucket_name, file_name, _, _, _ in src_stems:
        output.append((stem_type, bucket_name, file_name))

    for _, stem_type, bucket_name, file_name, _, _, _ in dst_stems:
        output.append((stem_type, bucket_name, file_name))

    return output


def download_song(search_query):
    yt_metadata = ytdl_helper.download(search_query)

    # get {'id': 'Ce1r05SSbwA', 'artist': 'Santana', 'track': 'Smooth'} or None

    if yt_metadata is None:
        # raise error
        pass

    youtube_id = yt_metadata["id"]

    logging.info("Found metdata for song: " + str(yt_metadata))

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

    if is_minor:
        song_key = audio_manip.minor_to_major_pitch_class(song_key)

    for file in only_files:
        stem_type = file.split(".")[0]
        mp3_file = audio_manip.dump_wav(file)
        file_path = stems_path + mp3_file
        gcp_storage_helper.upload_blob(BUCKET_NAME, file_path, file_path)
        gcp_storage_helper.post_upload(youtube_id, BUCKET_NAME, stem_type, file_path, file_path, tempo, song_key,
                                       yt_metadata["duration"])

    return youtube_id


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

    status, songList = mysql_helper.fetch_song_list()
    cached_yids = []
    yids = ["", ""]

    for yid, _, _ in songList:
        cached_yids.append(yid)

    logging.info("Cached yids: " + str(cached_yids))

    for i in range(len(yids)):
        if queries[i] not in cached_yids:
            yids[i] = download_song(queries[i])
        else:
            yids[i] = queries[i]

    stems_info = transform_song(yids[0], yids[1])
    return json.dumps(stems_info)


@app.route('/cached-songs')
def getCachedSongs():
    status, songList = mysql_helper.fetch_song_list()
    if not status:
        return json.dumps([])
    else:
        return json.dumps(songList)


app.run()