#!/bin/bash

while :
do
    now=$(date +"%Y/%m/%d-%H:%M:%S")
    echo "### $now ###"
    sh run_get_temperature.sh
    sleep 5
    echo
done
