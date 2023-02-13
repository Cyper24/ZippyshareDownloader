import requests
import re
from bs4 import BeautifulSoup
import csv


header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Content-Type": "text/html; charset=utf-8",
    }

ses = requests.Session()    
source = 'list.txt'
with open(source, 'rt') as cp_csv:
    cp_url = csv.reader(cp_csv)
    for row in cp_url:
        url = row[0]
        blink = re.findall(r'\//(.*?)\/', url)
        blin2 = blink[0]
        print(url)
        res = ses.get(url,headers=header)
        soup = BeautifulSoup(res.content,'html.parser')
        data = str(soup.find_all('script'))
        match = re.search(r'document\.getElementById\(\'fimage\'\)\.href\s*=\s*"(.+?)".*?\+\s*\((.*?)%\s*(.*?)\s*\+\s*(.*?)%\s*(.*?)\)\s*\+\s*"(.*?)"', data, re.DOTALL)
        sublink = match.group(1).replace("/i/","/d/") 
        a = int(match.group(2)) 
        b = int(match.group(3))
        c = int(match.group(4)) 
        d = int(match.group(5)) 
        fn = match.group(6)
        ab = a % b + c % d
        tot = str(ab)
        sw = "https://"
        downlink = str(sw + blin2 + sublink + tot + fn)
        filename = downlink.rsplit('/', 1)[1]
        print("++ Downloading.. " + filename)
        file = ses.get(downlink,allow_redirects=True)       
        open(filename, 'wb').write(file.content)
        print("-- Success " + filename)
        print("Next--")
print("Done")