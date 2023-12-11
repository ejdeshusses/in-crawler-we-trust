import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import csv

def tokenize(text):
    """ Tokenize the given text into words. """
    tokens = re.findall(r'\b\w+\b', text.lower())
    return set(tokens)

def contains_keyword(tokens, keywords):
    """ Check if any of the keywords are in the tokens. """
    return any(keyword in tokens for keyword in keywords)

def get_partners_links(url, keywords):
    """ Get links related to specified keywords from the given webpage. """
    links = set()
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            link_text = link.get_text().strip().lower()
            tokens = tokenize(link_text)
            full_link = urljoin(url, link['href'])
            if contains_keyword(tokens, keywords):
                links.add(full_link)
    except requests.RequestException as e:
        print(f"Error occurred while fetching {url}: {e}")

    return links

def write_links_to_csv(base_url, links):
    """ Write the base URL and retrieved links to a CSV file with each link. """
    with open('links.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Start with the base URL and then add all retrieved links
        row = [base_url] + list(links)
        writer.writerow(row)


base_url = 'https://www.unitedway.org/'
keywords = [
    'partners', 'associates', 'collaborators', 'colleagues', 'affiliates', 'allies',
    'about', 'pertaining', 'respect', 'relating',
    'aboutus', 'team', 'company', 'partner', 'teammate', 'collaborator', 'associate', 'companion',
    'contributors', 'supporters', 'donors', 'benefactors', 'sponsors', 'backers'
]
partners_links = get_partners_links(base_url, keywords)
write_links_to_csv(base_url, partners_links)

print(f"Links related to {keywords} found on the page:")
for link in partners_links:
    print(link)
