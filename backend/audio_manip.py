from pydub import AudioSegment
import wave
import contextlib
import soundfile as sf
import pyrubberband as pyrb
import logging

logging.basicConfig(level=logging.INFO)


def minor_to_major_pitch_class(minor_key):
    return (minor_key + 3) % 12


# converts "{filename}.wav" to "{filename}.mp3"
def dump_wav(filename):
    logging.info(f"Converting {filename} to mp3")
    AudioSegment.from_wav(f"{filename}.wav").export(f"{filename}.mp3", format="mp3")

    return f"{filename}.mp3"


# changes tempo of "{filename}.wav" from old_bpm to new_bpm, saves to "{filename}_{new_npm}.wav"
def change_tempo(filename, old_bpm, new_bpm):
    tempo_multiplier = new_bpm / old_bpm
    logging.info(f"Loading {filename}.wav")
    y, sr = sf.read(f"{filename}.wav")

    logging.info(f"Changing tempo for {filename}.wav from {old_bpm} to {new_bpm} (factor of {tempo_multiplier})")

    y_stretched = pyrb.time_stretch(y, sr, tempo_multiplier)

    new_filename = f"{filename}_{new_bpm}"
    logging.info(f"Saving {new_filename}.wav")
    sf.write(f"{new_filename}.wav", y_stretched, sr, format='wav')

    return new_filename


# changes the key of "{filename}.wav" from old_key to new_key, saves to "{filename}_{new_key}.wav"
def change_key(filename, old_key, new_key, old_key_minor=False, new_key_minor=False):
    if old_key_minor:
        old_key = minor_to_major_pitch_class(old_key)

    if new_key_minor:
        new_key = minor_to_major_pitch_class(new_key)

    # first determine if it is closer to shift upwards or downwards
    up_transpose = ((new_key if new_key >= old_key else new_key + 12) - old_key) % 12
    down_transpose = up_transpose - 12

    logging.debug(f"old {old_key}, new {new_key}, up {up_transpose}, down {down_transpose}")

    if abs(up_transpose) < abs(down_transpose):
        transpose = up_transpose
    else:
        transpose = down_transpose

    logging.info(f"Loading file {filename}.wav")
    y, sr = sf.read(f"{filename}.wav")

    logging.info(f"Changing pitch for {filename}.wav from {old_key} to {new_key} (transpose of {transpose})")
    y_shift = pyrb.pitch_shift(y, sr, transpose)

    logging.info(f"Saving file {filename}_{new_key}.wav")
    sf.write(f"{filename}_{new_key}.wav", y_shift, sr, format='wav')

    return f"{filename}_{new_key}"


# Example usage:
#   Santana - Smooth is in key of Am (9, minor=True) with 112 bpm
#   to transform to key of F (7, minor=False) with bpm 133:
#   transform("Smooth", 112, 113, 9, 7, old_key_minor=True)
def transform(filename, old_bpm, new_bpm, old_key, new_key, old_key_minor=False, new_key_minor=False):
    f_tempo = change_tempo(filename, old_bpm, new_bpm)
    f_tempo_key = change_key(f_tempo, old_key, new_key, old_key_minor, new_key_minor)
    dump_wav(f_tempo_key)


def get_wav_duration(filename):
    with contextlib.closing(wave.open(f"{filename}.wav", 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        length = frames / float(rate)
        return length
