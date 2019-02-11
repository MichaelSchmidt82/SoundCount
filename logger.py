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

import os
import logging

from environment import APP_VARS as config


class Log():
    """
    A class to manage logging activity
    """


    def __init__(self):
        """
        Create a handler for std_out and file stream for logging.Logger() emitters
        """

        self.logger = logging.getLogger('sound-count')

        self.logger.setLevel(logging.DEBUG)

        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')

        self.stdout_handler = logging.StreamHandler()
        self.stdout_handler.setFormatter(self.formatter)

        self.file_handler = logging.FileHandler(config['LOG_PATH'])
        self.file_handler.setFormatter(self.formatter)

        self.logger.addHandler(self.stdout_handler)
        self.logger.addHandler(self.file_handler)


    def debug(self, message):
        """
        Custom DEBUG message
        :message:   str()       message to log
        :returns:   None
        """

        self.check_size()
        self.logger.debug('DEBUG: %s', message)


    def info(self, message):
        """
        Custom INFO message
        :message:   str()       message to log
        :returns:   None
        """

        self.check_size()
        self.logger.info('INFO: %s', message)

    # custom warning message
    def warning(self, message):
        """
        Custom WARNING message
        :message:   str()       message to log
        :returns:   None
        """

        self.check_size()
        self.logger.info('WARNING: %s', message)

    # custom error message
    def error(self, message):
        """
        Custom ERROR message
        :message:   str()       message to log
        :returns:   None
        """

        self.check_size()
        self.logger.info('ERROR: %s', message)

    # custom criticals message
    def critical(self, message):
        """
        Custom CRITICAL message
        :message:   str()       message to log
        :returns:   None
        """

        self.check_size()
        self.logger.info('CRITICAL: %s', message)

    # checks the see if the size is too big, removes the log file if 512 Mb
    def check_size(self):
        """
        Remove log based on size (in bytes)
        """

        if os.path.getsize(config['LOG_PATH']) > config['LOG_MAXSIZE']:
            os.remove(config['LOG_PATH'])

LOGGER = Log()
