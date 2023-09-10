#!/bin/bash

# TODO: Add Nginx support
# TODO: Create log folder /var/log/open-cr
# use `fuser -k 8080/tcp` to kill the process on port 8080 

# Open-CR CONSTANTS
INSTALL_DIR=/var/local/Open-CR/
PORT=5777

# CouchDB CONSTANTS
COUCHDB_PORT=5984
COUCHDB_DIR_ARCH=/etc/couchdb/
COUCHDB_DIR_DEB=/opt/couchdb/etc/
COUCHDB_DIR_RASP=/home/couchdb/etc/


# Find out which OS Open-CR is being installed on
OS="$(cat /etc/os-release | grep ^NAME | sed 's/NAME=//g' | sed 's/"//g')"

if [ ! -d "$INSTALL_DIR" ]; then
    mkdir $INSTALL_DIR
fi

# Configure CouchDB
if [ -f ".env.local" ]; then
    printf "**** CouchDB Installed and .env.local found ****\n\n"
else
    printf "**** Configuring CouchDB ****\n\n"

    installed=false

    # Create a randomized password for the CouchDB server
    PASS="$(head -c 48 /dev/urandom | base64)"

    # Setup CouchDB configuration
    if [ -f "./local.ini" ]; then
        rm ./local.ini
    fi

    # Configure CouchDB
    cp ./configuration/local.ini ./
    sed -i "s|\$PASSWORD|$PASS|" ./local.ini
    sed -i "s|\$PORT|$COUCHDB_PORT|" ./local.ini

    # Actually Configure CouchDB for each OS Listed Below
    if [ "$OS" == "Arch Linux" ]; then
        # Check if CouchDB is installed
        if [ ! -d $COUCHDB_DIR_ARCH ]; then
            printf "Please Install CouchDB and rerun the installation script"
        else
            sudo rm $COUCHDB_DIR_ARCH/local.ini
            sudo mv ./local.ini $COUCHDB_DIR_ARCH
            sudo chown couchdb:couchdb $COUCHDB_DIR_ARCH/local.ini

            installed=true
        fi
    elif [ "$OS" == "Ubuntu" ] || [ "$OS" == "Debian GNU/Linux" ]; then
        if [ ! -d $COUCHDB_DIR_DEB ]; then
            printf "Please Install CouchDB and rerun the installation script"
        else
            sudo rm $COUCHDB_DIR_DEB/local.ini
            sudo mv ./local.ini $COUCHDB_DIR_DEB
            sudo chown couchdb:couchdb $COUCHDB_DIR_DEB/local.ini
        
            installed=true
        fi
    elif [ "$OS" == "Raspbian GNU/Linux" ]; then
        if [ ! -d $COUCHDB_DIR_RASP ]; then
            # Install CouchDB
            sudo ./CouchDB.sh
        fi

        sudo rm $COUCHDB_DIR_RASP/local.ini
        sudo mv ./local.ini $COUCHDB_DIR_RASP
        sudo chown couchdb:couchdb $COUCHDB_DIR_RASP/local.ini
        sudo cp ./configuration/couchdb.service /lib/systemd/system/

        installed=true
    else
        printf "Your Operating System is currently Unsupported. Please Install CouchDB Manually"
        printf "Follow the same instructions found in the README regarding pre-installed CouchDB"

        sleep 5  # Give user time to read
    fi

    if [ $installed == "true" ]; then
        # Save the configuration
        printf "{ \"user\": \"admin\", \"password\": \"${PASS}\", \"port\": 5984 }, \"url\": \"localhost\"" > ./backend/.env.local

        # Create log file directory
        if [ ! -d "/var/log/couchdb/" ]; then
            mkdir /var/log/couchdb/
        fi
        sudo chown couchdb:couchdb /var/log/couchdb

        # Enable CouchDB as a service
        sudo systemctl daemon-reload
        sudo systemctl enable couchdb.service
        sudo systemctl start couchdb.service
    fi
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
printf "\n\n************************ Installion Finished!! Please Restart Your System for Open-CR to Run! ************************\n\n"
