import youtube_dl
import requests
import logging

logging.basicConfig(level=logging.INFO)


class MyLogger(object):
    @staticmethod
    def debug(msg):
        logging.debug(msg)

    @staticmethod
    def warning(msg):
        logging.info(msg)

    @staticmethod
    def error(msg):
        logging.error(msg)


def my_hook(d):
    if d['status'] == 'finished':
        logging.info('Done downloading, now converting ...')


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    'noplaylist': 'True',
    'outtmpl': '%(id)s.%(ext)s',
}


# either specify search phrase download("santana smooth lyrics")
# or the youtube url download("https://www.youtube.com/watch?v=????")
#
# this will download the file as {youtube_id}.mp3
def download(arg):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            requests.get(arg)
        except requests.exceptions:
            video = ydl.extract_info(f"ytsearch:{arg}", download=True)['entries'][0]["webpage_url"]
        else:
            video = ydl.extract_info(arg, download=True)

    return video
