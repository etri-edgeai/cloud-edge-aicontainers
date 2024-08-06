#!/bin/sh

#------------------------------------------------
# - Usage
#     nohup bash beacon.sh &
#
# - by JPark @ KETI, 2024
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

hostname=$1

echo "Beacon v1.1"
while true; do
    # Get temperature
    temperature=$(sensors | grep -i 'temp1' | head -n 1 | awk '{print $2}' | tr -d '+°C')
    
    # Get CPU clock speed
    cpuclock=$(lscpu | grep "CPU max MHz" | awk '{print $4}')

    # Get available memory
    mem_max=$(free -m | awk 'NR==2{print $2}')
    
    # Get available memory
    mem_available=$(free -m | awk 'NR==2{print $7}')

    # Send data to server
    /usr/bin/curl "http://evc.re.kr:20080/puship.php?hostname=${hostname}&temperature=${temperature}&cpuclock=${cpuclock}&mem=${mem_available}"

    # Print data to console
    echo "${hostname}, ${temperature}, ${cpuclock}, ${mem_max}, ${mem_available}"
    
    # Wait for 60 seconds before next iteration
    sleep 1
done