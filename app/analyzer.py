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

import nltk
import librosa
import contextlib

import numpy as np

import speech_recognition as sr
import recognizers

from logger import LOGGER as log

from environment import CLFFG as gender_model
from environment import CLFFA as age_model
from environment import CLFFD as dialect_model


class VoiceAnalyzer:
    """
    Perform analysis on voice using pickled model.
    See: https://github.com/lreynolds18/Voice-Analyzer
    """

    def __init__(self, log=None):
        self.log = log

    def transcribe(self, filename):
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

    def tag(self, words):
        """
        Tag each word with associated POS.
        :words:     list()          list of str(), element: word
        :retruns    list[list()]    list() of list(), element [word, pos]
        """

        tagged_words = []
        for word in words:
            tagged_words.append(nltk.pos_tag(word))

        return tagged_words[0]

    def analyze(self, filename):
        """

        """

        y, sr = librosa.load(filename, sr=22050)

        stft        = np.abs(librosa.stft(y))
        mfccs       = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
        mel         = np.mean(librosa.feature.melspectrogram(y, sr=sr).T, axis=0)
        contrast    = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sr).T, axis=0)
        tonnetz     = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr).T, axis=0)
        chroma      = np.mean(librosa.feature.chroma_stft(S=stft, sr=sr).T, axis=0)

        features = np.hstack([mfccs, chroma, mel, contrast, tonnetz])
        features = features.reshape(1, -1)

        meta = {
            'gender': gender_model.predict(features)[0],
            'age': age_model.predict(features)[0],
            'dialect': dialect_model.predict(features)[0]
        }

        if self.log:
            self.log.info('Voice analyzer completed task: {g} {a} {d}'.format(
                g=meta['gender'],
                a=meta['age'],
                d=meta['dialect']))

        return meta

    def duration(self, filename):
        """
        Opens a wave file and finds the number of frames per rate

        :filename:      str()           A filename (relative to __main__)
        :returns:       float()         Duration in seconds
        """

        with contextlib.closing(wave.open(filename, 'r')) as data:
            frames = data.getnframes()
            rate = data.getframerate()
            return frames / float(rate)
