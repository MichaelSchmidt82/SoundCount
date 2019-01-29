def post(self):
    """
    Handles HTTP POST request given a form with a 'file.'  'file' represents
    the user's audio submission.
    :file:      (WAV) waveform audio        Via HTTP POST form-data.
    :returns:   dict()                      Meta-information of the audio.
    """

    . . .

    parse = reqparse.RequestParser()
    parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
    args = parse.parse_args()

    try:
        audio_file = args['file']
        audio_file.save(tempfile)
    except AttributeError:
        . . .

    try:
        payload['meta'].update(speech_rec(tempfile))
        payload['meta'].update(voice_analyzer(tempfile))
    except:
        . . .

    payload['count'] = len(payload['meta']['text'])
    payload['meta']['text'] = pos_tagger([payload['meta']['text']])
    payload['meta']['duration'] = duration(tempfile)

    . . .

    return payload

    Lines 8 - 19 receive and parse the request, and save the audio data as a file named "tempfile."
    Lines 22 and 23 perform speech recognition, and run the audio through the voice analyzer.  Both these functions return dict() types so the payload's meta information is updated.
    Line 27 uses Python's built-in len() function, and line 28 uses NTLK Averaged Perceptron Tagger to tag the list of words.
    The duration of the file is calculated using the audio's frame count divided by the frame-rate.  It's performed on line 29
    Finally the temp file is removed and "payload" is returned.  Flask coverts Python's dict() type into a serialized JSON string.
