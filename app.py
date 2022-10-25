from asyncio.windows_events import NULL
import os
import sys
import pandas as pd
from pyparsing import null_debug_action
import requests
from bs4 import BeautifulSoup as bs

def ReadTabbedFile():
    # Verifying that an inventory file exists!
    exists1 = os.path.isfile('inventory.txt')
    if not exists1:
        print('Inventory.txt file not found!')
        input("ENTER to exit...")
        sys.exit()
    
    df = pd.read_csv('inventory.txt', delimiter='\t', names=['Text','Model','Device Name','Description','Device Type','Device Protocol','Status','IPv4 Address','Copy','Super Copy'])
    df = df.loc[(df['Status'] != 'Unregistered')]
    ipAddressTable = list(df['IPv4 Address'])

    return ipAddressTable

def webscraper(ipAddress):
    uri = f'http://{ipAddress}/CGI/Java/Serviceability?adapter=device.statistics.device'
    try:
        r = requests.get(uri)
        soup = bs(r.content, 'html.parser')
        soup = bs(str(soup.find('div')), 'html.parser')
        table = soup.find('table')
        ipTable = []
        for row in table.find_all('tr'): 
            # Find all data for each column
            columns = row.find_all('td')
            if(columns != []):
                name_ = columns[0].text.strip()
                value_ = columns[2].text.strip()
                ipTable.append([str(name_),str(value_)])
        df = pd.DataFrame(ipTable, columns=['Name','Value'])
        df = df.loc[df['Name'] == 'Serial number']
        return df['Value'].item()
    except Exception as e:
        return e

if __name__ == '__main__':
    ipAddressTable = ReadTabbedFile()
    for ipAddress in ipAddressTable:
        print(webscraper(ipAddress))
