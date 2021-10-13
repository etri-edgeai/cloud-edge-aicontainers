from ai_interface.baseclass import BaseClass
from ai_interface.appconfig import AppConfig
from ai_interface.flask import init_handler
import ai_interface.utils.model_utils as model_utils

from flask import Response

import logging, sys
import logging.handlers

import os
import json

import time

from MyModel import MyModel

def log_setup():
    """
    log_handler = logging.handlers.TimedRotatingFileHandler('/log/fe.log', when='midnight')

    log_handler.setFormatter(formatter)
    """
    formatter = logging.Formatter(
        '%(asctime)s program_name [%(process)d]: %(message)s',
        '%b %d %H:%M:%S')

    termlog_handler = logging.StreamHandler()
    termlog_handler.setFormatter(formatter)

    logger = logging.getLogger()
    #logger.addHandler(log_handler)
    logger.addHandler(termlog_handler)
    logger.setLevel(logging.INFO)

def main():

    # set logger config
    #logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    log_setup()

    # Init BaseClass
    if os.path.isfile('./app_config.json'):
        with open('./app_config.json') as json_file:
            app = BaseClass( json.loads(json_file.read()))
    elif os.getenv('MY_APP_CONFIG') is None: app = BaseClass()
    else: app = BaseClass ( json.loads(os.getenv('MY_APP_CONFIG')))

    my_model = MyModel()
    
    app.start(my_model)

    # start Flask message handler here
    msg_handler = init_handler(app)

    flaskapp = msg_handler.get_flask_app()

    @flaskapp.route('/test')
    def test():
        return 'custom msg handler test page'

    flaskapp.run(host="0.0.0.0", threaded=True)

    #while True:
    #    time.sleep(1)

main()
