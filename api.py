# imports
import os
import uuid
import werkzeug
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

from utils import logger, duration, speech_rec, pos_tagger

from analyzer import voice_analyzer



# Instance of application
class SoundCount(Resource):

    """
    An instance of the SoundCount app
    POST: receive a WAV file to process.
    file: the file field.
    """

    def post(self):
        """
        Handles HTTP POST request given a form with a 'file.'  'file' represents
        the user's audio submission.

        :file:      (WAV) waveform audio        Via HTTP POST form-data.
        :returns:   dict()                      Meta-information of the audio.
        """

        tempfile = str(uuid.uuid4())
        logger.info("POST Request received. using temp file {}".format(tempfile))
        payload = {'status': 'failure',
                   'count': 0,
                   'meta': {}}

        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()

        try:
            audio_file = args['file']
            audio_file.save(tempfile)
        except AttributeError:
            if audio_file is None:
                logger.error('Audio data not received')
                payload['meta']['error'] = 'audio data not received'
                payload['meta']['parameter'] = '\'file\' not present'
                return payload

        logger.info('Analyzing temp file: {}'.format(tempfile))

        try:
            payload['meta'].update(speech_rec(tempfile))
            payload['meta'].update(voice_analyzer(tempfile))
        except:
            logger.error('File {} does not appear to be a valid'.format(tempfile))

            os.remove(tempfile)
            logger.debug('Temp file removed. Was {}'.format(tempfile))
            payload['meta']['error'] = 'file does not appear to be a valid'

            return payload

        payload['count'] = len("the quick brown fox jumps over the lazy dog".split())
        payload['meta']['text'] = pos_tagger(["the quick brown fox jumps over the lazy dog".split()])
        payload['meta']['duration'] = duration(tempfile)

        if 'error' not in payload['meta']:
            payload['status'] = 'success'

        os.remove(tempfile)
        logger.info("Process completed, removed tempfile {}".format(tempfile))

        return payload

# Create the app and resource (root)
app = Flask(__name__)
api = Api(app)

api.add_resource(SoundCount, '/')
if __name__ == '__main__':
    logger.debug('Starting flask app.')
    app.run(host='0.0.0.0', debug=True)
