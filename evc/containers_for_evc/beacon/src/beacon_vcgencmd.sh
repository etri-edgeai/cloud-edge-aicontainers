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
    temperature=$(vcgencmd measure_temp | grep -oE '[0-9]+(\.[0-9]+)?')
    cpuclock=$(vcgencmd measure_clock arm | grep -Eo '[0-9]{4,10}')
    mem=$(vcgencmd get_mem arm | grep -oE '[0-9]+.')
    /usr/bin/curl http://evc.re.kr:20080/puship.php?hostname=${hostname}\&temperature=${temperature}\&cpuclock=${cpuclock}\&mem=${mem}
    echo ${hostname}, ${temperature}, ${cpuclock}, ${mem}
    sleep 60
done