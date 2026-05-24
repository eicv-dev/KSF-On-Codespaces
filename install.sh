#!/bin/sh
cd "$(dirname "$0")"

sudo pip3 install textual --break-system-packages 2>/dev/null || pip3 install textual

python3 installer.py

sudo apt-get update -q
sudo apt-get install -y jq

docker build -t ksf-on-codespaces . --no-cache

mkdir -p Save
cp -r root/config/* Save

json_file="options.json"
if jq ".enablekvm" "$json_file" | grep -q true; then
    docker run -d --name=KSFOnCodespaces -e PUID=1000 -e PGID=1000 --device=/dev/kvm --security-opt seccomp=unconfined -e TZ=Etc/UTC -e SUBFOLDER=/ -e TITLE="KSF On Codespaces" -p 3000:3000 --shm-size="2gb" -v $(pwd)/Save:/config --restart unless-stopped ksf-on-codespaces
else
    docker run -d --name=KSFOnCodespaces -e PUID=1000 -e PGID=1000 --security-opt seccomp=unconfined -e TZ=Etc/UTC -e SUBFOLDER=/ -e TITLE="KSF On Codespaces" -p 3000:3000 --shm-size="2gb" -v $(pwd)/Save:/config --restart unless-stopped ksf-on-codespaces
fi
clear
echo "KSF ON CODESPACES WAS INSTALLED SUCCESSFULLY! Check Port Tab"