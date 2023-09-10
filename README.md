# Open CR

An open source and free continuum robot platform that allows anyone (with internet and a raspberry pi) to conduct high-level continuum robot research!

# Installation
Open-CR currently only officially supports linux. However, the project could be migrated to another OS such as Windows or MacOs

## Dependencies

Open-CR has the following dependencies:

* `Python 3.6` or above
* `PIP`
* `Node JS`
* `NPM`
* `CouchDB`
* `OpenSSL`
* `Nginx`

**Note: If you are installing Open-CR unto a Raspberry Pi with Raspbian as the OS, the installation script will automatically install CouchDB for you if it is not installed.**

## Installing Open-CR
Please run the following command to install Open-CR:

```bash
sudo ./install.sh
```

## CouchDB Pre-Installed
If you already have a running version of CouchDB and would like to keep the configuration file unaltered, then please **do the following before you install Open-CR**:

1. Create a `.env.local` file inside the directory.

2. Copy the following text into the file:

```
{
    'user': '$user',
    'password': '$password',
    'port': '$port'
}
```

3. Replace `$user` with the CouchDB user name, `$password` with the CouchDB password, and `$port` with the CouchDB port. Don't forget to save the file.
