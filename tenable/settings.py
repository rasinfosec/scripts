#!/usr/bin/env python3

import datetime
import logging
import os
    
## Specify in hours the scan history you want to look for
scan_history = 30

# This is the Tenable SC API user and consoles
username = ''
password = ''

# This is the Tenable.io API access and secret
access_code = ''
api_secret = ''
baseurl = 'https://cloud.tenable.com:443'

# Set the paths.  We run as service so setting the full path seems work better.  Otherwise the os.path works.  
dir_path = '/api'
file_in = dir_path + '/in/'
file_out = dir_path + '/out/'

logfile = '/api/nessus.log'
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename=logfile)

# Grab the time
current_time = datetime.datetime.now()

# Take the current time and subtract the hours defined.
timecalc = current_time - datetime.timedelta(hours = scan_history)
epoch_time = timecalc.strftime("%s")
