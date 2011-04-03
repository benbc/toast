Dev setup
=========

sudo apt-get install python-setuptools
sudo easy_install pip
sudo pip install virtualenv
sudo pip install virtualenvwrapper

mkdir ~/.virtualenvs
mkvirtualenv toast
workon toast

mkdir log
touch log/command.log

pip install --requirement=requirements.txt
