"""
MIT License

Copyright (c) 2018 Michael Schmidt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import speech_recognition as sp_rec

from environment import CREDS as creds
from logger import LOGGER as log

# Sphinx Recognizer, Free to use but only decent at recognizing
def sphinx(rec, audio):
    """
    Use sphinx to recognize the natural language.
    :rec:       speech_recognition.Recognizer()     The speech recognition engine.
    :audio:     speech_recognition.AudioData()      The audio from the end user.
    :returns:   dict()                              meta-information: text transcipt
    """

    meta = dict({})

    try:
        phrase = rec.recognize_sphinx(audio)
        meta['text'] = phrase.split()
    except sp_rec.UnknownValueError:
        meta['error'] = 'Sphinx could not understand audio'
        log.error('Sphinx couldn\'t understand audio')
    except sp_rec.RequestError as exp:
        meta['error'] = 'Sphinx error; {0}'.format(exp)
        log.error('Sphinx error; {0}'.format(exp))

    return meta


def google(rec, audio):
    """
    Use GOOGLE API to recognize the natural language.
    :rec:       speech_recognition.Recognizer()     The speech recognition engine.
    :audio:     speech_recognition.AudioData()      The audio from the end user.
    :returns:   dict()                              meta-information: text transcipt
    """

    meta = dict({})

    try:
        phrase = rec.recognize_google(audio) # TODO: this needs to be updated
        meta['text'] = phrase.split()
    except sp_rec.UnknownValueError:
        meta['error'] = 'Google Speech Recognizer could not understand audio'
        log.error('Google Speech Recognizer couldn\'t understand audio')
    except sp_rec.RequestError as exc:
        meta['error'] = 'Could not request results from Google Speech Recognition service; {0}'.format(exc)
        log.error('Could not request results from Google Speech Recognition service; {0}'.format(exc))

    return meta


def google_sound_cloud(rec, audio):
    """
    Use GOOGLE SOUND CLOUD API to recognize the natural language.
    :rec:       speech_recognition.Recognizer()     The speech recognition engine.
    :audio:     speech_recognition.AudioData()      The audio from the end user.
    :returns:   dict()                              meta-information: text transcipt
    """

    meta = dict({})

    try:
        phrase = rec.recognize_google_cloud(audio, credentials_json=creds['GOOGLE_CLOUD_SPEECH'])
        meta['text'] = phrase.split()
    except sp_rec.UnknownValueError:
        meta['error'] = 'Google Cloud Speech could not understand audio'
        log.error('Google Cloud Speech couldn\'t understand audio')
    except sp_rec.RequestError as exc:
        meta['error'] = 'Could not request results from Google Cloud Speech service; {0}'.format(exc)
        log.error('Could not request results from Google Cloud speech Recognition service; {0}'.format(exc))

    return meta


def wit(rec, audio):
    """
    Use WIT API to recognize the natural language.
    :rec:       speech_recognition.Recognizer()     The speech recognition engine.
    :audio:     speech_recognition.AudioData()      The audio from the end user.
    :returns:   dict()                              meta-information: text transcipt
    """

    meta = dict({})

    try:
        phrase = rec.recognize_wit(audio, key=creds['WIT_AI_KEY'])
        meta['text'] = phrase.split()
    except sp_rec.UnknownValueError:
        meta['error'] = 'Wit.ai could not understand audio'
        log.error('Wit.ai couldn\'t understand audio')
    except sp_rec.RequestError as exc:
        meta['error'] = 'Could not request results from Wit.ai service; {0}'.format(exc)
        log.error('Could not request results from Wit.ai service; {0}'.format(exc))

    return meta


def bing(rec, audio):
    """
    Use Bing API to recognize the natural language.
    :rec:       speech_recognition.Recognizer()     The speech recognition engine.
    :audio:     speech_recognition.AudioData()      The audio from the end user.
    :returns:   dict()                              meta-information: text transcipt
    """

    meta = dict({})

    try:
        phrase = rec.recognize_bing(audio, key=creds['BING_KEY'])
        meta['text'] = phrase.split()
    except sp_rec.UnknownValueError:
        meta['error'] = 'Microsoft Bing Voice Recognition could not understand audio'
        log.error('Microsoft Bing Voice Recognition couldn\'t understand audio')
    except sp_rec.RequestError as exc:
        meta['error'] = 'Could not request results from Microsoft Bing Voice Recognition service; {0}'.format(exc)
        log.error('Could not request results from Microsoft Bing Voice Recognition service; {0}'.format(exc))

    return meta


def houndify(rec, audio):
    """
    Use Houndify API to recognize the natural language.
    :rec:       speech_recognition.Recognizer()     The speech recognition engine.
    :audio:     speech_recognition.AudioData()      The audio from the end user.
    :returns:   dict()                              meta-information: text transcipt
    """

    meta = dict({})

    try:
        phrase = rec.recognize_houndify(audio,
                                        client_id=creds['HOUNDIFY_CLIENT_ID'],
                                        client_key=creds['HOUNDIFY_CLIENT_KEY'])
        meta['text'] = phrase.split()
    except sp_rec.UnknownValueError:
        meta['error'] = 'Houndify could not understand audio'
        log.error('Houndify couldn\'t understand audio')
    except sp_rec.RequestError as exc:
        meta['error'] = 'Could not request results from Houndify service; {0}'.format(exc)
        log.error('Could not request results from Houndify service; {0}'.format(exc))

    return meta

def ibm(rec, audio):
    """
    Use IBM API to recognize the natural language.
    :rec:       speech_recognition.Recognizer()     The speech recognition engine.
    :audio:     speech_recognition.AudioData()      The audio from the end user.
    :returns:   dict()                              meta-information: text transcipt
    """

    meta = dict({})

    try:
        phrase = rec.recognize_ibm(audio,
                                   username=creds['IBM_USERNAME'],
                                   password=creds['IBM_PASSWORD'])
        meta['text'] = phrase.split()
    except sp_rec.UnknownValueError:
        meta['error'] = 'IBM Speech to Text could not understand audio'
        log.error('IBM Speech to Text couldn\'t understand audio')
    except sp_rec.RequestError as exc:
        meta['error'] = 'Could not request results from IBM Speech to Text service; {0}'.format(exc)
        log.error('Could not request results from IBM Speech to Text service; {0}'.format(exc))

    return meta
