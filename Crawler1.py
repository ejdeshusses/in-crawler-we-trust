import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_unique_links(url, already_visited):
    """ Get unique links from a given webpage. """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        for link in soup.find_all('a', href=True):
            full_link = urljoin(url, link['href'])
            # Add the link if not already visited
            if full_link not in already_visited:
                links.add(full_link)
        return links
    except requests.RequestException as e:
        print(f"Error occurred while crawling {url}: {e}")
        return set()


def crawl_layers(base_url, depth=2):
    """ Crawl through the website layers. """
    visited = set()  # Tracks visited URLs
    layers = {0: {base_url}}
    visited.add(base_url)  # Mark the base URL as visited

    for i in range(1, depth + 1):
        layers[i] = set()
        print(f"Crawling layer {i}...")
        for url in layers[i - 1]:
            new_links = get_unique_links(url, visited)
            layers[i].update(new_links)
            visited.update(new_links)  # Add newly discovered links to visited
            print(f"Found {len(new_links)} new links in layer {i}.")
            for link in new_links:
                print(link)  # Print each new link found

    return layers


# Example usage
base_url = 'https://www.bysavi.com/'
layers = crawl_layers(base_url)

# Display the total number of links in each layer
for depth, links in layers.items():
    print(f"Layer {depth} has {len(links)} links.")
