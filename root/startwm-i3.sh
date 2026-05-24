#!/bin/bash

setterm blank 0
setterm powerdown 0
chmod +x /firstboot.sh && /firstboot.sh &
/usr/bin/i3 > /dev/null 2>&1