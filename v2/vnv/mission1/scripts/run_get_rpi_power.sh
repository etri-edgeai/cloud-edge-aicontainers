ansible rpi -m shell -a "vcgencmd version; vcgencmd get_throttled; vcgencmd measure_volts; vcgencmd measure_temp;vcgencmd measure_clock arm;" -i hosts.ini 




