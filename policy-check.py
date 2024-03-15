#!/usr/bin/env python3

import argparse
from illumio import *
import sys
import os
import json
import argparse
import uuid
import logging
import requests
import json
import socket

def write_to_file(keyfile, content):
    file_name = keyfile 
    with open(file_name, 'w') as outfile:
        outfile.write(content)
    logging.info(f"Content written to {file_name} successfully!")

def parse_arguments():
    parser = argparse.ArgumentParser(description='PCE Demo Host Credentials')
    parser.add_argument('--pce_host', default=os.environ.get('PCE_HOST', 'poc1.illum.io'), help='Integer for the PCE demo host')
    parser.add_argument('--pce_port', default=os.environ.get('PCE_PORT', 443), help='TCP port for the PCE connection')
    parser.add_argument('--org_id', default=os.environ.get('PCE_ORG', 1), help='Organization ID for the PCE')
    parser.add_argument('--api_user', default=os.environ.get('PCE_API_USER'), help='Optional username (default: demo@illumio.com)')
    parser.add_argument('--api_key', default=os.environ.get('PCE_API_KEY'), help='Optional password (default: password)')
    parser.add_argument('--verbose', action='store_true', help='Be more verbose (logging)')
    parser.add_argument('--source', help = 'Source IP address')
    parser.add_argument('--destination', help = 'Source IP address')
    parser.add_argument('--destination-port', help = 'Source IP address', type=int, default=443)
    parser.add_argument('--protocol', default='TCP', help = 'Protocol (TCP, UDP, Default: TCP)')
    return parser.parse_args()


def get_protocol_number(protocol_name):
    try:
        return socket.getprotobyname(protocol_name.lower())
    except OSError:
        return 6

# Parsing the arguments
args = parse_arguments()

# Accessing the values
pce_host = args.pce_host
pce_port = args.pce_port
org_id = args.org_id
username = args.api_user
password = args.api_key
verbose = args.verbose
source = args.source
destination = args.destination
destination_port = args.destination_port
protocol = args.protocol

if not pce_host:
    exit("PCE Host (--pce_host or environemnt variable PCE_HOST) is required")

if not username:
    exit("API User (--api_user or environment variable PCE_API_USER) is required")

if not password:
    exit("API Key (--api_key or environment variable PCE_API_KEY) is required")

if verbose:
    print("Verbose logging enabled")
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


# Printing the values
logging.debug(f"PCE Host: {pce_host}")
logging.debug(f"PCE Port: {pce_port}")
logging.debug(f"Organization ID: {org_id}")
logging.debug(f"Username: {username}")

pce = PolicyComputeEngine(pce_host, port=pce_port, org_id=org_id)
pce.set_credentials(username, password)
if pce.check_connection():
    logging.info("Connected to Illumio PCE API on {}:{}".format(pce_host, pce_port))
else:
    logging.info("Connection failed to: {}:{}".format(pce_host, pce_port))
    exit(1)


# fill label dict, this reads all labels and puts the object into a value of a dict. The dict key is the label name.
label_href_map = {}
value_href_map = {}
for l in pce.labels.get():
    label_href_map[l.href] = { "key": l.key, "value": l.value }
    value_href_map["{}={}".format(l.key, l.value)] = l.href
 

protocol_number = str(get_protocol_number(protocol))
logging.debug(f"Protocol: {protocol} - Protocol Number: {protocol_number}")

payload = {
    "ingress_services": [{"proto": int(protocol_number), "port": int(destination_port)}],
    "providers": [{"ip_address": destination}],
    "consumers": [{"ip_address": source}],
    "resolve_actors": True
}


resp = pce.post('/sec_policy/active/rule_search', json=payload)
resp.raise_for_status()
logging.info(resp.json())

if len(resp.json()) > 0:
    logging.info("Existing rules found")
    for rule in resp.json():
        print(json.dumps(rule, indent=2))
    exit(0)
else:
    logging.info("No rules found")
    exit(1)