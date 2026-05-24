# KSF On Codespaces (Modified DesktopOnCodespaces)
### Installation
First start a new blank codespace by going to https://github.com/codespaces/ and choosing the "Blank" template.
Clone this repo into your codespace, then run:
```
python3 installer.py
docker build -t ksf-on-codespaces . --no-cache
sudo ./install.sh
```
