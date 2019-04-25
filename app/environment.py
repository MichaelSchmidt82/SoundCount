"""
MIT License

Copyright (c) 2019 Michael Schmidt

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
from sklearn.externals import joblib

# in KB
LOG_SIZE = 512

APP_VARS = {
    'APP_DEBUG': True,

    'LOG_PATH': 'logs/log.log',
    'LOG_MAXSIZE': LOG_SIZE * 1024,
    'HOST': '0.0.0.0',
    'PORT': 5000
}

CREDS = {
    'BING_KEY': '',
    'GOOGLE_CLOUD_SPEECH': '',

    'HOUNDIFY_CLIENT_ID': '',
    'HOUNDIFY_CLIENT_KEY': '',

    'WIT_AI_KEY': '',

    'IBM_USERNAME': '',
    'IBM_PASSWORD': ''}

# grab the pickled for the recognizer
CLFFG = joblib.load(os.path.join('models', 'cfl_gender.pkl'))
CLFFA = joblib.load(os.path.join('models', 'cfl_age.pkl'))
CLFFD = joblib.load(os.path.join('models', 'cfl_dialect.pkl'))
