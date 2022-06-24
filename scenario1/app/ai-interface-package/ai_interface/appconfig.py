"""
==================
:mod: 'appconfig'
==================

description
=============
contains AppConfig class definition and a utility function to create instance of that. This AppConfig class holds variables for AI application running.

"""
from urllib.request import urlopen, urlretrieve
from urllib.parse import urlparse

import logging, sys

class AppConfig:
    """
    :class: Class to hold configuration information and related methods to configure AI running environment.

    """

    def __init__(self, jsonconfig = None):
        if (jsonconfig != None):
            # input src must be only one.
            self.input_source_url = urlparse(jsonconfig['input']['url'])
            # destinations can be multiple.
            self.destination_url = {}
            for key, url in jsonconfig['output']['url'].items():
                self.destination_url[key] = urlparse(url)
            self.model_url = jsonconfig['ai_model']['url']
            self.model_name = jsonconfig['ai_model']['model_name']
            self.model_version = jsonconfig['ai_model']['model_version']
            self.autostart = jsonconfig['autostart']['value']
        else:
            self.input_source_url = ""
            self.destination_url = ""
            self.model_url = ""
            self.model_name = ""
            self.model_version = ""
            self.autostart = False

    def set_input_source(self, url):
        """
        to set location (URL) of source data to be analyzed.

        :param str url: URL of source data to be analyzed.
        """

        self.input_source_url = urlparse(url)

    def get_input_source(self):
        """
        to get current location of source data to be anlayzed.

        :return: URL of input source.
        """

        return self.input_source_url

    def set_destination(self, url):
        """
        to set location (URL) to where AI results will be delivered

        :param str url: URL of destination.
        """

        #self.destination_url = url
        return "not_implemented"

    def get_destination(self):
        """
        :return: URL of destination
        """

        return self.destination_url

    def set_model_url(self, url):
        """
        to set model type to be used in AI method.

        :param: str url: URL of a model
        """

        logging.info("model = " + srt(url))
        self.model_url = url

        # temporarily
        self.model_volume = "/"

        # self.app.load_ai_model()
    """
    def get_model_url(self):
        logging.info("returned model = " + str( self.model_url))
        return self.model_url

    def get_model_volume(self):
        logging.info("returned model volume = " + str(self.model_volume))
        return self.model_volume
    """
    def set_model_info(self, url, name, version):
            self.model_url = url
            self.model_name = name
            self.model_version = version

    def set_autostart(self, value):
        logging.info("set_autostart : " + value)
        self.autostart = value

    def get_autostart(self):
        logging.info("get_autostart : " + self.autostart)
        return self.autostart

    def set_model_status(self, model_status):
        logging.info("set_model_Status : " + model_status)
        self.model_status = model_status
        return

    def get_model_status(self):
        logging.info("get_model_Status : " + self.model_status)
        return self.model_status
