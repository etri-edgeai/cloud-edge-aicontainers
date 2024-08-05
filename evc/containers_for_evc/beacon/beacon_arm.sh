#!/bin/sh
echo "Running on ARM architecture"
# ARM-specific commands here

#------------------------------------------------
# - Usage
#     nohup bash beacon.sh &
#
# - by JPark @ KETI, 2023
#
# - Examples of vcgencmd
#   vcgencmd version
#   vcgencmd commands
#   vcgencmd get_mem arm
#   vcgencmd get_mem gpu
#   vcgencmd measure_volts
#   vcgencmd measure_temp
#   vcgencmd measure_clock arm
#------------------------------------------------

hostname=$(uname -n)

while true; do
    temperature=$(sudo vcgencmd measure_temp | grep -oE '[0-9]+(\.[0-9]+)?')
    cpuclock=$(sudo vcgencmd measure_clock arm | grep -Eo '[0-9]{4,10}')
    mem=$(sudo vcgencmd get_mem arm | grep -oE '[0-9]+.')
    curl http://evc.re.kr:20080/puship.php?hostname=${hostname}\&temperature=${temperature}\&cpuclock=${cpuclock}\&mem=${mem}
    echo ${temperature}
    echo ${hostname}
    sleep 60
done