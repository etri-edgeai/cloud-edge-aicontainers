"""
This module is to provide RESTful interfaces for the DECENTER pacakge.

:class: DecenterFlask

This class contains Flask application instance, and handle for appconfig.

:func: init_handler

Utility funcion to create and configure DecenterFlask instance. Also, all the routing functions for Flask app are defined in this function.

"""

from flask import Flask
from flask import request
from flask import Response

from flask_cors import CORS

import logging, sys

class DecenterFlask():
    """
    :class: DecenterFlask

    This class creates and hods instance of Flask class. While being initialized, this class receives one parameter: instance of :class:`decenter.ai.appconfig` class. Basically, this class is a message handler between RESTful interface (Flask) and the internal decenter.ai.appconfig. When it receives a HTTP request to a specific RESTful endpoint, it calls corresponding methods of :class:`~decenter.ai.appconfig` or :class:`~decenter.ai.baseclass.BaseClass`.

    To use this class, call :func:`~decenter.ai.flask.init_handler`. It will return the instance of this DecenterFlask. Remember, this init_handler() call does not start Flask app by itself. You have to run explicitly by calling app.run() method of the Flask instance. To access Flask inside the :class:'decenter.ai.flask.DecenterFlask', call :func:'get_flask_app'.

    """
    def __init__(self, app):
        self.flask = Flask(__name__)
        self.app = app

        #if custom_handler!=None:
        #    import_module( custom_handler )

    def get_flask_app(self):
        """
        :return: instance of Flask app.
        """

        return self.flask

    def get_app(self):
        logging.info('get app called')
        return self.app

#    def setAppConfig(self, appconfig):
#        """
#        instance methods to set the appconfig variable. This variable will be used to configrue AI applicaiton with respect to the configuration messages.
#        :param AppConfig appconfig: instance of AppConfig.
#        """

#        self.appconfig = appconfig

def init_handler(app):
    """
    Utility function to intialize DecenterFlask, and set appconfig and custom message handler.

    :param: AppConfig appConfig: instance of appconfig.
    :param: str custom_handler: name of custom handler module (not file name - do not include .py extension)

    """
    #global msghandler

    msghandler = DecenterFlask(app)

    flask = msghandler.get_flask_app()
    CORS(flask)

    #msghandler.setAppConfig(appConfig)

    # default handler in decenter pacakge
    #import decenter.ai.flaskhandler

    # add custmo handler here
    #if custom_handler!=None:
    #    import_module( custom_handler )

    #msghandler.run(host='0.0.0.0')


    @flask.route('/')
    def index():
        """

            Replies to index page

        """
        return 'index page'

    @flask.route('/hello')
    def hello():
        return 'Hello, World'

    @flask.route('/set_input')
    def setinput():
        """
            set URL location of input source to be fed to the input layer of AI model.

            :param source_url: URL of source media
            :status 200: when everything is OK
        """
        sourceurl = request.args.get('url')
        logging.info('set input received with value: ' + sourceurl)

        global msg_handler
        msghandler.get_app().get_app_config().set_input_source( sourceurl )
        return 'set input completes'

    @flask.route('/get_input')
    def getinput():
        """
            returns current input media.

            :status 200: when everything is OK
        """
        global msg_handler

        str = msghandler.get_app().get_app_config().get_input_source()
        return str

    @flask.route('/set_output')
    def setoutput():
        """
        """
        dsturl = request.args.get('url')
        logging.info('set output received with value: ' + dsturl )

        global msg_handler
        msghandler.get_app().get_app_config().set_destination( dsturl )
        return 'set output completes'

    @flask.route('/get_output')
    def getoutput():
        """
        """
        global msg_handler

        str = msghandler.get_app().get_app_config().get_destination()
        return str


    @flask.route('/set_model')
    def setmodel():
        """
        """
        model_server_url = request.args.get('server')
        model_name = request.args.get('model_name')
        model_version = request.args.get('model_version')
        logging.info('set model received with value: ' + model_server_url + ", " + model_name + ", " + model_version)

        global msg_handler
        msghandler.get_app().get_app_config().set_model_info( model_server_url, model_name, model_version )
        return 'set model completes'

    @flask.route('/compute')
    def compute():
        """
            Request computation result of AI model.

            :status 200: when everything is OK
        """
        global msg_handler

        value = msghandler.get_app().compute_ai()
        logging.info('returning response')
        #return Response(msghandler.get_app().compute_ai(),
        #            mimetype='multipart/x-mixed-replace; boundary=frame')
        if(value == 0):
            retVal = "200 OK"
        else:
            retVal = "500 Internal Server Error."
        return retVal 

    @flask.route('/compute_stream')
    def compute_stream():

        """
            Request computation result of AI model.

            :status 200: when everything is OK
        """
        global msg_handler

        #value = msghandler.get_app().compute_ai()
        logging.info('returning response')
        return Response(msghandler.get_app().compute_ai_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
        #return value

    @flask.route('/stop_compute')
    def stop_compute():
        """
            Request to stop computation.

            :status 200: when everything is OK
        """
        global msg_handler

        value = msghandler.get_app().stop_compute()
        logging.info('stopping computation')
        return value

    return msghandler
    #app.run(host='0.0.0.0')
#todo how can I set custom message handler or override message handler?
