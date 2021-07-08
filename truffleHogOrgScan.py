import requests
import json
import argparse, os
import re

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--org", dest = "org", help="Supply a valid org name, as found in https://api.github.com/orgs/ORG/repos?type=all.  We only need the org name")
args = parser.parse_args()
comp = args.org
url = "https://api.github.com/orgs/{}/repos?type=all".format(comp)
print ("The URL being used is {}".format(url))

r = requests.get(url)
data = r.json()

for repo in data:
    gitLoc = (repo["html_url"])
    saveFile = re.sub('[^A-Za-z0-9]+', '', gitLoc.strip('https://github.com/' + comp + '/'))
    print ("Scanning {}.git and saving json file to {}.json".format(gitLoc, saveFile))
    cmd = "trufflehog --regex --entropy=True --json {}.git >> {}.json".format(gitLoc, saveFile)
    os.system(cmd)
