from spleeter.separator import Separator

# in_path - path of input song(s): song.mp3
# out_path - path of output stems: vocal.wav, bass.wav, drums.wav, others.wav
# runtime is varied and long, ranges from 35-40 seconds


def split_song(in_path, out_path):
    separator = Separator("spleeter:4stems") # specifies the number of stems produced

    return separator.separate_to_file(in_path, out_path)