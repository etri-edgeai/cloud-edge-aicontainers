#!/usr/bin/env bash
set -e

SCRIPT_DIR=$(dirname $(readlink -f $0))
cd $SCRIPT_DIR

if [ -z ${1} ]; then
  echo "Wrong number of paramaters.";
  echo "Usage: generate.sh /CN=CommonName";
  echo "CN = Common Name";
  exit 1;
fi

echo "arg is " ${1}
openssl genrsa -out server.key 2048
openssl req -new -x509 -sha256 -key server.key -out server.crt -days 365 -subj ${1}
