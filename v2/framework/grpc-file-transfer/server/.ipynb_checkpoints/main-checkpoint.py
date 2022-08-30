import argparse
import logging

from server.server import FileServer

def main():
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description="gRPC file transfer server")
    parser.add_argument(
        "-i", "--ip_adress", required=True, type=str, help="IP address for server")
    parser.add_argument(
        "-p", "--port", required=True, type=str, help="port address for server")
    parser.add_argument(
        "-w", "--max_workers",required=True, type=int, help="maximum worker threads for server")
    parser.add_argument(
        "-d", "--files_directory", required=True, type=str, help="directory containing files")
    parser.add_argument(
        "-priv", "--private_key_file", required=False, type=str, help="private key file path")
    parser.add_argument(
        "-cert", "--cert_file", required=False, type=str, help="certificate file path")
    args = parser.parse_args()

  
    # secure
    if args.private_key_file and args.cert_file:
        logger.info(
            "ip_adress:{ip_adress}, \
            port:{port}, \
            max_workers:{max_workers}, \
            files_directory:{files_directory}, \
            private_key_file:{private_key_file}, \
            cert_file:{cert_file}"\
            .format(
              ip_adress=args.ip_adress,
              port=args.port,
              max_workers=args.max_workers,
              files_directory=args.files_directory,
              private_key_file=args.private_key_file,
              cert_file=args.cert_file))
    # insecure
    else:
        logger.info(
            "ip_adress:{ip_adress}, \
            port:{port}, \
            max_workers:{max_workers}, \
            files_directory:{files_directory}"\
            .format(
              ip_adress=args.ip_adress,
              port=args.port,
              max_workers=args.max_workers,
              files_directory=args.files_directory))
        
    server = FileServer(
        args.ip_adress,
        args.port,
        args.max_workers,
        args.files_directory,
        args.private_key_file,
        args.cert_file)

    server.start()

if __name__ == "__main__":
    main()
