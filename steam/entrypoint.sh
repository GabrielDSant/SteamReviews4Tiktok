#!/bin/bash
set -e

# install coisas steam
cd /steam
pip install -r requirements.txt
pip install translators

bash /steam/download-chrome.sh -y

if [ ! -L "/usr/local/bin/chromedriver" ]; then
    ln -s /steam/chrome/chromedriver/chromedriver /usr/local/bin/chromedriver
    chmod +x /usr/local/bin/chromedriver
fi

playwright install

bash /steam/install.sh -y

# Mantém o container ativo
exec tail -f /dev/null
