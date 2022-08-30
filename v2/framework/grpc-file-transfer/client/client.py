import logging
import os
import time

import grpc

import protos.file_pb2 as file_pb2
import protos.file_pb2_grpc as file_pb2_grpc
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CHUNK_SIZE = 1024 * 1024 # 1MB


class FileClient:

    def __init__(self, ip_address, port, from_id, to_id, cert_file):
        self.__ip_address = ip_address
        self.__port = port
        self.__from_id = from_id
        self.__to_id = to_id
        self.__cert_file = cert_file

        try:
            with open(self.__cert_file, "rb") as fh:
                trusted_cert = fh.read()
            self.__is_secure_channel = True
        except:
            self.__is_secure_channel = False


        if self.__is_secure_channel:
            credentials = grpc.ssl_channel_credentials(root_certificates=trusted_cert)
            channel = grpc.secure_channel("{}:{}".format(self.__ip_address, self.__port), credentials)
        else:
            channel = grpc.insecure_channel("{}:{}".format(self.__ip_address, self.__port))
        
        self.stub = file_pb2_grpc.FileStub(channel)

        logger.info("[d] created instance " + str(self))

    def list(self, from_id):
        logger.info("[d] downloading files list from server")
        response_stream = self.stub.list(file_pb2.ListRequest(from_id=from_id))
        self.__list_files(response_stream)


    def download(self, file_name, from_id, out_file_name, out_file_dir):
        logger.info("[d] downloading file:{file_name}, from_id:{from_id}, to {out_file_dir}/{out_file_name}"
          .format(
            file_name=file_name,
            from_id=from_id,
            out_file_dir=out_file_dir,
            out_file_name=out_file_name))
        response_stream = self.stub.download(file_pb2.FileDownloadRequest(name=file_name, from_id=from_id))
        self.__file_server2client(response_stream, out_file_name, out_file_dir)

        
    def __file_server2client(self, response_stream, out_file_name, out_file_dir):
        try:
            with open(out_file_dir + "/" + out_file_name, "wb") as fh:
                for response in response_stream:
                    fh.write(response.buffer)
        except grpc.RpcError as e:
            status_code = e.code()
            logger.error("[-] Error details: {}, status name: {}, status value: {}"
                .format(e.details(), status_code.name, status_code.value))



    # by JPark
    def upload(self, fpath4upload, from_id, to_id):
        
        if os.path.isfile(fpath4upload):
            logger.info('-'*50)
            logger.info("[d] uploading file:{fpath4upload}".format(fpath4upload=fpath4upload))
            chunks_generator = self.__file_client2server(fpath4upload, from_id, to_id)
            response = self.stub.upload(chunks_generator)
            logger.info('[d] response.file_size = {file_size}'.format(file_size=response.file_size))
            if ( response.file_size == os.path.getsize(fpath4upload) ):
                logger.info('[+] success! file uploaded')
            logger.info('-'*50)
        
        else:
            logger.error('[-] file open error')
       
    # by JPark
    def __file_client2server(self, fpath, from_id, to_id):
        head, fname = os.path.split(fpath)
        
        try:
            with open(fpath, 'rb') as f:
                while True:
                    piece = f.read(CHUNK_SIZE);
                    if len(piece) == 0:
                        break     
                    yield file_pb2.FileChunk(buffer=piece, name=fname, from_id=from_id, to_id=to_id)
        except:
            yield file_pb2.FileChunk()

        
    def __list_files(self, response_stream):
        a = []
        for response in response_stream:
            b= {'name' : response.name, 'size' : response.size}
            a.append(b)
            
        #logger.info( json.dumps(a) )
        print( '-'*50 )
        print( 'files = ' )
        print( json.dumps(a) )
        print( '-'*50 )

    def __str__(self):
        
        if self.__is_secure_channel:
            s = "[d] ip:{ip_address}, port:{port}, from_id:{from_id}, to_id:{to_id}, cert_file:{cert_file}"\
              .format(
                ip_address=self.__ip_address,
                port=self.__port,
                from_id=self.__from_id,
                to_id=self.__to_id,
                cert_file=self.__cert_file)
        else:
            s = "[d] ip:{ip_address}, from_id:{from_id}, to_id:{to_id}, port:{port}"\
              .format(
                ip_address=self.__ip_address,
                from_id=self.__from_id,
                to_id=self.__to_id,
                port=self.__port)
            
        return s