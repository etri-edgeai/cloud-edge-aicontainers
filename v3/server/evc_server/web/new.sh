#!/bin/bash

#--------------------------------------------------
# newedge.sh
# 
# - usage :
#
#   $ wget http://evc.re.kr/newedge.sh -O newedge.sh
#
#   $ bash newedge.sh
#  
# - by : J. Park, KETI, 2023 
#--------------------------------------------------

# add edge device
function common {
    echo "Raspberry PI"
    sudo apt update
    sudo apt upgrade
    echo 'install openssh-server'
    sudo apt install openssh-server
    echo "IPQoS cs0 cs0" | sudo tee --append /etc/ssh/sshd_config
    sudo cat /etc/ssh/sshd_config
    mkdir ~/.ssh
    
    echo 'install git'
    sudo apt install git
    sudo apt install curl
    
    echo "alias dir='ls -al'" | tee -a ~/.bashrc
    
    # Add authorized key
    curl -X GET http://evc.re.kr:20080/api/get_key.php >> ~/.ssh/authorized_keys
}


function rpi {
    common
}

function ubuntu {
    common
}

function macos {
    echo "MacOS"
    
    # Add authorized key
    curl -X GET http://evc.re.kr:20080/api/get_key.php >> ~/.ssh/authorized_keys
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
       platform='ubuntu'
    elif [[ "$CODE" == 'ubuntu' ]]; then
       platform='ubuntu'
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
elif [[ "$platform" == 'rpi' ]]; then
    rpi
elif [[ "$platform" == 'ubuntu' ]]; then
    ubuntu
elif [[ "$platform" == 'FreeBSD' ]]; then
    echo 'todo'
elif [[ "$platform" == 'macos' ]]; then
    macos
else
    common
fi




