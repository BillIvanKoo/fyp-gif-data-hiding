# Data Hiding in GIF 

#### Bill Ivan Kooslarto - 28694120

#### Choong Jia Qin - 28858964

#### Yeoh Joe Den - 28851692

This is a Final Year Project for FIT3162 Monash University Malaysia

We created a website to hide data in GIF by using least significant byte (LSB) method. This website consists of two instances, a server and a client application.

### Main Dependencies
 - Python3.6+
 - Flask
 - NodeJS and npm

### Running the Server Locally
```bash
$ export FLASK_APP=server.py
$ flask run
```
the server will run on localhost:5000


### Running the Client Locally
```bash
$ cd client

# install app dependencies first, just need to run once
$ npm install

$ npm start
```
the client will run on localhost:3000

### Server API Endpoints
| HTTP Method | Route | Description |
| --- | --- | --- |
| POST | /gif/calculate | to calculate the hiding capacity of a gif
| POST | /gif/encode | to hide data in a gif
| POST | /gif/decode | to retrieve the hidden data in a gif