#!/usr/bin/python
import subprocess
import os
from neutronclient.v2_0 import client
class Configinfo:
    #class for openstack configuration information
    _network_info = {}
    _port_info = {}
    _d = {}
    def __init__(self):
        #sets credentials requires to get the token in d
        with open('/home/stack/auth.ini') as f:
            content = f.readlines()
        self._d['username'] = content[0].rstrip()
        self._d['password'] = content[1].rstrip()
        self._d['auth_url'] = content[3].rstrip()
        self._d['tenant_name'] = content[2].rstrip()


    def get_credentials(self):
        ##returns a dictonary containing credentials
        return self._d

    def __set_network_info(self, network):
        #store available neutron networks
        self._network_info = network['networks']


    def __set_port_info(self, port):
        #store available neutron ports
        self._port_info = port['ports']

    def print_port_values(self, port, network):
        #List all the networks and associated neutron ports in each network.
        # and tap interfaces (if any)
        self.__set_network_info(network)
        self.__set_port_info(port)
        for p in self._network_info:
            print(("network-id: %s\n" % p['id']))
            for q in self._port_info:
                if q['network_id'] == p['id']:
                    print(("\tPort ID: %s   %s" % (q['id'], q['device_owner'])))
                    tap = q['id'].split("-")[0]
                    #print tap
                    strr = os.popen("\
                        sudo ip a | grep tap" + tap + " | awk '{ print $2 }'\
                        && ovs-dpctl show | grep tap" + tap + " | awk '{print\
                        $3}'").read()
                    print(("\t\t\ttap interface: %s" % strr))
                    print(("\
                    \tSubnet ID: %s" % (q['fixed_ips'][0]['subnet_id'])))
                    print(("\
                    \tip address: %s" % (q['fixed_ips'][0]['ip_address'])))
                    print("\n")

obj1 = Configinfo()
credentials = obj1.get_credentials()
neutron = client.Client(**credentials)
#adding new line to file for test only
netw = neutron.list_ports()
nete = neutron.list_networks()
obj1.print_port_values(netw, nete)
