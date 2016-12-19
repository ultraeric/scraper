#!/usr/bin/env bash

sudo apt-get purge runit -y
sudo apt-get purge git-all -y
sudo apt-get purge git -y
sudo apt-get autoremove -y
sudo apt update -y
sudo apt install git -y

sudo apt-get install python3-pip -y

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

printf "\nInstalling Requests \n"
python3 -m pip install requests
