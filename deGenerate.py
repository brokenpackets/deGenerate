#!/usr/bin/env python
import requests
import json
###### User Variables

username = 'admin'
password = 'Arista123'
server1 = 'https://192.168.255.50'

######
connect_timeout = 10
headers = {"Accept": "application/json",
           "Content-Type": "application/json"}
requests.packages.urllib3.disable_warnings()
session = requests.Session()

def login(url_prefix, username, password):
    authdata = {"userId": username, "password": password}
    headers.pop('APP_SESSION_ID', None)
    response = session.post(url_prefix+'/web/login/authenticate.do', data=json.dumps(authdata),
                            headers=headers, timeout=connect_timeout,
                            verify=False)
    cookies = response.cookies
    headers['APP_SESSION_ID'] = response.json()['sessionId']
    if response.json()['sessionId']:
        return response.json()['sessionId']

def logout(url_prefix):
    response = session.post(url_prefix+'/web/login/logout.do')
    return response.json()

def save_topology(url_prefix):
    response = session.post(url_prefix+'/cvpservice/provisioning/v2/saveTopology.do', data=json.dumps([]))
    return response.json()

def get_configlets(url_prefix):
    response = session.get(url_prefix+'/cvpservice/configlet/getConfiglets.do?type=Generated&startIndex=0&endIndex=0')
    return response.json()

def delete_configlet(url_prefix,configlet_key,configlet_name):
    tempData = [{"key": configlet_key, "name": configlet_name}]
    response = session.post(url_prefix+'/cvpservice/configlet/deleteConfiglet.do', data=json.dumps(tempData))
    return response.json()

#### Login ####
print '###### Logging into Server 1'
login(server1, username, password)
output = get_configlets(server1)
for item in output['data']:
    if item['type'] == 'Generated' and item['netElementCount'] == 0:
        configlet_name = item['name']
        configlet_key = item['key']
        print item
        configlet_to_delete = delete_configlet(server1,configlet_key,configlet_name)
        print configlet_to_delete
logout(server1)
