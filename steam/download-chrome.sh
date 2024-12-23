#!/bin/bash

# Baixar o .deb do Google Chrome
wget -O /steam/chrome/google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install /steam/chrome/google-chrome.deb -y
rm /steam/chrome/google-chrome.deb

# Criar diretório para o ChromeDriver
mkdir -p /steam/chrome

# Baixar o ChromeDriver
export CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+\.\d+')
wget -O /steam/chrome/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION/linux64/chromedriver-linux64.zip

# Descompactar o ChromeDriver
unzip /steam/chrome/chromedriver.zip -d /steam/chrome/
rm /steam/chrome/chromedriver.zip

# Tornar o ChromeDriver executável

mv /steam/chrome/chromedriver-linux64 /steam/chrome/chromedriver
chmod +x /steam/chrome/chromedriver/chromedriver

if [ ! -L "/usr/local/bin/chromedriver" ]; then
    ln -s /steam/chrome/chromedriver/chromedriver /usr/local/bin/chromedriver
    chmod +x /usr/local/bin/chromedriver
fi

echo "Download concluído e ChromeDriver configurado."