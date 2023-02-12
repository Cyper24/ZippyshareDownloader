import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv


header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Content-Type": "text/html; charset=utf-8",
    }
    
# Convert txt to csv
df = pd.read_fwf('list.txt')
df.to_csv('link.csv',index=False)

source = 'link.csv'
with open(source, 'rt', encoding='utf-8-sig') as cp_csv:
    cp_url = csv.reader(cp_csv)
    for row in cp_url:
        url = row[0]
        blink = re.findall(r'\//(.*?)\/', url)
        blin2 = blink[0]
        res = requests.get(url,headers=header)
        soup = BeautifulSoup(res.content,'html.parser')
        script = soup.find_all('script')[9]
        sc = script.get_text()
        try:
            x = re.findall(r'\((.*?)\)', sc)[1].split()
        except Exception as str_error:
            pass
            if str_error:
                print("Error. Retry...")
                time.sleep(1)
                res = requests.get(url,headers=header)
                soup = BeautifulSoup(res.content,'html.parser')
                script = soup.find_all('script')[9]
                sc = script.get_text()
                x = re.findall(r'\((.*?)\)', sc)[1].split()
        a = int(x[0])
        b = int(x[2])
        c = int(x[4])
        d = int(x[6])
        ab = a % b + c % d
        tot = str(ab)
        xx = re.findall(r'\"(.*?)\"', sc)
        l2 = xx[0]
        fn = xx[1]
        sw = "https://"
        downlink = str(sw + blin2 + l2 + tot + fn)
        filename = downlink.rsplit('/', 1)[1]
        print("++ Downloading.. " + filename)
        file = requests.get(downlink,allow_redirects=True)       
        open(filename, 'wb').write(file.content)
        print("-- Success " + filename)

    