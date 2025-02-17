import requests
from bs4 import BeautifulSoup
import json


def searchIsotope(name):

    url = f"https://www.nndc.bnl.gov/nudat3/decaysearchdirect.jsp?nuc={name}&unc=NDS"

    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')

    parsed_data = parse_decay_data(soup)

    print(json.dumps(parsed_data, indent=4))


def parse_decay_data(soup):
    tables = soup.find_all('table', {'border': '0', 'cellspacing': '1', 'cellpadding': '2', 'bgcolor': 'navy'})
    data = []
    for table in tables:
        rows = table.find_all('tr')[1]  # Skip header
        columns = rows.find_all('td')
        
        data.append({
            'Nucleus': columns[2].get_text(strip=True),
            # 'E(level)': columns[3].get_text(strip=True),
            # 'Jπ': columns[4].get_text(strip=True),
            'T1/2': columns[5].get_text(strip=True),
            'Decay Mode': columns[6].get_text(strip=True),
            # 'GS-GS Q-value (keV)': columns[7].get_text(strip=True),
            # 'Daughter Nucleus': columns[8].get_text(strip=True)
        })
    
    return data 



searchIsotope("Co60")