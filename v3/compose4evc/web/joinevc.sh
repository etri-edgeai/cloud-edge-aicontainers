#!/bin/bash

#--------------------------------------------------
# joinevc.sh
# 
# - usage :
#
#   $ wget http://evc.re.kr/joinevc.sh -O joinevc.sh
#
#   $ bash joinevc.sh
#  
# - by : J. Park, KETI, 2023 
#--------------------------------------------------

# add edge device
function rpi {
    echo : 'rpi'
    echo : $(lsb_release -d -s)
}

function ubuntu_focal {
    echo : 'ubuntu_focal'
    echo : $(lsb_release -d -s)
    mkdir ~/.evc
}


OS=$(uname)
#echo "$OS"

ARCH=$(uname -m)
#echo "$ARCH"

#--------------------------------------------------
# Check and install for this platform
#--------------------------------------------------

if [[ "$OS" == 'Linux' ]]; then
    platform='linux'
   
    CODE=$(lsb_release -c -s)
    if [[ "$CODE" == 'lunar' ]]; then
       platform='rpi_lunar'
    elif [[ "$CODE" == 'bullseye' ]]; then
       platform='rpi_bullseye'
    elif [[ "$CODE" == 'focal' ]]; then
       platform='ubuntu_focal'
    fi   
elif [[ "$OS" == 'FreeBSD' ]]; then
    platform='freebsd'
elif [[ "$OS" == 'Darwin' ]]; then
    platform='macos'
fi
echo 'Platform' : $platform


# install & update
if [[ "$platform" == 'rpi_lunar' ]]; then
    rpi
elif [[ "$platform" == 'rpi_bullseye' ]]; then
    rpi
elif [[ "$platform" == 'ubuntu_focal' ]]; then
    ubuntu_focal
elif [[ "$platform" == 'FreeBSD' ]]; then
    echo 'todo'
elif [[ "$platform" == 'macos' ]]; then
    echo 'todo'
fi




