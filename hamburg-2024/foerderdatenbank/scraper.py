import requests
from bs4 import BeautifulSoup

def get_program_links(url, BASE_URL):
    links = []
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all the funding program divs
        program_divs = soup.find_all('div', class_='card card--horizontal card--fundingprogram')
        
        for div in program_divs:
            link = div.find('a', title='Öffnet die Einzelsicht')
            if link:
                href = link.get('href')
                full_link = BASE_URL + href
                links.append(full_link)
        
        # Find the "weiter" link
        next_link = soup.find('a', class_='forward button', title='SucheSeite')
        if next_link:
            url = BASE_URL + next_link.get('href')
        else:
            url = None
    
    return links

def extract_text_with_newlines(element):
    texts = []

    def recursive_extract_text(elem):
        if isinstance(elem, str):
            texts.append(elem.string.strip())
        if hasattr(elem, 'children'):
            for child in elem.children:
                recursive_extract_text(child)

    recursive_extract_text(element[0])
    return "\n".join(filter(None, texts))

def extract_program_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    program_details = {}

    name_tag = soup.find('h1', class_='title')
    program_details["name"] = name_tag.get_text(strip=True) if name_tag else "No Name Found"

    # fetch the funding program metadata
    metadata = soup.find("dl", class_="grid-modul--two-elements document-info-fundingprogram")
    for header, content in zip(metadata.find_all('dt'), metadata.find_all('dd')):
        program_details[header.get_text(strip=True).replace(':', '')] = content.get_text("\n", strip=True)

    tab_names = [tab_h2.get_text().lower().strip() for tab_h2 in soup.find_all("h2", class_="horizontal--tab-opener")]

    if tab_names:
        articles = soup.find_all("article", class_="content--tab-text")
        for i in range(len(articles)):
            tab_content = []
            for child in articles[i].descendants:
                if child.name in ['p', 'h3']:
                    tab_content.append(child.get_text(strip=True))
            program_details[tab_names[i]] = "\n".join(tab_content)

    else:
        program_details["description"] = extract_text_with_newlines(soup.select('div[class*="container content--main"]'))

    return program_details