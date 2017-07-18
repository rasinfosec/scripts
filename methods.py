# Script written by @rasinfosec

import requests
import sys

site = sys.argv[1]
username = raw_input("Enter Username:  ")
password = raw_input("Enter Password:  ")

req = requests.request('OPTIONS', site, auth=(username, password))
data = req.headers

#print data.items()

for x in data.items():
    print x

