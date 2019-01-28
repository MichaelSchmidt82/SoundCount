# imports
import os
import uuid
import utils

import werkzeug
from utils import logger
from flask import Flask, request
from analyzer import voice_analyzer
from flask_restful import Resource, Api, reqparse


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

        logger.info("POST Request received.")
        payload = {'status': 'failure',
                   'count': 0,
                   'meta': {}}

        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()

        tempfile = str(uuid.uuid4())
        try:
            audio_file = args['file']
            audio_file.save(tempfile)
        except AttributeError:
            if audio_file is None:
                logger.error('Audio data not received')
                payload['meta']['error'] = 'audio data not received'
                payload['meta']['parameter'] = 'file'
                return payload

        logger.info('Analyzing temp file: {}'.format(tempfile))

        try:
            words = utils.speech_rec(tempfile)
            analysis = voice_analyzer(tempfile)
        except:
            logger.error('File does not appear to be a valid wav file')

            os.remove(tempfile)
            logger.debug('Temp file removed. Was {}'.format(tempfile))
            return payload

        payload['meta']['text'] = utils.pos_tagger([words['meta']['text']])

        payload['meta']['gender'] = analysis['gender']
        payload['meta']['age'] = analysis['age']
        payload['meta']['dialect'] = analysis['dialect']

        payload['count'] = len(payload['meta']['text'])

        duration = utils.duration(tempfile)
        logger.info("Analysis completed")

        if 'error' not in payload:
            payload['status'] = 'success'
            payload['meta']['duration'] = duration

        os.remove(tempfile)
        logger.debug("Temp file removed.  Was {}".format(tempfile))

        return payload

# Create the app and resource (root)
app = Flask(__name__)
api = Api(app)

api.add_resource(SoundCount, '/')
if __name__ == '__main__':
    logger.debug('Starting flask app.')
    app.run(host='0.0.0.0', debug=False)
