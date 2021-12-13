# to calculate hosts between two IP addresses like 10.0.1.30-10.0.1.120
from ipaddress import ip_address

def listHosts(start, end):
    start = ip_address(start)
    end = ip_address(end)
    result = []
    while start <= end:
        result.append(str(start))
        start += 1
    return result

file = open("ips.txt","r")

for line in file:
    fields = line.split("-")
    host1 = fields[0].strip()
    host2 = fields[1].strip()
    calcHosts = (listHosts(host1, host2))
    for i in calcHosts:
        print (i)
