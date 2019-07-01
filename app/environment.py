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
    'GOOGLE_CLOUD_SPEECH': r"""{
      "type": "service_account",
      "project_id": "sound-count",
      "private_key_id": "345aba9f88f021912b0b94134f0ed0c519db6742",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDU48TioKoDPx9S\ntz+6tGeUvCXmsJkrTyOQYK8G6I1luu7PHeaLn2eAHvDgKYd0m+4MuD5FYkFofH6q\n4Eg7w00CVvcQczt5UWSZ5rNp4hyiek8ZiqvoG1eoGJ9aQ+z385KY2vHXPLfdr9vA\nxq2epftuuvYZmeLzQbK94PzVHzgdX3UbqJLotpO49ZN0jjFLeyMkCPZqVtQ5wECB\nGB+hyEfeE1x8oYl+CtJcKx57t5CD7uz+D4snCKv7X6ErVGDapkRElo98HfmESC5o\nGP2wGMIDB6xSlxbTm1lUEmoIeLwPFV3dHihRyiOHAwOPWIYYc2vdxix8smVLtP7A\nj3QRPgxNAgMBAAECggEARzqkK+10pNxwVwUgChCFXaLsDXkF7pMug4aN2UJi2OhI\nMb0/33RotVnk3yOWAkKPzeqxTxa2asbIvNSI5pIMSJ2fUX40pn1Aqyug2OsCCKzi\nnVmj9ed8Fy6R1qpGdZml8YXEB+91V3OZE7GF8sB3VU+xutQdtqVDMDvAbHBjHpQv\nAscjy/HA5It756SrTvLckZvTeanJzlYcHv5aw/8ah3nhTHgbGskABSEoa8D9VdIG\n6Z6MhiNdtUdA37tn9R20yC7kMn8LkVsNwd4l7LRJi5x3fD2IBaqQEgn/TPPAD1Ez\n8AKwMEnzxWbtK6RURyHppcXgHK5h4Kn8A62ahKbvIwKBgQDuLdX10s9PfVUwyaPw\nofGEpdva6RzIxZ5QTfsHztrIS0olItEWun8DY7zB/Z1cwrMhkgLtaufQD0zg/G3d\n7gTQ1OSkxaWZRTCQjxF1v+FPZLtCvNDtl7iriuNCAY2W24zPDkvSrObVzWqlgVVf\nR+Um5RQ8GuEspT2G2dLUeknXGwKBgQDk0Yhm0ecX424tqZJS+Q2LaSOt1Ny4575e\ns2cjP998/ImpOR63Lf7+pKOCqhyYLxnq19rtJpkriXrNCZEelC+fWL7+esYhL5wo\n4mNNsb3311L3fATpBp42/8HntIFZCWtSMgtqlUtlUNEqJcnCUXAZLs1FaMaJwror\no65WQcxYtwKBgA4TVV6mq6u162/rqq2Q1HYTWy/PsOzIiPeT9C7c8Z7+nA4fxZ2D\nPfhUT5ZjR4Zw1yc3usaPF8366X8uS8vewhgZTL3UFFo/dYRFgDGmOkl32X0zLWGt\nIrO4jH+dGeH9bY/a924m26ls702CnCn6VLd8uDppGD+MMFukycnWxEBbAoGBAOAp\nMTJhUb5CTK6pH7LvT8iScKScEruGNCY8JL8QlNWx5P6F+cREaDl4esLH+glQo1hA\nrLWFCarwHQB+7c8CJwE5BKrzBeR+6sHWvqffh5YkOKBAu+K5XAfPWFuwpsLeCmhU\npIB+z4Tqvm5G5Lfb5jCVe/0SXuWYgZ+8006nWRRTAoGABRWNUUi+W9sei50eWZEd\nuZdTcsun9H6cPE3m/AxNGPTMn3WGrdCju/BwPf1zK2xwdoI9rx2AeKdadQnoekwC\nNRnUbPudoT3wSu5l0S/R6hbjzETBkCmw8Uo6aX8Y3dOsmL7VlVhZz5Ab+3usXMTz\nGCjn8FPplIc0GfKkVH0qKaY=\n-----END PRIVATE KEY-----\n",
      "client_email": "sound-count@sound-count.iam.gserviceaccount.com",
      "client_id": "105742980417282357346",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/sound-count%40sound-count.iam.gserviceaccount.com"
    }
""",

    'HOUNDIFY_CLIENT_ID': '',
    'HOUNDIFY_CLIENT_KEY': '',

    'WIT_AI_KEY': '',

    'IBM_USERNAME': '',
    'IBM_PASSWORD': ''}

# grab the pickled for the recognizer
CLFFG = joblib.load(os.path.join('models', 'cfl_gender.pkl'))
CLFFA = joblib.load(os.path.join('models', 'cfl_age.pkl'))
CLFFD = joblib.load(os.path.join('models', 'cfl_dialect.pkl'))
