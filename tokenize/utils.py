import io
import wave
import subprocess

from exceptions import AudioFileFormatError, TimeFormatError

import config


def seconds_to_str_fromatter(_format):
    """
    Accepted format directives: %i %s %m %h
    """
    # check directives are correct

    if _format == '%S':
        def _fromatter(seconds):
            return '{:.2f}'.format(seconds)

    elif _format == '%I':
        def _fromatter(seconds):
            return '{0}'.format(int(seconds * 1000))

    else:
        _format = _format.replace('%h', '{hrs:02d}')
        _format = _format.replace('%m', '{mins:02d}')
        _format = _format.replace('%s', '{secs:02d}')
        _format = _format.replace('%i', '{millis:03d}')

        try:
            i = _format.index('%')
            raise TimeFormatError("Unknow time format directive '{0}'".format(_format[i:i+2]))
        except ValueError:
            pass

        def _fromatter(seconds):
            millis = int(seconds * 1000)
            hrs, millis = divmod(millis, 3600000)
            mins, millis = divmod(millis, 60000)
            secs, millis = divmod(millis, 1000)
            return _format.format(hrs=hrs, mins=mins, secs=secs, millis=millis)

    return _fromatter


def save_audio_data(data, filename, filetype=None, **kwargs):

    lower_fname = filename.lower()
    if filetype is not None:
        filetype = filetype.lower()

    # save raw data
    if filetype == 'raw' or (filetype is None and lower_fname.endswith('.raw')):
        fp = open(filename, 'w')
        fp.write(data)
        fp.close()
        return

    # save other types of data
    # requires all audio parameters
    srate = kwargs.pop('sampling_rate', None)
    if srate is None:
        srate = kwargs.pop('sr', None)

    swidth = kwargs.pop('sample_width', None)
    if swidth is None:
        swidth = kwargs.pop('sw', None)

    ch = kwargs.pop('channels', None)
    if ch is None:
        ch = kwargs.pop('ch', None)

    if None in (swidth, srate, ch):
        raise Exception('All audio parameters are required to save no raw data')

    if filetype in ('wav', 'wave') or (filetype is None and lower_fname.endswith('.wav')):
        # use standard python's wave module
        fp = wave.open(filename, 'w')
        fp.setnchannels(ch)
        fp.setsampwidth(swidth)
        fp.setframerate(srate)
        fp.writeframes(data)
        fp.close()
    else:
        raise AudioFileFormatError('cannot write file format {0} (file name: {1})'.format(filetype, filename))


def convert_to_wav(data):
    """
    Convert audio into waveform audio
    data        io.BytesIO()        Audio data (MP4/AAC)
    """
    if isinstance(data, bytes):
        data = io.BytesIO(data)

    # ffmpeg -i valid.mp4 -sample_rate 48000 -f wav valid.wav
    command = ['ffmpeg', '-i', '-', '-sample_rate', str(config.DEFAULT_SAMPLE_RATE), '-f', 'wav', 'pipe:1']
    ffmpeg = subprocess.Popen(command,
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

    wav, errs = ffmpeg.communicate(data.read(), timeout=config.TIMEOUT)

    data = io.BytesIO(wav)
    data.seek(0)
    ffmpeg.wait()

    return data
