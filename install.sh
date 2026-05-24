#!/bin/sh
cd "$(dirname "$0")"

echo "=== Installing dependencies ==="
sudo pip3 install textual pillow --break-system-packages 2>/dev/null || pip3 install textual pillow

echo "=== Running installer ==="
python3 -c "
import os, sys
try:
    from PIL import Image
    img = Image.open('assets/banner.png').convert('RGB')
    w, h = img.size
    new_w = 80
    new_h = int(h * new_w / w * 0.45)
    img = img.resize((new_w, new_h))
    for y in range(new_h):
        row = ''
        for x in range(new_w):
            r, g, b = img.getpixel((x, y))
            row += f'\033[38;2;{r};{g};{b}m\u2588'
        print(row + '\033[0m')
except Exception:
    pass
"
python3 installer.py

echo "=== Installing jq ==="
sudo apt-get update -q
sudo apt-get install -y jq

echo "=== Building Docker image ==="
docker build -t ksf-on-codespaces . --no-cache

echo "=== Setting up config ==="
mkdir -p Save
cp -r root/config/* Save

echo "=== Starting container ==="
json_file="options.json"
if jq ".enablekvm" "$json_file" | grep -q true; then
    docker run -d --name=KSFOnCodespaces -e PUID=1000 -e PGID=1000 --device=/dev/kvm --security-opt seccomp=unconfined -e TZ=Etc/UTC -e SUBFOLDER=/ -e TITLE="KSF On Codespaces" -p 3000:3000 --shm-size="2gb" -v $(pwd)/Save:/config --restart unless-stopped ksf-on-codespaces
else
    docker run -d --name=KSFOnCodespaces -e PUID=1000 -e PGID=1000 --security-opt seccomp=unconfined -e TZ=Etc/UTC -e SUBFOLDER=/ -e TITLE="KSF On Codespaces" -p 3000:3000 --shm-size="2gb" -v $(pwd)/Save:/config --restart unless-stopped ksf-on-codespaces
fi
clear
echo "KSF ON CODESPACES WAS INSTALLED SUCCESSFULLY! Check Port Tab"
