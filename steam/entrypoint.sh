#!/bin/bash
set -e

# install coisas steam
cd /steam
pip install -r requirements.txt
pip install translators

bash /steam/download-chrome.sh

playwright install

bash /steam/install.sh -y

export TIKTOK_SESSION_ID="f8ce3c9691bbcc3282ded83860f83099"

cd /tiktok_upload
pip install hatch
hatch build
pip install -e .

# Mantém o container ativo
exec tail -f /dev/null
