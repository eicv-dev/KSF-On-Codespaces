#!/bin/bash
set -e
cd "$(dirname "$0")"

echo "=== Installing dependencies ==="
pip install textual
sleep 2

echo "=== Running installer ==="
python3 installer.py

echo "=== Installing jq ==="
sudo apt update
sudo apt install -y jq

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
