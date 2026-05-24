#!/bin/bash
FIRSTBOOT_FLAG="$HOME/.config/.ksf_firstboot_done"
if [ ! -f "$FIRSTBOOT_FLAG" ]; then
    mkdir -p "$HOME/.config"
    touch "$FIRSTBOOT_FLAG"
    sleep 5
    xdg-open "https://killsecurely.com" &
fi
