# Clave

Clave (pronounced `klah-vey`, after the instrument) is an open source robot management system that provides the tools needed to remotely conduct experiments and collect data in an effecient manner.

# Installation
Clave currently only officially supports linux. However, the project could be migrated to another OS such as Windows or MacOs

## Dependencies

Clave has the following dependencies:

* `Python 3.6` or above
* `PIP`
* `Node JS`
* `NPM`
* `CouchDB`
* `OpenSSL`
* `Nginx`

**Note: If you are installing Clave unto a Raspberry Pi with Raspbian as the OS, the installation script will automatically install CouchDB for you if it is not installed.**

## Installing Clave
Please run the following command to install Clave:

```bash
sudo ./install.sh
```

## CouchDB Pre-Installed
If you already have a running version of CouchDB and would like to keep the configuration file unaltered, then please **do the following before you install Clave**:

1. Set the `INSTALL_COUCHDB` variable in the `install.sh` file to `false`.

2. Set the `COUCHDB_ADDRESS`, `COUCHDB_PORT`, `COUCHDB_USER` and `COUCHDB_PASS` variables inside `install.sh` to their appropriate values.

3. Save your changes and run the installation file.