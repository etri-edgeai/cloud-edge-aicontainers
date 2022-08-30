import argparse
import logging
import sys

from client.client import FileClient

def main():
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    logger = logging.getLogger(__name__)

    # root parser
    parser = argparse.ArgumentParser(description="gRPC file transfer client")
    parser.add_argument(
        "-i", "--ip_adress", required=True, type=str, help="IP address of server")
    parser.add_argument(
        "-p", "--port", required=True, type=str, help="port address of server")
    parser.add_argument(
        "-m", "--from_id", required=True, type=int, help="{0: master}, {1,2,3... : edge}")
    parser.add_argument(
        "-n", "--to_id", required=False, type=int, help="{0: master}, {1,2,3... : edge}")
    parser.add_argument(
        "-c", "--cert_file", required=False, type=str, help="certificate file path")

    # subparsers
    subparsers = parser.add_subparsers(dest="action", help="client possible actions")
    subparsers.required = True

    # subparser : download
    download_parser = subparsers.add_parser("download", help="download file from server")
    download_parser.add_argument(
        "-d", "--directory", required=True, type=str, help="where to save files")
    download_parser.add_argument(
        "-f", "--file", required=True, type=str, help="file name to download")

    # by JPark
    # subparser : upload
    upload_parser = subparsers.add_parser("upload", help="upload file from server")
    upload_parser.add_argument(
        "-f", "--file", required=True, type=str, help="file name to upload")


    # subparser : list
    subparsers.add_parser("list", help="list files on server")

    # parser
    args = parser.parse_args()

    if args.cert_file:
        logger.info("ip_adress:{ip_adress}, port:{port}, from_id:{from_id}, to_id:{to_id}, cert_file:{cert_file}, action:{action}"
        .format(
            ip_adress=args.ip_adress,
            port=args.port,
            from_id=args.from_id,
            to_id=args.to_id,
            cert_file=args.cert_file,
            action=args.action))
    
    else:
        logger.info("ip_adress:{ip_adress}, port:{port}, from_id:{from_id}, to_id:{to_id}, action:{action}"
        .format(
            ip_adress=args.ip_adress,
            port=args.port,
            from_id=args.from_id,
            to_id=args.to_id,
            action=args.action))
        
    client = FileClient(args.ip_adress, args.port, args.from_id, args.to_id, args.cert_file)

    action = args.action
    if action == "download":
        client.download(args.file, args.from_id, args.file, args.directory)
    elif action == "upload":
        client.upload(args.file, args.from_id, args.to_id)
    elif action == "list":
        client.list(args.from_id)
    else:
        logger.error("no such action " + action)

if __name__ == "__main__":
    main()
