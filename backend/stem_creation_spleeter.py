from spleeter.separator import Separator
import time


def split_song(in_path, out_path):
    separator = Separator("spleeter:4stems")

    return separator.separate_to_file(in_path, out_path)