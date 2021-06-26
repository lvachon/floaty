#!/usr/bin/env bash

DATETIMESTR="$(date +"%Y-%m-%d-%R")"
mkdir $DATETIMESTR
echo $DATETIMESTR
raspistill -tl 1000 -t 0 -o ./$DATETIMESTR/cam%04d.jpg -w 1024 -h 768 -q 10 -l /var/www/html/latest.jpg -gps &
