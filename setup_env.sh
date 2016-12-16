#!/usr/bin/env bash

sudo apt-get purge runit -y
sudo apt-get purge git-all -y
sudo apt-get purge git -y
sudo apt-get autoremove -y
sudo apt update -y
sudo apt install git -y

printf "\nInstalling Selenium \n"
sudo apt-get install python3-pip -y

python3 -m pip install selenium

printf "\nInstalling Rust \n"
curl -sf -L https://static.rust-lang.org/rustup.sh | sh

printf "\nInstalling Chromium \n"
sudo apt-get install chromium-browser -y
sudo apt-get install -f -y
sudo apt-get install xvfb -y

printf "\nInstalling chromedriver \n"
cd /usr/bin
wget -N http://chromedriver.storage.googleapis.com/2.26/chromedriver_linux64.zip -P ~/Downloads
sudo unzip ~/Downloads/chromedriver_linux64.zip -d ~/Downloads
sudo chmod a+x ~/Downloads/chromedriver
sudo mv -f ~/Downloads/chromedriver /usr/bin/chromedriver

printf "\nInstalling Torch \n"
git clone https://github.com/torch/distro.git ~/torch --recursive
cd ~/torch; bash install-deps;
./install.sh
source ~/.bashrc
luarocks install lua-cjson
luarocks install nn
luarocks install rnn
luarocks install nngraph
luarocks install dp
luarocks install dpnn
luarocks install graphnn
luarocks install optim
luarocks install unsup
luarocks install qttorch
