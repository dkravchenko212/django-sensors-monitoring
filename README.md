# Project for monitoring data from sensors connected to Orange Pi using Python and Django

## Prerequisites
Before installation you must have installed:
- MongoDB
- nginx

As an alternative to installation you can run MongoDB in docker container
```bash
sudo docker run --name mongodb -d -p 27017:27017 mongo:4.4
```

## Installtion
Do the following steps:
- got to deployment folder 
```bash 
cd ./deployment
```
- run `install.sh` (if you also want to intall systemd service run scipt with `sudo`)
```bash
sudo ./install.sh
```
