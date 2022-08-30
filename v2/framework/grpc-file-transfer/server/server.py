from concurrent import futures
import logging
import os
import time

import grpc

import protos.file_pb2 as file_pb2
import protos.file_pb2_grpc as file_pb2_grpc

logger = logging.getLogger(__name__)

CHUNK_SIZE = 1024 * 1024 # 1MB
TEMPFILE_NAME = "temp_file" # Hard coded


def makedir(path): 
    try: 
        os.makedirs(path)
        
    except OSError: 
        if not os.path.isdir(path): 
            raise
    
    return os.path.abspath(path)

class FileServicer(file_pb2_grpc.FileServicer):
  
    def __init__(self, files_directory):
        self.__files_directory = files_directory

        
    def list(self, request, context):
        from_id = request.from_id
        
        try:
            logger.info("[d] sending files list")
            files = [(f, os.path.getsize(self.__files_directory + "/" + str(from_id) + '/' + f))
                for f
                in os.listdir(self.__files_directory + "/" + str(from_id))
                if os.path.isfile(self.__files_directory + "/" + str(from_id) + '/' + f)]

            print( self.__files_directory + "/" + str(from_id) + '/' )
            print(files)

            if len(files) == 0:
                yield file_pb2.ListResponse()
            else:
                for file in files:
                    yield file_pb2.ListResponse(name=file[0], size=file[1])
        except:
            yield file_pb2.ListResponse()
            
    def download(self, request, context):
        file_name = request.name
        from_id = request.from_id
        fpath = self.__files_directory + "/" + str(from_id) + "/" + file_name
        
        if os.path.isfile(fpath):
            logger.info("[d] sending file={file_name} to from_id={from_id}".format(file_name=file_name, from_id=from_id))
            with open(fpath, "rb") as fh:
                while True:
                    piece = fh.read(CHUNK_SIZE)
                    if len(piece) == 0:
                        break
                    yield file_pb2.FileChunk(buffer=piece, from_id=from_id)
                logger.info("[+] download success, {}".format(fpath))
            
        else:
            error_detail = "[-] File: " + file_name + " not exists"
            logger.error(error_detail)
            context.set_details(error_detail)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            yield file_pb2.FileChunk()
        

    def upload(self, request_iterator, context):
        request1 = next(request_iterator)
        name = request1.name
        from_id = request1.from_id
        to_id = request1.to_id
        
        fdir = self.__files_directory + "/" + str(to_id)
        fdir = makedir(fdir)
        fpath_dst = fdir + f"/{name}"
        
        logger.info("[d] fpath_dst = {fpath_dst}, from_id = {from_id}, to_id={to_id}".format(fpath_dst=fpath_dst, from_id=from_id, to_id=to_id))
        self.__save_file(request_iterator, fpath_dst)
        file_size = os.path.getsize(fpath_dst)
        return file_pb2.FileUploadResponse(file_size=file_size)

    def __save_file(self, response_stream, fpath_dst):
        try:
            with open(fpath_dst, "wb") as fh:
                for response in response_stream:
                    fh.write(response.buffer)
                
                logger.info("[+] file uploaded ")
        except:
            logger.info("[-] error in file saving")


class FileServer():
    _ONE_DAY_IN_SECONDS = 60 * 60 * 24

    def __init__(self, ip_address, port, max_workers, files_directory, private_key_file, cert_file):
        self.__ip_address = ip_address
        self.__port = port
        self.__max_workers = max_workers
        self.__files_directory = files_directory
        self.__private_key_file = private_key_file
        self.__cert_file = cert_file

        try:
            with open(self.__private_key_file, "rb") as fh:
                private_key = fh.read()
            with open(self.__cert_file, "rb") as fh:
                certificate_chain = fh.read()
            self.__is_scure_channel = True
        except:
            self.__is_scure_channel = False
        
        if self.__is_scure_channel: # secure channel
            self.__server = grpc.server(futures.ThreadPoolExecutor(max_workers=self.__max_workers))
            file_pb2_grpc.add_FileServicer_to_server(FileServicer(self.__files_directory), self.__server)
            server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain,),))
            self.__server.add_secure_port(self.__ip_address + ":" + self.__port, server_credentials)
        
        else:
            self.__server = grpc.server(futures.ThreadPoolExecutor(max_workers=self.__max_workers))
            file_pb2_grpc.add_FileServicer_to_server(FileServicer(self.__files_directory), self.__server)
            self.__server.add_insecure_port(self.__ip_address + ":" + self.__port)

        logger.info("created instance " + str(self))

    def __str__(self):
        if self.__is_scure_channel:
            s = "ip:{ip_address},\
              port:{port},\
              max_workers:{max_workers},\
              files_directory:{files_directory},\
              private_key_file:{private_key_file},\
              cert_file:{cert_file}"\
              .format(
                ip_address=self.__ip_address,
                port=self.__port,
                max_workers=self.__max_workers,
                files_directory=self.__files_directory,
                private_key_file=self.__private_key_file,
                cert_file=self.__cert_file)
        else:
            s = "ip:{ip_address},\
              port:{port},\
              max_workers:{max_workers},\
              files_directory:{files_directory}"\
              .format(
                ip_address=self.__ip_address,
                port=self.__port,
                max_workers=self.__max_workers,
                files_directory=self.__files_directory)
    
        return s
    
    def start(self):
        logger.info("starting instance " + str(self))
        self.__server.start()
        try:
            while True:
                time.sleep(FileServer._ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            self.__server.stop(0)
