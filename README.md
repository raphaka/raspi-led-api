# raspi-led-api

A REST-API to control your SMD5050 light strips on your Raspberry Pi.
It features different modes:
* Static Color Mode: Setting a color directly from its hexadezimal RGB value
* Stream Mode: Set hexadecimal color information from a UDP port for better performance in ambilight effects

## Setting up the light strips
A tutorial on how to install the light strips on your Raspberry pi can be found here:  
https://dordnung.de/raspberrypi-ledstrip/  
It is available in German and English.

## Installing and running the application
Install the flask application:  
`git clone https://github.com/raphaka/raspi-led-api.git`  
`cd raspi-led-api`  
`pip install --user -r requirements.txt`  

Enable pigpio:  
`sudo apt-get install pigpiod`  
`sudo systemctl enable --now pigpiod`

Run the application:  
`python3 run.py`

## Basics
Adjust the `SERVER_NAME` variable in _led_api/flask_config.cfg_ to set up the \<host\> and \<port\>.


**Setting the light strips to a specific color:**  
`GET http://<host>:<port>/set/colorhex/<color>`  
\<color\> is the hexadecimal representation of a 24bit RGB value (e.g. 00ff00 for green)


**Enable stream mode:**  
`GET http://<host>:<port>/set/stream`  
The port can be configured in the settings.


**Adjusting the settings:**  
`PUT http://<host>:<port>/set/stream`  
The request data should be a JSON object containing one or more key/value pairs.
Unrecognised keys will automatically be ignored.  
Example:  
`{"brightness_maximum": 200, "contrast_adjustment":1.5}`
