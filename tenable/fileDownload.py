#!/usr/bin/env python3

from tenable.sc import TenableSC
from tenable.io import TenableIO
import requests
from urllib.parse import urlparse
try:
    import settings
except ImportError:
    raise ImportError('You must use the settings.py script')
from zipfile import ZipFile
import json, os, logging, time, sys, shutil

node = sys.argv[1]
tio = TenableIO(settings.access_code, settings.api_secret)

def tenable_sc():
    sc = TenableSC(node)
    sc.login(settings.username, settings.password)
    getscandata = sc.get('scanResult?fields=name,startTime,finishTime')
    scandata = json.loads(getscandata.text)

    for scan in scandata['response']['usable']:
        # check to see if the finish time is greater than or equal to the epoch time from ## hours ago
        scan_finishtime = scan['finishTime']
        scan_name = scan['name']
        scan_id = scan['id']
        """
        This will set a unique value for the scan to determine if the report has already
        been pulled down.  If it has been pulled dont download again.  
        """
        file_id_value = scan_name + scan_id + scan_finishtime
        if int(scan_finishtime) >= int(settings.epoch_time):
            #load = sc.post('scanResult/' + scan['id'] + '/download', stream=True)
            zip_file = 'nessus_' + scan_name + settings.current_time.strftime('%Y%m%d%H%M%S') + '.zip'
            file_name = 'nessus_' + scan_name + settings.current_time.strftime('%Y%m%d%H%M%S') + '.nessus'
            #with open(os.path.join(settings.file_in + '/download/tmp/', zip_file), 'w') as zip:
                #zip.write(load.content)
            with open(os.path.join(settings.file_in + '/download/tmp', zip_file), 'wb') as reportobj:
                sc.scan_instances.export_scan(scan_id, reportobj)
            for zip_file in os.listdir(settings.file_in + '/download/tmp/'):
                if zip_file.endswith('.zip'):
                    zip_ref = ZipFile(settings.file_in + '/download/tmp/' + zip_file, 'r')
                    zip_ref.extractall(path = settings.file_in + '/download/tmp/')
                    zip_ref.close()
                    #os.remove(settings.file_in + '/download/tmp/' + zip_file)
                    time.sleep(1)
            for nessus_file in os.listdir(settings.file_in + '/download/tmp/'):
                if nessus_file.endswith('.nessus'):
                    shutil.move(settings.file_in + '/download/tmp/' + nessus_file, settings.file_in + '/download/' + file_name)

def tenable_io():
    scanurl = settings.baseurl + '/scans'
    r = requests.get(scanurl, headers={'X-ApiKeys': 'accessKey=%s; secretKey=%s;' %(settings.access_code,settings.api_secret)})
    scandata = json.loads(r.text)
    for scan in scandata['scans']:
        scan_id = scan['id']
        scan_name = scan['name']
        uuid = scan['uuid']
        """
        This will set a unique value for the scan to determine if the report has already
        been pulled down.  If it has been pulled dont download again.  
        """
        io_file_value = str(scan_id) + str(uuid)
        historyurl = settings.baseurl + '/scans/{}/history/{}'.format(scan_id,uuid)
        r = requests.get(historyurl, headers={'X-ApiKeys': 'accessKey=%s; secretKey=%s;' %(settings.access_code,settings.api_secret)})
        history_data = json.loads(r.text)
        scan_finishtime = history_data['scan_end']
        if int(scan_finishtime) >= int(settings.epoch_time):
            # There is no option to download as a zip file - https://developer.tenable.com/reference#scans-export-request
            file_name = 'nessus' + '-' + history_data['name'] + '_' + settings.current_time.strftime('%Y%m%d%H%M%S') + '.nessus'
            with open(os.path.join(settings.file_in + '/download', file_name), 'wb') as reportobj:
                tio.scans.export(scan_id, fobj=reportobj)

def main():
    if 'io' not in node:
        tenable_sc()
    else:
        tenable_io()

if __name__ == '__main__':
    main()
