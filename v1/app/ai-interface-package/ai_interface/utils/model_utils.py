def download_ai_model( model_url, file_url="/" ):
    #volume_name = self.appconfig.get_model_volume()
    model_url = self.appconfig.get_model_url()
    logging.info('downloading AI model from : '+ str(model_url) )
    
    file_name = "/" + model_url.path.split('/')[-1]

    if os.path.isfile( file_name ):
        logging.info('Model file exists. Not downloading' )
        return (file_name)

    urlretrieve (model_url.geturl(), file_name)
    logging.info('download complete!' )

    return file_name
