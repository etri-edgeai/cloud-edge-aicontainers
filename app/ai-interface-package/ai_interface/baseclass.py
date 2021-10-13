import logging, sys, os
import zipfile
import pickle
from urllib.request import urlopen, urlretrieve
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
import requests
import inspect

from ai_interface.appconfig import AppConfig
from ai_interface.model import model_manager

class BaseClass:
    """
    :class: BaseClass for AI applicaiton to be implemented.

    This BaseClass defines structure of an AI application, suitable for microservice implementation.

    AI application develpoers can use this class to implement their own application. Just create an instance of this class, and override several methods. Or, create a inhereted class from this one and then override some methods or implement new methods for the inhereted class.

    """
    def __init__(self, jsonconfig = None):
        """
        :param: appconfig instance to store configuration values for this applicaiton.

        """
        logging.info("BaseClass Init called")
        self.appconfig = AppConfig(jsonconfig)

        """
        self.load_ai_model()

        if ( self.appconfig.get_input_source().scheme == 'mqtt' ):
            self.mqttinput = mqtt.Client()
            self.register_mqtt_handle_input()
            self.connectSrc()
            self.mqttinput.loop_start()

        if ( self.appconfig.get_destination().scheme == 'mqtt'):
            self.mqttoutput= mqtt.Client()
            self.register_mqtt_handle_output()
            self.connectDst()
            self.mqttoutput.loop_start()

        logging.info("AUTOSTART = :" + self.appconfig.get_autostart() )
        if ( self.appconfig.get_input_source().scheme == 'http') and (self.appconfig.get_autostart() == 'True' ):
            # MQTT is auto-start by nature
            logging.info("starting compute_ai, HTTP and AUTOSTART")
            self.compute_ai()
        """
    def start( self, MyModel ):
        self.model = MyModel
        #model_file = self.download_ai_model()

        self.load_ai_model( )

