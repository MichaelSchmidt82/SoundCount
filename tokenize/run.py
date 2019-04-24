#!/usr/bin/env python
# encoding: utf-8
import os
import io
import time
import threading

import utils
import config
from audio import ADSFactory, AudioEnergyValidator
from workers import TokenizerWorker, TokenSaverWorker, TranscribeWorker
from tokenizer import StreamTokenizer

def create_transcript(sid, adult_audio, child_audio):
    """
    i am a docstring, hear me roar!!1!
    """

    adult_audio = utils.convert_to_wav(adult_audio)
    child_audio = utils.convert_to_wav(child_audio)

    adult_fname = '{{N}}_{{start}}_{{end}}_adult.{sid}'.format(sid=sid)
    child_fname = '{{N}}_{{start}}_{{end}}_child.{sid}'.format(sid=sid)

    adult_audio = ADSFactory.ads(data_buffer=adult_audio.read(),
                                 sampling_rate=config.DEFAULT_SAMPLE_RATE,
                                 sample_width=config.DEFAULT_SAMPLE_WIDTH,
                                 channels=config.DEFAULT_NB_CHANNELS,
                                 record=False)

    child_audio = ADSFactory.ads(data_buffer=child_audio.read(),
                                 sampling_rate=config.DEFAULT_SAMPLE_RATE,
                                 sample_width=config.DEFAULT_SAMPLE_WIDTH,
                                 channels=config.DEFAULT_NB_CHANNELS,
                                 record=False)

    adult_validator = AudioEnergyValidator(sample_width=adult_audio.get_sample_width(),
                                           energy_threshold=config.DEFUALT_NRG_THRESHOLD)

    child_validator = AudioEnergyValidator(sample_width=child_audio.get_sample_width(),
                                           energy_threshold=config.DEFUALT_NRG_THRESHOLD)

    adult_tokenizer = StreamTokenizer(validator=adult_validator,
                                      min_length=40,
                                      max_length=60000,
                                      max_continuous_silence=25,
                                      mode=False)

    child_tokenizer = StreamTokenizer(validator=child_validator,
                                      min_length=40,
                                      max_length=60000,
                                      max_continuous_silence=25,
                                      mode=False)

    adult_token_saver = TokenSaverWorker(name_format=adult_fname,
                                         filetype='wav',
                                         debug=0,
                                         sr=adult_audio.get_sampling_rate(),
                                         sw=adult_audio.get_sample_width(),
                                         ch=adult_audio.get_channels())

    child_token_saver = TokenSaverWorker(name_format=child_fname,
                                         filetype='wav',
                                         debug=0,
                                         sr=child_audio.get_sampling_rate(),
                                         sw=child_audio.get_sample_width(),
                                         ch=child_audio.get_channels())

    adult_xscribe_worker = TranscribeWorker(name_format=adult_fname)
    child_xscribe_worker = TranscribeWorker(name_format=child_fname)

    adult_observers = [adult_xscribe_worker, adult_token_saver]
    child_observers = [child_xscribe_worker, child_token_saver]

    adult_tokenizer_worker = TokenizerWorker(adult_audio, adult_tokenizer, 0.01, adult_observers)
    child_tokenizer_worker = TokenizerWorker(child_audio, child_tokenizer, 0.01, child_observers)

    for adult_ob, child_ob in zip(adult_observers, child_observers):
        adult_ob.start()
        child_ob.start()

    adult_tokenizer_worker.start()
    child_tokenizer_worker.start()

    while True:
        workers = threading.enumerate()
        if not set(adult_observers + child_observers).intersection(set(workers)):
            break
        time.sleep(1 / 3)

    adult_tokenizer_worker = None
    child_tokenizer_worker = None

    adult_data = sorted(adult_xscribe_worker.get(), key=lambda k: k['TIME'])
    child_data = sorted(child_xscribe_worker.get(), key=lambda k: k['TIME'])

    with open('job_transcript.txt', 'w') as out:
        while adult_data and child_data:
            if adult_data[0]['TIME'] < child_data[0]['TIME']:
                out.write('{time} ({user}): {text}\n'.format(time=adult_data[0]['TIME'],
                                                             user='adult',
                                                             text=adult_data[0]['CONTENT']))
                adult_data.pop(0)
            else:
                out.write('{time} ({user}): {text}\n'.format(time=child_data[0]['TIME'],
                                                             user='child',
                                                             text=child_data[0]['CONTENT']))
                child_data.pop(0)

        for _ in adult_data:
            out.write('{time} ({user}): {text}\n'.format(time=adult_data[0]['TIME'],
                                                         user='adult',
                                                         text=adult_data[0]['CONTENT']))
            adult_data.pop(0)

        for _ in child_data:
            out.write('{time} ({user}): {text}\n'.format(time=child_data[0]['TIME'],
                                                         user='child',
                                                         text=child_data[0]['CONTENT']))
            child_data.pop(0)


if __name__ == '__main__':

    with open(os.path.join('..', 'media', 'segment1.mp4'), 'rb') as dummy_audio:
        adult = io.BytesIO(dummy_audio.read())

    with open(os.path.join('..', 'media', 'segment1.mp4'), 'rb') as dummy_audio:
        child = io.BytesIO(dummy_audio.read())

    create_transcript('sid', adult, child)
