#!/bin/bash

if [ $1 -eq 2 ]
then
POS=”0 0″
else
POS=”1680 0″
fi

/usr/bin/xdotool movewindow `/usr/bin/xdotool getwindowfocus` $POS

exit 0