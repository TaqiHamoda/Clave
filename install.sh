#!/bin/bash

# TODO: Add Nginx support
# TODO: Create log folder /var/log/open-cr
# use `fuser -k 8080/tcp` to kill the process on port 8080 

# Open-CR CONSTANTS
CLAVE_ADDRESS=localhost
CLAVE_PORT=5777
CLAVE_CERT_DIR=/tmp/
CLAVE_INSTALL_DIR=/var/local/Open-CR/
CLAVE_SECRET="$(head -c 48 /dev/urandom | base64)"
CLAVE_MODULE_DIR=${CLAVE_INSTALL_DIR}/backend/modules/

# CouchDB CONSTANTS
COUCHDB_USER=admin
COUCHDB_ADDRESS=localhost
COUCHDB_PORT=5984
COUCHDB_PASS="$(head -c 48 /dev/urandom | base64)" # Create a randomized password for the CouchDB server

COUCHDB_DIR_ARCH=/etc/couchdb/
COUCHDB_DIR_DEB=/opt/couchdb/etc/
COUCHDB_DIR_RASP=/home/couchdb/etc/

# Find out which OS Open-CR is being installed on
OS="$(cat /etc/os-release | grep ^NAME | sed 's/NAME=//g' | sed 's/"//g')"

if [ ! -d "$CLAVE_INSTALL_DIR" ]; then
    mkdir $CLAVE_INSTALL_DIR
fi

# Configure CouchDB
printf "**** Configuring CouchDB ****\n\n"

# Set Local variables
couchdb_dir=""
couchdb_installed=false

# Setup CouchDB configuration
if [ -f "./local.ini" ]; then
    rm ./local.ini
fi

# Configure CouchDB depending on OS
if [ "$OS" == "Arch Linux" ]; then
    # Check if CouchDB is installed
    if [ ! -d $COUCHDB_DIR_ARCH ]; then
        printf "**** Installing CouchDB ****\n\n"
        sudo pacman -Sy couchdb
    fi

    couchdb_dir=$COUCHDB_DIR_ARCH

    couchdb_installed=true
elif [ "$OS" == "Ubuntu" ] || [ "$OS" == "Debian GNU/Linux" ]; then
    if [ ! -d $COUCHDB_DIR_DEB ]; then
        "**** Installing CouchDB ****\n\n"
        curl -L https://couchdb.apache.org/repo/bintray-pubkey.asc | sudo apt-key add -
        echo "deb https://apache.bintray.com/couchdb-deb focal main" | sudo tee -a /etc/apt/sources.list

        sudo apt update && sudo apt install couchdb
    fi

    couchdb_dir=$COUCHDB_DIR_DEB

    couchdb_installed=true
elif [ "$OS" == "Raspbian GNU/Linux" ]; then
    if [ ! -d $COUCHDB_DIR_RASP ]; then
        # Install CouchDB
        sudo ./CouchDB.sh
    fi

    couchdb_dir=$COUCHDB_DIR_RASP
    sudo cp ./configuration/couchdb.service /lib/systemd/system/

    couchdb_installed=true
fi

if [ $couchdb_installed == "true" ]; then
    # Save the backend configuration
    cp ./configuration/backend.env.json ./backend/.env.json

    sed -i "s|\$CLAVE_ADDRESS|$CLAVE_ADDRESS|" ./backend/.env.json
    sed -i "s|\$CLAVE_PORT|$CLAVE_PORT|" ./backend/.env.json
    sed -i "s|\$CLAVE_CERT_DIR|$CLAVE_CERT_DIR|" ./backend/.env.json
    sed -i "s|\$CLAVE_SECRET|$CLAVE_SECRET|" ./backend/.env.json
    sed -i "s|\$MODULE_DIR|$CLAVE_MODULE_DIR|" ./backend/.env.json

    sed -i "s|\$DB_USER|$COUCHDB_USER|" ./backend/.env.json
    sed -i "s|\$DB_PASS|$COUCHDB_PASS|" ./backend/.env.json
    sed -i "s|\$DB_PORT|$COUCHDB_PORT|" ./backend/.env.json
    sed -i "s|\$DB_ADDRESS|$COUCHDB_ADDRESS|" ./backend/.env.json

    # Save the frontend configuration
    cp ./configuration/frontend.env ./frontend/.env

    sed -i "s|\$CLAVE_ADDRESS|$CLAVE_ADDRESS|" ./frontend/.env
    sed -i "s|\$CLAVE_PORT|$CLAVE_PORT|" ./frontend/.env

    printf "${COUCHDB_USER} = ${COUCHDB_PASS}" | sudo tee -a $couchdb_dir/local.ini > /dev/null

    # Create log file directory
    if [ ! -d "/var/log/couchdb/" ]; then
        mkdir /var/log/couchdb/
    fi

    sudo chown couchdb:couchdb /var/log/couchdb

    # Enable CouchDB as a service
    sudo systemctl daemon-reload
    sudo systemctl enable couchdb.service
    sudo systemctl start couchdb.service
else
    printf "Your Operating System is currently Unsupported. Please Install CouchDB Manually"
    printf "Follow the same instructions found in the README regarding pre-installed CouchDB"

    exit  # Exit the installation so user can install CouchDB
fi

# Python Dependencies installation
sudo pip3 install -r ./requirements.txt

# Frontend Dependencies
cd frontend && npm install && cd ..

# TODO: Build the frontend portion and export it instead of the code

# TODO: Generate a server certificate so connections are secured

# # Move website files and folders to installation location
# sudo cp -r ./backend/ $INSTALL_DIR
# sudo cp -r ./frontend/ $INSTALL_DIR

# # Configure Gunicorn
# sudo rm /etc/systemd/system/gunicorn.service
# sudo cp ./configuration/gunicorn.service && sed -i "s|\$INSTALL_DIR|$INSTALL_DIR|" ./gunicorn.service
# sudo mv ./gunicorn.service /etc/systemd/system/

# # Enable and Run Gunicorn
# sudo systemctl enable gunicorn.service
# sudo systemctl start gunicorn.service

# Finished!
printf "\n\n******* Installion Finished!! Please Restart Your System for Open-CR to Run! *******\n\n"
