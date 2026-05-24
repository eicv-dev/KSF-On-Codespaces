#!/bin/bash

if [ ! -f $HOME/.config/kwinrc ]; then
  kwriteconfig5 --file $HOME/.config/kwinrc --group Compositing --key Enabled false
fi
if [ ! -f $HOME/.config/kscreenlockerrc ]; then
  kwriteconfig5 --file $HOME/.config/kscreenlockerrc --group Daemon --key Autolock false
fi
setterm blank 0
setterm powerdown 0
chmod +x /firstboot.sh && /firstboot.sh &
/usr/bin/dbus-launch /usr/bin/startplasma-x11 > /dev/null 2>&1