#        if ( self.appconfig.get_input_source().scheme == 'mqtt' ):
#            self.mqttinput = mqtt.Client()
#            self.register_mqtt_handle_input()
#            self.connectSrc()
#            self.mqttinput.loop_start()

        # destination can be multiple.
        self.mqttoutput = {}
        self.httpoutput = {}
        for key, url in self.appconfig.get_destination().items():
            if (url.scheme == 'mqtt'):
                self.mqttoutput[key] = mqtt.Client()
                self.register_mqtt_handle_output(key)
                self.connectDst(key)
                self.mqttoutput[key].loop_start()
            elif (url.scheme == 'http'):
                self.httpoutput[key] = url.geturl()

        if ( self.appconfig.get_input_source().scheme == 'mqtt' ):
            self.mqttinput = mqtt.Client()
            self.register_mqtt_handle_input()
            self.connectSrc()
            self.mqttinput.loop_start()

        logging.info("AUTOSTART = :" + self.appconfig.get_autostart() )
        if ( self.appconfig.get_input_source().scheme == 'http') and (self.appconfig.get_autostart() == 'True' ):
            # MQTT is auto-start by nature
            logging.info("starting compute_ai, HTTP and AUTOSTART")

            # result from compute_ai() is dict type.
            result = self.compute_ai(self.appconfig.get_input_source().geturl())
            #self.fire_notification(result)

    def connectSrc(self):
        logging.info("Connecting to a source")

        inputsource = self.appconfig.get_input_source()

        # Where this code needs to be placed?
        #if inputsource.scheme == "http":
        #    logging.info("using http protocol")
        #    if self.appconfig.get_autostart == 'True':
        #        logging.info("autostart is TRUE, starting compute_ai()")
        #        self.compute_ai()

        if inputsource.scheme == "mqtt":
            logging.info("using mqtt protocol")
            # TODO default port
            self.mqttinput.connect(inputsource.hostname, inputsource.port)
            logging.info ("source server : " + inputsource.hostname)
            logging.info ("source port : " + str(inputsource.port))
            self.mqttinput.subscribe(inputsource.path, 2)
            logging.info ("source path : " + inputsource.path)

        else:
            logging.error("not supported url - scheme: " + inputsource.scheme)

    def connectDst(self, key):
        logging.info("Connecting to a dest")

        dest = self.appconfig.get_destination()[key]

        if dest.scheme == "mqtt":
            logging.info("using mqtt protocol for output")
            # TODO default port
            self.mqttoutput[key].connect(dest.hostname, dest.port)

        else:
            logging.error("not supported url - scheme: " + dest.scheme)

    def register_mqtt_handle_input(self):

        def on_connect(client, userdata, flags, rc):
            logging.info('input-connect')

        def on_message(client, userdata, message):
            logging.info('input-message')
            logging.info('meesage topic =' + message.topic)
            logging.info('input source=' + self.appconfig.get_input_source().path)

            if message.topic == self.appconfig.get_input_source().path:
                body = pickle.loads(message.payload)
                result = self.compute_ai(body)
                """
                if ( self.appconfig.get_destination.scheme == "mqtt"):
                    self.fire_notification( str(retVal))
                    logging.info('output fired to : ' + self.appconfig.get_destination().path)
                elif ( self.appconfig.get_destination.scheme == "http"):
                    logging.info("sending output with HTTP")
                else:
                    logging.error("unkonw destination. discarding compute_ai result")
                """
                #self.fire_notification(result)

        def on_publish(client, userdata, mid):
            logging.info('input-publish')

        def on_subscribe(client, userdata, mid, granted_qos):
            logging.info('input-subscribe')

        self.mqttinput.on_message = on_message
        self.mqttinput.on_connect = on_connect
        self.mqttinput.on_publish = on_publish
        self.mqttinput.on_subscribe = on_subscribe

    def register_mqtt_handle_output(self, key):

        def on_connect(client, userdata, flags, rc):
            logging.info('output-connect')

        def on_message(client, userdata, message):
            logging.info('output-message')

        def on_publish(client, userdata, mid):
            logging.info('output-publish')

        def on_subscribe(client, userdata, mid, granted_qos):
            logging.info('output-subscribe')

        self.mqttoutput[key].on_message = on_message
        self.mqttoutput[key].on_connect = on_connect
        self.mqttoutput[key].on_publish = on_publish
        self.mqttoutput[key].on_subscribe = on_subscribe


    def load_ai_model(self):
        """
        this method download the AI model file to the designated volume if it's not there, and then load AI model onto memory. AI model information (including location of AI model files) are stored in the appConfig.

        :param str model_url: designates location of model file. shall be represented in URL (i.e. http://server/model_file)
        :param str volume_name: volume to store downloaded model. shall be represnted in PATH type (i.e. /, /volume ) It is a good excercise to store model on volume on the host to avoid download AI model every time container is started.

        .. todo:: check validity of parameters.
         """
        logging.info("load_ai_model called")

        if (self.get_app_config().model_url.startswith('file')):
            self.appconfig.set_model_status('loaded')
            return

        self.appconfig.set_model_status('loading')
        model_file = self.download_ai_model()
        ret = self.model.load_ai_model( model_file )
        if ( ret == 0 ):
            logging.info ("model loading done")
            self.appconfig.set_model_status('loaded')

    def download_ai_model(self):
        #volume_name = self.appconfig.get_model_volume()
        
        model_info = {
            "model_name":self.get_app_config().model_name,
            "model_version":self.get_app_config().model_version,
            "model_split":"Split_No",
            "split_number":"0"
        }

        model_downloader = model_manager()
        model_downloader.set_model_info(model_info)
        model_downloader.set_model_repository(self.get_app_config().model_url)

        model_file_name = self.get_app_config().model_name + "_" + str(self.get_app_config().model_version) + ".zip"
        if os.path.isfile(model_file_name) is True:
            print('file exist, not downloaing flle :' + model_file_name )
        else:
            model_downloader.set_stored_file_name(model_file_name)
            model_downloader.model_save( model_downloader.model_download() )

        """
        model_url = self.appconfig.get_model_url()

        logging.info('downloading AI model from : '+ str(model_url) )

        file_name = "/" + model_url.path.split('/')[-1]

        if os.path.isfile( file_name ):
            logging.info('Model file exists. Not downloading' )
            return (file_name)

        urlretrieve (model_url.geturl(), file_name)
        logging.info('download complete!' )
        """
        return model_file_name

    def preprocess_input(self, *args):
        """
        this methods opens the data source, which is designated in appconfig, and then process those data to make them suitable to be fed to the input layer of model to be used. AI applicaiton develpoer needs to override this method.
        .. todo:: to be implemented.
        """
        logging.info("preprocess_input called")
        return

    def postprocess_output(self, *args):
        """
        this methods interprets the scores which is produced in the output layer of the model.

        .. todo:: to be implemented.
        """
        logging.info("postproces_output called")
        return

    def compute_ai(self, *args):
        """
        this methods computes AI methods by applying preprocessed input data to the input layer of AI model.

        :param str input_source: input_source location. This methods will be called from FlaskHandler in usual cases, with the value saved in appconfig.
        """

        if ( self.appconfig.get_model_status() != 'loaded' ):
            logging.info("model file is not ready")
            return (-1, None)

        inputsource = self.appconfig.get_input_source()

        logging.info("compute_ai called")
        logging.info("retrieven input source from: " + inputsource.geturl())

        print("input source scheme : " + inputsource.scheme)

        if inputsource.scheme == "mqtt":
            print("input source scheme is mqtt" )
            val = self.model.compute_ai(args[0])
        else : #inputsource.scheme == "http":
            print("input source scheme is http" )
            val = self.model.compute_ai(inputsource.geturl())

        """
        if ( self.appconfig.get_destination().scheme == "mqtt"):
            logging.info('output fired to : ' + self.appconfig.get_destination().path)
            self.fire_notification( "test" )
        elif ( self.appconfig.get_destination().scheme == "http"):
            logging.info("sending output with HTTP")
        else:
            logging.error("unkonw destination. discarding compute_ai result")
        """

        if inspect.isgeneratorfunction( self.model.compute_ai):
            print('GENERATOR type returned')
            for item in val:
                self.fire_notification(item)
                
        #else:
        #    self.fire_notification(val)

        return 0

    def compute_ai_stream(self, *args):
        if ( self.appconfig.get_model_status() != 'loaded' ):
            logging.info("model file is not ready")
            return (-1, None)

        inputsource = self.appconfig.get_input_source()

        logging.info("compute_ai called")
        logging.info("retrieven input source from: " + inputsource.geturl())

        print("input source scheme : " + inputsource.scheme)


        val = self.model.compute_ai_stream(inputsource.geturl())

        return val
        


    def stop_ai(self):
        """
        request termination of AI method

        .. todo:: to be implemented.
        """
        logging.info("stop_ai called")
        return "OK, Stop AI"

    def fire_notification(self, retVals ):
        """
        send notification to the client. The destination is designated in appconfig.

        .. todo:: to be implemented.
        """
        logging.info("fire_notification called")

        for key, ret in retVals.items():
            if key in self.mqttoutput:
                body = pickle.dumps(ret, protocol=3)
                infot = self.mqttoutput[key].publish(self.appconfig.get_destination()[key].path, body, qos=2)
                logging.info('output fired to : ' + self.appconfig.get_destination()[key].path)
                infot.wait_for_publish()
            elif key in self.httpoutput:
                response = requests.post(url = self.httpoutput[key], data=str(ret))
                logging.info('output fired to : ' + self.httpoutput[key])
                logging.info('Response : ' + str(response))
            

        #self.mqttinput.loop_start()
        #for key, ret in retVals.items():
        #    body = pickle.dumps(ret, protocol=3)
        #    infot = self.mqttoutput[key].publish(self.appconfig.get_destination()[key].path, body, qos=2)
        #    logging.info('output fired to : ' + self.appconfig.get_destination()[key].path)
        #    infot.wait_for_publish()

    def set_config(self, config_name, config_value):
        logging.info("set config of app with name = " + config_name + ", value = " + config_value )

    def get_config(self, config_name):
        logging.info("get config of app with name = " + config_name)

    def get_app_config(self):
        return self.appconfig
