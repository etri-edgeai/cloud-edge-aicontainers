#!/bin/sh
#------------------------------------------------
# - Usage
#     nohup bash beacon.sh &
#
# - by JPark @ KETI, 2024
#------------------------------------------------
hostname=$1

echo "Beacon v1.1"
while true; do
    # Get temperature
    temperature=$(sensors | grep -i 'temp1' | head -n 1 | awk '{print $2}' | tr -d '+°C')
    
    # Get CPU clock speed
    cpuclock=$(lscpu | grep "CPU max MHz" | awk '{print $4}')

    # Get available memory
    mem_total=$(free -m | awk 'NR==2{print $2}')
    
    # Get available memory
    mem_available=$(free -m | awk 'NR==2{print $7}')

    # Send data to server
    /usr/bin/curl "http://evc.re.kr:20080/beacon.php?hostname=${hostname}&temperature=${temperature}&cpuclock=${cpuclock}&mem_total=${mem_total}&mem_avilable=${mem_available}"

    # Print data to console
    #echo "${hostname}, ${temperature}, ${cpuclock}, ${mem_max}, ${mem_available}"
    
    # Wait for 60 seconds before next iteration
    sleep 60
done