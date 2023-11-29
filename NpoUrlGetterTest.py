from selenium import webdriver 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
import pandas as pd
# import selenium.webdriver.common.*

# element = driver.find_element(*self.locator)


# search_text = 'United Ways'
search_text = 'United Way Central Mass'
search_arr = ['United Way', 'United way mass', 'cws', 'java', 'wpi goat cheese', 'wpi']

GOOGLE = "https://www.google.com/"


class AutomateChromeURLSearch(object):

    def __init__(self):
        ## Chrome driver
        self.driver = None
        ## search bar element
        self.searchBar_element = None


    ''' Initialize chromedriver and open Google Home'''
    def start_driver(self):
        ## Run headless. Should automatically get chromedriver for the corresponding version of Chrome on local machine
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu') 

        self.driver = webdriver.Chrome(options=options)

        self.driver.get(GOOGLE)
        ## locate the element, or relocate in case of stale element
        self.searchBar_element = self.locate_search_bar()

        return True
    
    # def start_wait(self): 
    #     wait = WebDriverWait(self.driver)
    #     element = wait.until(EC.element_to_be_clickable((By.ID, 'someid')))

    ''' Locate Google search bar element for each page (refreshed)'''
    def locate_search_bar(self): 
        self.searchBar_element = self.driver.find_element(By.XPATH, "//textarea[@jsname='yZiJbe']")

        return True

    ''' Search text in Google search bar '''
    def search_text(self, text):
        ## if search bar is not initialized, ERROR
        if self.searchBar_element == None: 
            return False 
        
        ## relocate search bar for new page (otherwise stale element)
        self.locate_search_bar()
        ## clear search bar before new search
        self.searchBar_element.clear()

        ## search text 
        self.searchBar_element.send_keys(text)
        self.searchBar_element.submit()

        time.sleep(0.01)
        return True



    ''' Helper functions: 
        * get_base_url(url) : processing url, returns standardized base url 
        ## change to get clean url 
        ** add get base url method that gets all text left of the first single '/', or the overall third '/'?
        
        '''
    def get_clean_url(self, url): 

        base = re.match(r'^(.*/)[^/]+$', url)
        if base:
            return base.group(1)
        
        return url


    def get_base_url(self, url): 

        # pattern = r'(?<!/)/(?!/)(.)'
        pattern = r'(?<!/)/(?=[^/])'

        base = re.split(pattern, url)

        print(f"get base url found ::{base}")
        # if base:
        #     return base[0]
        
        return base[0]


    ''' Get top 10 urls from the google search, parse and process urls '''
    def get_search_result_urls(self):

        # print(f"> Seetkng url for: {self.driver.title} ...")
        results = self.driver.find_element(By.XPATH, "//div[@id='search']/div/div" )
        # print("++++++++++++++++++++++++++++++++")

        npo_urls = []
        max_urls = 4

        all_span = results.find_elements(By.TAG_NAME, 'a')

        for aa in all_span:
            if max_urls == 0: 
                break
            parent = aa.find_element(By.XPATH, "./..")

            if parent.get_attribute('jscontroller') == 'msmzHf':
                npo_urls.append(aa.get_attribute('href'))
                max_urls -= 1
        

        ''' !!!! Need to fix url parsing logic !!!!
            Add: url validation 
            Current errors: could be a news site, database, or other. 
            
            Validation: 
            option 1) url text matching --> if url has full string tokens of NPO (minus stop words?) 
                ** or check if npo 'SORT_NAME' matches the url text
            option 2) go to site and check for indicators in title, header/footer, etc. that match the NPO
                -- check site by beutiful soup or by chromedriver? 
                ** or check if npo 'SORT_NAME' matches the title, headers, etc.
            option 3) -maybe unnecessary- check if majority of top 3 results have the same base and are not social media  

        '''
        
        ## temporary social media avoiding 
        while max_urls <= len(npo_urls):
            return_url = self.get_base_url(npo_urls[max_urls])
            if return_url == 'https://www.facebook.com':
                max_urls += 1
                continue 
            if return_url == 'https://www.twitter.com':
                max_urls += 1
                continue 
            if return_url == 'https://www.wikipedia.com':
                max_urls += 1
                continue 
            if return_url == 'https://www.linkedin.com':
                max_urls += 1
                continue 
            else: 
                return return_url

        
        return False


    def iterate_for_list(self, search_list):
        url_list = []

        ## for all NPO names (in column of df)
        for search in search_list:
            print(f"> Iterating is searching for {search}")
            
            self.search_text(search)
            
            url_list.append(self.get_search_result_urls())

            try: 
                self.locate_search_bar()
            except Exception as e: 
                print(f"Element was stale. {e} .")
                self.start_driver()

        return url_list

def load_data(file_path):

    ## Read the .csv file into a pandas DataFrame
    NPO_df = pd.read_csv(file_path)

    ## Display the DataFrame
    print(NPO_df.head())
    return NPO_df





def main(args):
    print("Starting MAIN ")

    ## Specify the path to the csv file
    NPO_whitelist_path = "NPO_whitelist_2names.csv"

    npo_df = load_data(NPO_whitelist_path)

    npo_list = npo_df['NAME'].to_list()
    print(f" ___ got npo list {npo_list}" )
    small = npo_list[:10]
    mid = npo_list[:50]


    autoChrome = AutomateChromeURLSearch()

    ## initialize chromedriver and search bar element
    autoChrome.start_driver()


    # arr = ['United Way', 'United way mass', 'cws', 'java', 'wpi goat cheese', 'wpi']

    print(f" FINISHED getting urls. Go the top urls: \n{autoChrome.iterate_for_list(mid)}." )

    ## once all urls are found and validated, add to df 



if __name__ == "__main__":
    import sys
    main(sys.argv)



