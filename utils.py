import os
import sys
import wave
import logging
import contextlib

import nltk
import speech_recognition as sr

import environment as env
from recognizers import sphinx

def duration(filename):
    """
    Opens a wave file and finds the number of frames per rate

    :filename:  a filename which is a .wav file
    :returns: returns the framerate
    """
    with contextlib.closing(wave.open(filename, 'r')) as f:
        frames = f.getnframes()         # get frames
        rate = f.getframerate()         # get rate
        return frames / float(rate)     # return framerate


def speech_rec(filename):

    audio_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
    # instantiate a speech recognizer object
    r = sr.Recognizer()

    # try to open the audio file
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)

    # return the speech to text
    words = sphinx(r, audio)
    return words


def pos_tagger(words):
    tag_words = []

    for word in words:
        tag_words.append(nltk.pos_tag(word))

    return tag_words[0]



class Log():

    # initialization
    def __init__(self):
        # gets the logger from the sound count log
        self.logger = logging.getLogger('sound-count')
        # set the level of the degub message
        self.logger.setLevel(logging.DEBUG)

        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')


        # stdout logging
        self.stdout_handler = logging.StreamHandler()
        self.stdout_handler.setFormatter(self.formatter)

        # file handling
        self.file_handler = logging.FileHandler(env.app_vars['LOG_PATH'])
        self.file_handler.setFormatter(self.formatter)

        # add for handling for files and stdout
        self.logger.addHandler(self.stdout_handler)
        self.logger.addHandler(self.file_handler)

    # custom debugger message
    def debug(self, message):
        self.check_size()
        self.logger.debug("DEBUG: {0}".format(message))

    # custom info message
    def info(self, message):
        self.check_size()
        self.logger.info("INFO: {0}".format(message))

    # custom warning message
    def warning(self, message):
        self.check_size()
        self.logger.info("WARNING: {0}".format(message))

    # custom error message
    def error(self, message):
        self.check_size()
        self.logger.info("ERROR: {0}".format(message))

    # custom criticals message
    def critical(self, message):
        self.check_size()
        self.logger.info("CRITICAL: {0}".format(message))

    # checks the see if the size is too big, removes the log file if 512 Mb
    def check_size(self):
        if os.path.getsize(env.app_vars['LOG_PATH']) > env.app_vars['LOG_MAXSIZE']:
            os.remove(env.app_vars['LOG_PATH'])

# instantiate a logger
logger = Log()

# TESTING THE LOGGER
# logger.debug("This message")
# logger.info("That message")
# logger.warning("Bad message")
# logger.error("uh oh message")
# logger.critical("FFUUUUUU!")
