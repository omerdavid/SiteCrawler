

import logging


class LogService:

    def __init__(self, _fileName='sitecrawler.log'):
        logging.basicConfig(filename=_fileName,
                            level=logging.DEBUG)

    def error(self, ex):
        logging.exception(ex)

    def info(self, msg):
        logging.info(msg)
