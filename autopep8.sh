#!/usr/bin/env bash
# Fix python scripts styling with autopep8 guidelines and pycodestyle style guide
VENV='./env/*'

if [ ! "$(command -v autopep8)" ]
then
    echo "Missing package, start installing autopep8..."
    sudo python3 -m pip install pip --upgrade > /dev/null 2>&1 &&\
    sudo python3 -m pip install autopep8 -y > /dev/null 2>&1
fi

echo "Running autopep..."
find . -type f -name '*.py' ! -path '*/migrations/*' ! -path "$VENV" -exec \
    autopep8 --in-place --aggressive --recursive --verbose '{}' \;

if [ ! "$(command -v pycodestyle)" ]
then
	# if python 3.4 upgrade pip
	# curl https://bootstrap.pypa.io/pip/3.4/get-pip.py -o get-pip.py \
    #&& python3 get-pip.py
    echo "Missing package, start installing pycodestyle..."
    sudo python3 -m pip install pip --upgrade > /dev/null 2>&1 &&\
    sudo python3 -m pip install pycodestyle -y > /dev/null 2>&1
fi

echo -e "\n\nRunning pycodestyle..."
find . -type f -name '*.py' ! -path '*/migrations/*' ! -path "$VENV" -exec pycodestyle --verbose '{}' \;

echo -e "\nDone"
exit

