#!/bin/bash

# Baixar o .deb do Google Chrome
wget -O google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Criar diretório para o ChromeDriver
mkdir -p ./chrome

# Baixar o ChromeDriver
CHROME_VERSION=$(wget -qO- https://dl.google.com/linux/chrome/deb/dists/stable/main/binary-amd64/Packages | grep 'Version: ' | head -1 | awk '{print $2}')
CHROMEDRIVER_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION)
wget -O ./chrome/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip

# Descompactar o ChromeDriver
unzip ./chrome/chromedriver.zip -d ./chrome/
rm ./chrome/chromedriver.zip

# Tornar o ChromeDriver executável
chmod +x ./chrome/chromedriver

echo "Download concluído e ChromeDriver configurado."