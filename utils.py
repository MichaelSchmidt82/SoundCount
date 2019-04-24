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

import os
import wave
import contextlib

import nltk
import speech_recognition as sr

import recognizers

def duration(filename):
    """
    Opens a wave file and finds the number of frames per rate

    :filename:      str()           A filename (relative to __main__)
    :returns:       float()         Duration in seconds
    """

    with contextlib.closing(wave.open(filename, 'r')) as data:
        frames = data.getnframes()
        rate = data.getframerate()
        return frames / float(rate)


def speech_rec(filename):
    """
    Create the recognition engine and perform speech-to-text
    :filename:      str()       A filename (relative to __main__)
    :returns:       list()      A list of words
    """

    # TODO: pass in engine as paramater (a.k.a sphinx)
    # TODO: use io.BytesIO() as a buffer instead of a filename

    # buff = BytesIO()
    audio_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)

    s_rec = sr.Recognizer()

    # with sr.AudioFile(buff) as source:
    with sr.AudioFile(audio_file) as source:
        audio = s_rec.record(source)

    words = recognizers.sphinx(s_rec, audio)
    return words


def pos_tagger(words):
    """
    Tag each word with associated POS.
    :words:     list()          list of str(), element: word
    :retruns    list[list()]    list() of list(), element [word, pos]
    """

    tag_words = []
    for word in words:
        tag_words.append(nltk.pos_tag(word))

    return tag_words[0]
