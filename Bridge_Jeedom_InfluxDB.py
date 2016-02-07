#!/usr/bin/python

""" mainHTTPGetListener.py: Retrieve GET request from Jeedom and forward them to InfluxDB """

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import time
from influxdb import InfluxDBClient
import sys

__author__ = "Jonathan Neuhaus"
__copyright__ = "Copyright 2016"
__license__ = "MIT License"
__version__ = "1.0.0"
__status__ = "Production"

###########################
#    SCRIPT SETTINGS
###########################
# Set the port where you want the bridge service to run
PORT_NUMBER = 1234
# InfluxDB Server parameters
INLUXDB_SERVER_IP = '192.168.x.y'
INLUXDB_SERVER_PORT = 8086
INFLUXDB_USERNAME = 'root'
INFLUXDB_PASSWORD = 'root'
INFLUXDB_DB_NAME = 'db_name'
###########################


# This class will handles any incoming request from jeedom
# Request expected (Jeedom Push URL)
# > http://IP_FROM_SERVER:PORT_NUMBER/updateData?name=#cmd_name#&cmd_id=#cmd_id#&val=#value#&location=salon

class JeedomHandler(BaseHTTPRequestHandler):
    """ Handle Jeedom > InfluxDB Requests """

    # Disable Log messages
    @staticmethod
    def log_message(format, *args):
        return

    # Handler for the GET requests
    def do_GET(self):
        # Part 1: Get the correct GET request from jeedom
        try:
            parsed_url = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed_url.query)
            # Extract the value, the name and the location + add current time
            val = float(query["val"][0])
            name = query["name"][0]
            name = name.encode('latin-1').decode('utf-8')
            location = query["location"][0]
            act_time = time.time() * 1000000000
        except:
            print("URL Parsing error: ", sys.exc_info()[0])
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            return

        # Part 2: Write Data to InfluxDB
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        client = InfluxDBClient(INLUXDB_SERVER_IP, INLUXDB_SERVER_PORT, INFLUXDB_USERNAME, INFLUXDB_PASSWORD, INFLUXDB_DB_NAME)
        
        # Build JSON data
        req = [
            {
                'measurement': name,
                'tags': {
                    'lieu': location
                },
                'time': int(act_time),
                'fields': {
                    'value': val
                }
            }]
        client.write_points(req)
        return


if __name__ == '__main__':
    """ Start Jeedom-InfluxDB bridge """
    try:
        # Start the web server to handle the request
        server = HTTPServer(('', PORT_NUMBER), JeedomHandler)
        print('Started Jeedom-InfluxDB bridge on port ', PORT_NUMBER)

        # Wait forever for incoming http requests
        server.serve_forever()

    except KeyboardInterrupt:
        print('^C received, shutting down the Jeedom-InfluxDB bridge ')
        server.socket.close()
