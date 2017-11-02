#!/usr/bin/env bash

###########################################################################
# Installs the python-pip package along with the required python packages #
###########################################################################

readonly SUCCESS_CODE=0

# Show the output of this command to the user
dpkg -l python-pip

# The return code from the dpkg command is: 0 for success, 1 for failure
if [ "$?" -ne ${SUCCESS_CODE} ]; then
    echo "Installation of python-pip package..."
    sleep 1
    sudo apt-get -y --force-yes install software-properties-common
    sudo apt-add-repository universe
    sudo apt-get update
    sudo apt-get -y install python-pip
fi

# Install python-dev package
sudo apt-get -y install python-dev

# Install the required python packages
echo "Installing the required python packages..."
sleep 1
sudo pip install -r requirements.txt

echo "Done!"
