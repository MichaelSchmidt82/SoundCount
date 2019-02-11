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

import numpy as np
import librosa
from utils import LOGGER as logger
from environment import CLFFG as gender_model
from environment import CLFFA as age_model
from environment import CLFFD as dialect_model


def voice_analyzer(filename):
    """
    Perform analysis on voice using pickled model.
    See: https://github.com/lreynolds18/Voice-Analyzer
    """

    y, sr = librosa.load(filename, sr=22050)

    stft = np.abs(librosa.stft(y))
    mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
    mel = np.mean(librosa.feature.melspectrogram(y, sr=sr).T, axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sr).T, axis=0)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr).T, axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sr).T, axis=0)

    features = np.hstack([mfccs, chroma, mel, contrast, tonnetz])

    features = features.reshape(1, -1)

    meta = dict({})
    meta['gender'] = gender_model.predict(features)[0]
    meta['age'] = age_model.predict(features)[0]
    meta['dialect'] = dialect_model.predict(features)[0]

    logger.info('Voice analyzer completed task: {g} {a} {d}'.format(
        g=meta['gender'],
        a=meta['age'],
        d=meta['dialect']))

    return meta
