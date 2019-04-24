import os
import sys
import time
import logging

from threading import Thread
from queue import Queue, Empty

import speech_recognition as sp_rec

from utils import save_audio_data, seconds_to_str_fromatter

JOBS = Queue()


class Worker(Thread):

    def __init__(self, timeout=0.2, debug=False, logger=None):
        self.timeout = timeout
        self.debug = debug
        self.logger = logger

        if self.debug and self.logger is None:
            self.logger = logging.getLogger('__main__')
            self.logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler(sys.stdout)
            self.logger.addHandler(handler)

        self._inbox = Queue()
        self._stop_request = Queue()
        Thread.__init__(self)

    def debug_message(self, message):
        self.logger.debug(message)

    def _stop_requested(self):

        try:
            message = self._stop_request.get_nowait()
            if message == 'stop':
                return True
        except Empty:
            return False

    def stop(self):
        self._stop_request.put('stop')
        self.join()

    def send(self, message):
        self._inbox.put(message)

    def _get_message(self):
        try:
            message = self._inbox.get(timeout=self.timeout)
            return message
        except Empty:
            return None


class TokenSaverWorker(Worker):

    def __init__(self, name_format, filetype, timeout=0.2, debug=False, logger=None, **kwargs):
        """
        :name_format:
        :filetype:
        :timeout:
        :debug:
        :logger:
        """

        self.name_format = name_format
        self.filetype = filetype
        self.kwargs = kwargs
        Worker.__init__(self, timeout=timeout, debug=debug, logger=logger)

    def run(self):

        global JOBS # pylint: disable=W0603

        while True:
            if self._stop_requested():
                break

            message = self._get_message()
            if message is not None:
                if message == TokenizerWorker.END_OF_PROCESSING:
                    break

                _id = message.pop('id', None)
                audio_data = message.pop('audio_data', None)
                start = message.pop('start', None)
                end = message.pop('end', None)

                if audio_data is not None and len(audio_data) > 0:
                    fname = self.name_format.format(N=_id, start=start, end=end)
                    try:
                        if self.debug:
                            self.debug_message('[SAVE]: Detection {id} saved as {fname}'.format(id=_id, fname=fname))
                        save_audio_data(audio_data, fname, filetype=self.filetype, **self.kwargs)
                    except Exception as e:
                        sys.stderr.write(str(e) + '\n')

                JOBS.put(fname)

    def notify(self, message):
        self.send(message)


class TokenizerWorker(Worker):

    END_OF_PROCESSING = 'END_OF_PROCESSING'

    def __init__(self, ads, tokenizer, analysis_window, observers):
        self.ads = ads
        self.tokenizer = tokenizer
        self.analysis_window = analysis_window
        self.observers = observers
        self._inbox = Queue()
        self.count = 0
        Worker.__init__(self)


    def run(self):
        """

        """

        def notify_observers(data, start, end):
            audio_data = b''.join(data)
            self.count += 1

            start_time = start * self.analysis_window
            end_time = (end+1) * self.analysis_window
            duration = (end - start + 1) * self.analysis_window

            # notify observers
            for observer in self.observers:
                observer.notify({'id' : self.count,
                                 'audio_data' : audio_data,
                                 'start' : start,
                                 'end' : end,
                                 'start_time' : start_time,
                                 'end_time' : end_time,
                                 'duration' : duration}
                                )

        self.ads.open()
        self.tokenizer.tokenize(data_source=self, callback=notify_observers)
        for observer in self.observers:
            observer.notify(TokenizerWorker.END_OF_PROCESSING)

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def read(self):
        if self._stop_requested():
            return None
        else:
            return self.ads.read()


class LogWorker(Worker):

    def __init__(self, print_detections=False, output_format='{start} {end}',
                 time_formatter=seconds_to_str_fromatter('%S'), timeout=0.2, debug=False, activity=None):

        self.print_detections = print_detections
        self.output_format = output_format
        self.time_formatter = time_formatter
        self.detections = []

        Worker.__init__(self, timeout=timeout, debug=debug)

    def run(self):
        """

        """
        while True:
            if self._stop_requested():
                break

            message = self._get_message()

            if message is not None:

                if message == TokenizerWorker.END_OF_PROCESSING:
                    break

                audio_data = message.pop('audio_data', None)
                _id = message.pop('id', None)
                start = message.pop('start', None)
                end = message.pop('end', None)
                start_time = message.pop('start_time', None)
                end_time = message.pop('end_time', None)
                duration = message.pop('duration', None)
                if audio_data:  #if audio_data is not None and len(audio_data) > 0:

                    if self.debug:
                        self.debug_message('[DET]: Detection {id} (start:{start}, end:{end})'.format(
                            id=_id,
                            start='{:5.2f}'.format(start_time),
                            end='{:5.2f}'.format(end_time)))

                    if self.print_detections:
                        print(self.output_format.format(id= id,
                                                        start=self.time_formatter(start_time),
                                                        end=self.time_formatter(end_time),
                                                        duration=self.time_formatter(duration)))

                    self.detections.append((_id, start, end, start_time, end_time))

    def notify(self, message):
        self.send(message)

class TranscribeWorker(Worker):
    """

    """
    def __init__(self, name_format, timeout=0.2, debug=False, logger=None, **kwargs):
        """

        """
        self.initial_segment = True
        self.name_format = name_format
        self.results = []
        Worker.__init__(self, timeout=timeout, debug=debug, logger=logger)

    def _segment_to_text(self, fname):

        rec = sp_rec.Recognizer()
        with sp_rec.AudioFile(fname) as source:
            segment = rec.record(source)
            phrase = rec.recognize_sphinx(segment)

        return phrase

    def run(self):
        """

        """

        global JOBS # pylint: disable=W0603

        segment = {}
        last_timestamp = None

        while True:
            if self._stop_requested():
                break

            message = self._get_message()
            if message is not None:
                if message == TokenizerWorker.END_OF_PROCESSING:
                    break

                # audio_data = message.pop('audio_data', None)
                # _id = message.pop('id', None)
                # start = message.pop('start', None)
                # end = message.pop('end', None)
                start_time = message.pop('start_time', None)
                end_time = message.pop('end_time', None)
                # duration = message.pop('duration', None)

                while JOBS.empty():
                    time.sleep(1 / 3)

                fname = JOBS.get()
                if self.initial_segment:
                    segment['TIME'] = start_time
                    segment['CONTENT'] = self._segment_to_text(fname)
                    self.initial_segment = False
                elif abs(end_time - last_timestamp) < 3:
                    segment['CONTENT'] = '{} {}'.format(segment['CONTENT'], self._segment_to_text(fname))
                else:
                    self.results.append(segment)
                    segment = {}
                    segment['TIME'] = start_time
                    segment['CONTENT'] = self._segment_to_text(fname)

                last_timestamp = end_time
                os.remove(fname)
        self.results.append(segment)

    def notify(self, message):
        self.send(message)

    def get(self):
        if self.results:
            return self.results
        return None
