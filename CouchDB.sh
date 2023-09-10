# Script to install and configure CouchDB 3.1.1 on Raspbian

# Installing CouchDB Dependencies
wget http://packages.erlang-solutions.com/debian/erlang_solutions.asc
sudo apt-key add erlang_solutions.asc

sudo apt-get update
sudo apt-get --no-install-recommends -y install build-essential pkg-config erlang libicu-dev libmozjs185-dev libcurl4-openssl-dev

# Create a CouchDB User
sudo useradd -d /home/couchdb couchdb
sudo mkdir /home/couchdb
sudo chown couchdb:couchdb /home/couchdb

# Download CouchDB source
wget https://downloads.apache.org/couchdb/source/3.1.1/apache-couchdb-3.1.1.tar.gz
tar -xvf apache-couchdb-3.1.1.tar.gz

# Build CouchDB source
cd ./apache-couchdb-3.1.1/ && ./configure && make release

cd ./rel/couchdb/
sudo cp -Rp * /home/couchdb
sudo chown -R couchdb:couchdb /home/couchdb

# Remove downloaded files
cd ../../../
rm -rf apache-couchdb-3.1.1/
rm apache-couchdb-3.1.1.tar.gz
rm erlang_solutions.asc
