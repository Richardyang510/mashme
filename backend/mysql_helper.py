import mysql.connector
import os
from os.path import join, dirname
from dotenv import load_dotenv
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
create table SONGS (
    YOUTUBE_ID NVARCHAR(16) PRIMARY KEY,
    SPOTIFY_ID NVARCHAR(22),
    CREATED_TIME TIMESTAMP(6),
    TRACK_NAME NVARCHAR(256),
    TRACK_ARTIST NVARCHAR(256),
    TEMPO FLOAT,
    SONG_KEY INT,
    IS_MINOR BOOL
)
"""

stems_creation_sql = """
create table STEMS (
    ID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    CREATED_TIME TIMESTAMP(6),
    YOUTUBE_ID NVARCHAR(16),
    STEM_TYPE NVARCHAR(10),
    STEM_TEMPO FLOAT,
    STEM_KEY INT,
    BUCKET_NAME NVARCHAR(256),
    FILE_NAME NVARCHAR(256),
    FOREIGN KEY (YOUTUBE_ID) REFERENCES SONGS(YOUTUBE_ID)
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


def create_schemas():
    test_connection()
    logging.info("Creating " + songs_creation_sql)
    db_cursor = db.cursor()
    db_cursor.execute(songs_creation_sql)
    db.commit()

    logging.info("Creating " + stems_creation_sql)
    db_cursor = db.cursor()
    db_cursor.execute(stems_creation_sql)
    db.commit()

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


def insert_stems(youtube_id, bucket_name, stem_map, stem_tempo, stem_key):
    test_connection()
    db_cursor = db.cursor()

    num_stems = len(stem_map)

    sql = f"INSERT INTO {STEMS_TABLE} " \
          "(created_time, youtube_id, stem_type, stem_tempo, stem_key, bucket_name, file_name) " \
          "VALUES " + ("(current_timestamp, %s, %s, %s, %s, %s, %s)," * num_stems)[:-1]

    val_list = []

    for stem_type, file_name in stem_map:
        val_list.append([youtube_id, stem_type, stem_tempo, stem_key, bucket_name, file_name])

    val = tuple(val_list)
    logging.info(val)

    db_cursor.execute(sql, val)
    db.commit()

