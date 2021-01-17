import mysql.connector
import os
from os.path import join, dirname
from dotenv import load_dotenv
from audio_manip import minor_to_major_pitch_class
import logging

logging.basicConfig(level=logging.INFO)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASS = os.getenv('MYSQL_PASS')

DB_NAME = "HTNMaster"
SONGS_TABLE = "songs"
STEMS_TABLE = "stems"

songs_creation_sql = """
create table songs (
    YOUTUBE_ID NVARCHAR(16) PRIMARY KEY,
    SPOTIFY_ID NVARCHAR(22),
    CREATED_TIME TIMESTAMP(6),
    TRACK_NAME NVARCHAR(256),
    TRACK_ARTIST NVARCHAR(256),
    TEMPO DECIMAL,
    SONG_KEY INT,
    IS_MINOR BOOL
)
"""

stems_creation_sql = """
create table stems (
    ID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    CREATED_TIME TIMESTAMP(6),
    YOUTUBE_ID NVARCHAR(16),
    STEM_TYPE NVARCHAR(32),
    STEM_TEMPO DECIMAL,
    STEM_KEY INT,
    STEM_DURATION DECIMAL,
    BUCKET_NAME NVARCHAR(256),
    FILE_NAME NVARCHAR(256),
    FOREIGN KEY (YOUTUBE_ID) REFERENCES songs(YOUTUBE_ID)
)
"""


def init_connection():
    try:
        ctx = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            db=DB_NAME
        )
        return ctx
    except RuntimeError:
        logging.error("Could not create db connection")
        exit(1)


db = init_connection()

logging.info("Database connection initialized")


def test_connection():
    global db
    if not db.is_connected():
        logging.info("Recreating data base connection")
        db = init_connection()
    else:
        db.close()
        db = init_connection()


def create_schemas():
    test_connection()
    logging.info("Creating " + songs_creation_sql)
    db_cursor = db.cursor()
    db_cursor.execute(songs_creation_sql)
    db.commit()
    db_cursor.close()

    logging.info("Creating " + stems_creation_sql)
    db_cursor = db.cursor()
    db_cursor.execute(stems_creation_sql)
    db.commit()
    db_cursor.close()

    logging.info("Schemas created")


def insert_song(youtube_id, spotify_id, track_name, track_artist, tempo, song_key, is_minor):
    test_connection()
    db_cursor = db.cursor()

    sql = f"INSERT INTO {SONGS_TABLE} (youtube_id, spotify_id, created_time, " \
          "track_name, track_artist, tempo, song_key, is_minor) " \
          "VALUES (%s, %s, current_timestamp, %s, %s, %s, %s, %s)"

    val = (youtube_id, spotify_id, track_name, track_artist, tempo, song_key, is_minor)
    logging.info(val)

    db_cursor.execute(sql, val)
    db.commit()
    db_cursor.close()


def insert_stems(youtube_id, bucket_name, stem_map, stem_tempo, stem_key, stem_duration):
    test_connection()
    db_cursor = db.cursor()

    num_stems = len(stem_map)

    sql = f"INSERT INTO {STEMS_TABLE} " \
          "(created_time, youtube_id, stem_type, stem_tempo, stem_key, stem_duration, bucket_name, file_name) " \
          "VALUES " + ("(current_timestamp, %s, %s, %s, %s, %s, %s, %s)," * num_stems)[:-1]

    val_list = []

    for stem_type, file_name in stem_map:
        val_list.append([youtube_id, stem_type, stem_tempo, stem_key, stem_duration, bucket_name, file_name])

    val = tuple(val_list)
    logging.info(val)

    db_cursor.execute(sql, val)
    db.commit()
    db_cursor.close()


def insert_stem(youtube_id, bucket_name, stem_type, file_name, stem_tempo, stem_key, stem_duration):
    test_connection()
    db_cursor = db.cursor()

    sql = f"INSERT INTO {STEMS_TABLE} " \
          "(created_time, youtube_id, stem_type, stem_tempo, stem_key, stem_duration, bucket_name, file_name) " \
          "VALUES (current_timestamp, %s, %s, %s, %s, %s, %s, %s)"

    val = (youtube_id, stem_type, stem_tempo, stem_key, stem_duration, bucket_name, file_name)
    logging.info(val)

    db_cursor.execute(sql, val)
    db.commit()
    db_cursor.close()


def fetch_song_list():
    sql = "select distinct youtube_id, track_name, track_artist " \
          f"from {SONGS_TABLE}"

    test_connection()
    db_cursor = db.cursor()
    db_cursor.execute(sql)

    result = db_cursor.fetchall()

    logging.info(sql)
    logging.info(f"Found {len(result)} songs!")

    if len(result) == 0:
        return False, []
    else:
        data = []
        for youtube_id, track_name, track_artist in result:
            data.append((youtube_id, track_name, track_artist))
        db_cursor.close()
        return True, data


def fetch_song(youtube_id):
    sql = "select youtube_id, track_name, track_artist, tempo, song_key, is_minor " \
          f"from {SONGS_TABLE} " \
          "where youtube_id = %s"

    test_connection()
    val = (youtube_id, )

    logging.info(sql)
    logging.info(val)

    db_cursor = db.cursor()
    db_cursor.execute(sql, val)

    result = db_cursor.fetchall()

    if len(result) == 0:
        return False, None, None, None, None, None, None
    else:
        for youtube_id, track_name, track_artist, tempo, song_key, is_minor in result:
            db_cursor.close()
            return True, youtube_id, track_name, track_artist, tempo, song_key, is_minor


def fetch_stems(youtube_id, tempo, song_key, is_minor):
    if is_minor:
        song_key = minor_to_major_pitch_class(song_key)

    sql = "select youtube_id, stem_type, bucket_name, file_name, stem_key, stem_tempo, stem_duration " \
          f"from {STEMS_TABLE} " \
          "where youtube_id = %s and stem_tempo = %s and stem_key = %s"

    test_connection()
    val = (youtube_id, tempo, song_key)

    logging.info(sql)
    logging.info(val)

    db_cursor = db.cursor()
    db_cursor.execute(sql, val)

    result = db_cursor.fetchall()

    if len(result) == 0:
        return False, {}
    else:
        data = []
        for youtube_id, stem_type, bucket_name, file_name, stem_key, stem_tempo, stem_duration in result:
            data.append((youtube_id, stem_type, bucket_name, file_name, stem_key, stem_tempo, stem_duration))
        db_cursor.close()
        return True, data
