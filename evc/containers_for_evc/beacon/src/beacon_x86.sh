#!/bin/bash
echo "Running on x86 architecture (ver 1.2, BASH)"

# x86-specific commands here

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
    temperature=$((paste <(cat /sys/class/thermal/thermal_zone*/type) <(cat /sys/class/thermal/thermal_zone*/temp) | column -s $'\t' -t | sed 's/\(.\)..$/.\1°C/' | grep x86_pkg_temp) | grep -oE '[0-9]+(\.[0-9]+)?' | tail -1)
    #cpuclock=$(lscpu | grep 'CPU MHz' | grep -oE '[0-9]+(\.[0-9]+)?')
    cpuclock=$(awk -F': ' '/cpu MHz/ {print $2; exit}' /proc/cpuinfo)
    mem=$(free -m | awk 'NR==2{printf "%s", $3 }')
    #temperature=1.1
    #cpuclock=1
    #mem=2
    curl -X 'GET' http://evc.re.kr:20080/puship.php?hostname=${hostname}\&temperature=${temperature}\&cpuclock=${cpuclock}\&mem=${mem}
    echo ${hostname}, ${temperature}, ${cpuclock}, ${mem}
    sleep 60
done