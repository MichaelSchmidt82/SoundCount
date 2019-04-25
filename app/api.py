"""
MIT License

Copyright (c) 2018-2019 Michael Schmidt

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
import uuid
import werkzeug
from flask import Flask
from flask_restful import Resource, Api, reqparse

from environment import APP_VARS as config
from logger import LOGGER

from analyzer import VoiceAnalyzer


class SoundCount(Resource):

    """
    An instance of the SoundCount app

    :HTTP POST:   receive a WAV file to process.
    """
    def __init__(self):

        self.log = None
        if config['APP_DEBUG']:
            self.log = LOGGER

        self.analyzer = VoiceAnalyzer()

    def post(self):
        """
        HTTP POST.   Form with a 'file' field.

        :file:      (WAV) waveform audio        Via HTTP POST form-data.
        :returns:   dict()                      Meta-information of the audio.
        """

        payload = {
            'status': 'failure',
            'count': 0,
            'meta': dict()
        }
        tempfile = str(uuid.uuid4())
        if self.log:
            self.log.info("POST Request received. using temp file {}".format(tempfile))

        parse = reqparse.RequestParser()
        parse.add_argument('audio', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()

        try:
            audio_file = args['audio']
            audio_file.save(tempfile)
        except AttributeError:
            if audio_file is None:
                if self.log:
                    self.log.error('Audio data not received')
                payload['meta']['error'] = 'audio data not received'
                payload['meta']['parameter'] = '\'file\' not present'
                return payload

        if self.log:
            self.log.info('Analyzing temp file: {}'.format(tempfile))

        try:
            payload['meta'].update(self.analyzer.analyze(tempfile))
            payload['meta'].update(self.analyzer.transcribe(tempfile))
            payload['count'] = len(payload['meta']['text'])
            payload['meta']['text'] = self.analyzer.tag([payload['meta']['text']])
            payload['meta']['duration'] = self.analyzer.duration(tempfile)


        except:
            if self.log:
                self.log.error('File {} does not appear to be a valid'.format(tempfile))

            os.remove(tempfile)
            if self.log:
                self.log.debug('Temp file removed. Was {}'.format(tempfile))

            payload['meta']['error'] = 'file does not appear to be a valid'

            return payload

        payload['count'] = len(payload['meta']['text'])

        if 'error' not in payload['meta']:
            payload['status'] = 'success'

        os.remove(tempfile)
        if self.log:
            self.log.info("Process completed, removed tempfile {}".format(tempfile))

        return payload

APP = Flask(__name__)
API = Api(APP)

API.add_resource(SoundCount, '/')
if __name__ == '__main__':
    LOGGER.debug('Starting flask app.')
    APP.run(host=config['HOST'], port=config['PORT'], debug=config['APP_DEBUG'])
