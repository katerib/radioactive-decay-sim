import requests
from bs4 import BeautifulSoup
import json

def parse_decay_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    datasets = []
    isotope_data = []
    
    # find all text
    text_content = soup.body.get_text() if soup.body else ''
    dataset_sections = text_content.split('Dataset #')[1:]

    # Get the isotope data
    tables = soup.find_all('table', {'border': '0', 'cellspacing': '1', 'cellpadding': '2', 'bgcolor': 'navy'})
    for table in tables:
        rows = table.find_all('tr')[1]  # Skip header
        columns = rows.find_all('td')
        
        isotope_data.append({
            'half-life': columns[5].get_text(strip=True),
            'Decay Mode': columns[6].get_text(strip=True),
        })   
    
    for i, section in enumerate(dataset_sections, 1):
        # gamma section
        gamma_data = []
        gamma_start = section.find('Gamma and X-ray radiation:')
        if gamma_start != -1:
            gamma_lines = section[gamma_start:].split('\n')
            header_found = False
            
            for line in gamma_lines:
                line = line.strip()
                if not line or 'Coincidence' in line:
                    continue

                if not header_found:
                    if 'Energy' in line and 'Intensity' in line and 'Dose' in line:
                        header_found = True
                    continue
                
                parts = [p.strip() for p in line.split() if p.strip()]
                if len(parts) >= 3:
                    try:
                        # if line starts with XR, the first two parts are the type
                        if line.startswith('XR'):
                            rad_type = f'{parts[0]} {parts[1]}'
                            energy = float(parts[2])
                            intensity = float(parts[3].rstrip('%'))
                            dose = float(parts[-1])
                        else:
                            rad_type = 'gamma'
                            energy = float(parts[0])
                            intensity = float(parts[1].rstrip('%'))
                            dose = float(parts[-1])
                            
                        gamma_data.append({
                            'type': rad_type,
                            'energy': energy,
                            'intensity': intensity,
                            'dose': dose
                        })
                    except ValueError:
                        continue
        
        if gamma_data:
            datasets.append({
                'dataset': i,
                'gamma_emissions': gamma_data,
                'isotope_data': isotope_data 
            })
    
    return datasets


def SearchIsotope(name):
    url = f'https://www.nndc.bnl.gov/nudat3/decaysearchdirect.jsp?nuc={name}&unc=NDS'
    response = requests.get(url)
    if response.status_code == 200:
        return parse_decay_data(response.text)
    else:
        print(f'Error: Got status code {response.status_code}')
        return []


# if __name__ == '__main__':
#     print('Getting Co60 data from NNDC website:')
#     web_data = SearchIsotope('Co60')
#     for dataset in web_data:
#         print(f'\nDataset {dataset['dataset']}')
#         for emission in dataset['gamma_emissions']:
#             print(f'Type: {emission['type']}')
#             print(f' > Energy: {emission['energy']:.3f} keV')
#             print(f' > Intensity: {emission['intensity']:.3f}%')
#             print(f' > Dose: {emission['dose']:.6f} MeV/Bq-s')
#             print('-' * 40)

#     # only print gamma
#     for dataset in web_data:
#         print(f'\nDataset {dataset['dataset']}')
#         gamma_only = [e for e in dataset['gamma_emissions'] if e['type'] == 'gamma']
#         for emission in gamma_only:
#             print(f'Energy: {emission['energy']:.3f} keV')
#             print(f'Intensity: {emission['intensity']:.3f}%')
#             print(f'Dose: {emission['dose']:.6f} MeV/Bq-s')
#             print('-' * 40)