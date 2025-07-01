import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def parse(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        textarea = soup.find('textarea', {'class': 'content'})
        
        if not textarea:
            return None, None
            
        md_content = textarea.text.strip()
        license_key = None
        
        if md_content:
            first_line = md_content.split('\n')[0]
            if '-' in first_line:
                license_key = first_line.split('-')[0]
                
        return license_key, md_content
        
    except requests.exceptions.RequestException:
        return None, None

def generate_dates(start_date=None, days_back=30):
    if start_date is None:
        start_date = datetime.now()
    
    for i in range(days_back):
        current_date = start_date - timedelta(days=i)
        yield current_date.strftime("%Y-%m-%d")

def find_valid_key(base_url, year="2025", max_days_back=365):
    for date_str in generate_dates(datetime.now(), max_days_back):
        url = f"{base_url}/licenses/{year}/{year}-{date_str.split('-')[1]}-{date_str.split('-')[2]}.md"

        key, content = parse(url)
        
        if content:
            return key, content, url

    
    return None, None, None

if __name__ == "__main__":
    base_url = "https://gitee.com/superbeyone/J2_B5_A5_C4/blob/master"
    
    key, content, found_url = find_valid_key(base_url)
    
    if content:
        print(content)
    else:
        print("Key not found")
