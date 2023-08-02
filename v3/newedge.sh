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
function rpi {
    echo "Raspberry PI"
    sudo apt update
    sudo apt upgrade
    echo 'install openssh-server'
    sudo apt install openssh-server
    echo "IPQoS cs0 cs0" | sudo tee --append /etc/ssh/sshd_config
    sudo cat /etc/ssh/sshd_config
    mkdir ~/.ssh
    
    # Add authorized key
    curl -X GET http://evc.re.kr/api/get_key.php >> ~/.ssh/authorized_keys
}

function ubuntu_focal {
    echo "ubuntu_focal, Desktop"
    sudo apt update
    sudo apt upgrade
    sudo apt install openssh-server
    echo "IPQoS cs0 cs0" | sudo tee --append /etc/ssh/sshd_config
    sudo cat /etc/ssh/sshd_config
    mkdir ~/.ssh
        
    # Add authorized key
    curl -X GET http://evc.re.kr/api/get_key.php >> ~/.ssh/authorized_keys
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




