import requests
from bs4 import BeautifulSoup

# install nltk module
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

# Import URLs from previous crawler and tokenize the text from the page to match with 
urls = ['https://www.unitedway.org/our-partners/']

# Send a GET request to the URL
for url in urls:

    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get all the text from the page
        all_text = soup.get_text()
        
        # Tokenize the text
        tokens = word_tokenize(all_text)
        with open('IR/Proj/text.txt', 'w', encoding='utf-8') as file:
            file.write(all_text)

        # Print the tokens
        print(tokens)
        
        # Need to use these tokens to search through and find partners

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")