#!/usr/bin/env bash

sudo apt-get purge runit
sudo apt-get purge git-all
sudo apt-get purge git
sudo apt-get autoremove
sudo apt update
sudo apt install git

if command -v python3 > /dev/null 2>&1; then
	echo "Python3 installed"
else
	echo "Please install Python3"
	exit
fi

echo "\nInstalling Selenium \n"
sudo apt-get install python3-pip -y

python3 -m pip install selenium

echo "\nInstalling Rust \n"
curl -sf -L https://static.rust-lang.org/rustup.sh | sh

echo "\nInstalling Chrome \n"
sudo apt-get install chromium-browser
sudo apt-get install -f
sudo apt-get install xvfb

echo "\nInstalling chromedriver \n"
cd /usr/bin
wget -N http://chromedriver.storage.googleapis.com/2.26/chromedriver_linux64.zip -P ~/Downloads
sudo unzip ~/Downloads/chromedriver_linux64.zip -d ~/Downloads
sudo chmod a+x ~/Downloads/chromedriver
sudo mv -f ~/Downloads/chromedriver /usr/bin/chromedriver

