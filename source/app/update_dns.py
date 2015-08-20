import BaseHTTPServer, cgi
import json
import socket
import dns.name
import os
import iscpy

class httpServHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """
        Class to handle HTTP request
    """

    def do_PUT(self):
        """
            Update bind entry
        """
        
        length = int(self.headers['Content-length'])
        content = self.rfile.read(length)
        data = json.loads(content)
        check = check_input(data)
        if check is not True:
            print "KO"
            self.send_response(400)
        else:
            dns_name = dns.name.from_text(data['fqdn'])
            
            # Get dns zone
            parent = dns_name.parent()
            seq = parent[:-1]
            str = "."
            parent = str.join(seq)

            # Get zone config
            zone_config = get_dns_config()
            
            # Get zone file  to update
            if zone_config.has_key(parent):
                print "file to edit: %s" % zone_config[parent]['file']

            # Once update is done send HTTP response
            self.send_response(200)

    def do_DELETE(self):
        """
            Delete bind entry
        """

        length = int(self.headers['Content-length'])
        content = self.rfile.read(length)
        data = json.loads(content)
        check = check_input(data)
        if check is not True:
            print "KO"
            self.send_response(400)
        else:
            print "OK"
            self.send_response(200)

def check_input(data):
    """
        Check the content of the request
    """
    if data.has_key('fqdn') and data.has_key('ip'):

            try:
                socket.inet_aton(data['ip'])
                return True
            except socket.error:
                return False


# Function to get dns config
def get_dns_config():
    """
        Function to get zone config, handle zone and associate file
    """

    # Config 
    # TODO : to put in a external config file
    zones_config_file = '/etc/named/zones.conf'

    # load bind zone config file
    zones_config = iscpy.ParseISCString(open(zones_config_file, 'r').read())

    # Build zone tab to store zone name / config file
    zone_dict = dict()

    for z in zones_config:
        zone = z.split(' ')
        # check if the dns is master for this zone
        if zones_config[z]['type'] == 'master':
            zone_name = zone[1].replace("\"", "")
            zone_file = zones_config[z]['file'].replace("\"", "")
            zone_dict.update({zone_name : {'name': zone_name, 'file': zone_file}})

    return zone_dict

servAddr = ('', 9090)
serv = BaseHTTPServer.HTTPServer(servAddr, httpServHandler)
serv.serve_forever()