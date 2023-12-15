from selenium import webdriver 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import re
import pandas as pd


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
    
    def start_wait(self): 
        wait = WebDriverWait(self.driver, 5)
        # element = wait.until(EC.element_to_be_clickable((By.ID, 'someid')))
        return wait

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

    def tokenize(self, text):
        ## tokenize into a list? or set?
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens
    


    def parse_url(self, url):

        # Regex pattern to match the base_url, domain, and url_text
        pattern = r'(https?://)(www\.)?([\w\.-]+)(\.\w+)(/)(.*)'
        # pattern = r'(https?://[\w\.-]+(\.\w+)+/)(.*)'
        
        # Use regex search to find matches
        match = re.search(pattern, url)
        
        if match:
            base_url = match.group(1) + (match.group(2) if match.group(2) else '') + match.group(3) + match.group(4) + match.group(5)  # The base_url
            domain = match.group(3)  # The domain text
            url_text = match.group(6)  # The url_text
            return base_url, domain, url_text
    
        # else:
        return None, None, None
    
    ''' Get the acronym of an NPO tokensized list name '''
    def get_acronym(self, tok_list, stop_words): 
        
        # Initialize an empty string for the acronym
        acronym = ''
        
        # Iterate over the tokenized strings
        for string in tok_list:
            # If string is a stop word, include the possibility but do not add the letter
            if string in stop_words: 
                acronym += '.?'
            else: 
                # Add the first letter of the string to the acronym
                acronym +=string[0]
        
        return acronym

    def validate_url(self, npo, domain_url): 
        ## tokenize npo name 
        npo_tok = self.tokenize(npo)
        # Define a list of stop words that may of may not be in the NPO name, url, or acronym
        stop_words = ['the', 'a', 'for', 'of', 'and', 'in', 'inc']

        domain_text = domain_url.lower()
        is_match = []
        for tok in npo_tok:
            if tok in stop_words: 
                continue
            ## if tok is not 'the" 
            tok = re.escape(tok)
            pattern = r'{}'.format(tok)
            match = re.search(pattern, domain_text)

            if not match: 
                is_match.append(0)
            else:
                is_match.append(1)

        if len(is_match) >=3:
            if is_match[0] == 1 and is_match[1] == 1: 
                return True 
        if len(is_match) - sum(is_match) <= 2: 
            if sum(is_match)/len(is_match) >= 0.6:
                return True
        
        ## check for accronym of npo name 
        acronym_npo = self.get_acronym(npo_tok, stop_words)
        # print(f" got the npo tok : {npo_tok} .")
        print(f" got the acronym : {acronym_npo} .")
        pattern2 = r'{}'.format(acronym_npo)
        match2 = re.search(pattern2, domain_text)

        if match2: 
            return True
        
        return False


    ''' Get top 10 urls from the google search, parse and process urls '''
    def get_search_result_urls(self, npo):

        # print(f"> Seetkng url for: {self.driver.title} ...")
        results = self.driver.find_element(By.XPATH, "//div[@id='search']/div/div" )
        max_urls = 5

        # npo_urls = []

        all_span = results.find_elements(By.TAG_NAME, 'a')

        ## get the top search result urls  
        for aa in all_span:
            if max_urls == 0: 
                break
            parent = aa.find_element(By.XPATH, "./..")

            if parent.get_attribute('jscontroller') == 'msmzHf':

                temp_url = aa.get_attribute('href')
                # temp_url = self.get_base_url(temp_url)
                
                ## get url meat 
                base_url, domain_text, url_text = self.parse_url(temp_url)
                # print(f'v> Base URL: {base_url}')
                # print(f'v> second URL: {domain_text}')
                # print(f'v> URL Text: {url_text}')

                ## if it passes our url checks, return the url 
                if self.validate_url(npo, domain_text): 
                    print(f">> validated for base url: {base_url} .\n")
                    # ''' get base url? '''
                    # return self.get_base_url(temp_url)
                    return base_url
                ## else, check the next url 
                max_urls -= 1

        ## none of the top 5 search results passed our checks, url not found --> return false 
        return "url_not_found" 
        

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


    def iterate_for_list(self, search_list):
        url_list = []
        wait = self.start_wait()

        ## for all NPO names (in column of df)
        for search in search_list:
            print(f"> Iterating is searching for {search}")
            
            ## eEnter search text in the Google search bar 
            self.search_text(search)
            try: 
                wait.until(EC.presence_of_element_located((By.XPATH,"//div[@id='search']/div/div")))
            # WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".reply-button"))).click()
            # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "element_css"))).get_attribute("value")
            # self.driver.find_element(By.XPATH, "//div[@id='search']/div/div" )
            finally: 
                print(f"\n DRIVER ERROR... Restarting driver. ")
                self.start_driver()
                wait = self.start_wait()
                self.search_text(search)
                wait.until(EC.presence_of_element_located((By.XPATH,"//div[@id='search']/div/div")))
                print(f"Error fixed... Continue at {search}. ")



                # return url_list

            
            ## Get the top url for Google search 
            url_list.append(self.get_search_result_urls(search))

            try: 
                self.locate_search_bar()
            except Exception as e: 
                print(f"Element was stale. {e} .")
                self.start_driver()

        return url_list

def load_data(file_path):

    ## Read the .csv file into a pandas DataFrame
    NPO_df = pd.read_csv(file_path)

    
    npo_list = NPO_df['NAME'].to_list()
    npo_second_name = NPO_df['SORT_NAME'].to_list()

    print(f" ___ got npo list {npo_list}" )
    print(f" ___ got npo back up names list {npo_second_name}" )
    # small = npo_list[:10]
    # mid = npo_list[:50]

    ## Display the DataFrame
    print(NPO_df.head())
    return NPO_df, npo_list, npo_second_name





def main(args):
    print("Starting MAIN ")

    ## Specify the path to the csv file
    # NPO_whitelist_path = "NPO_whitelist_2names.csv"
    NPO_whitelist_path = "whitelist_NPO_cityWorcester.csv"

    npo_df, npo_list, npo_list2 = load_data(NPO_whitelist_path)

    ## start the Automated retreiving 
    autoChrome = AutomateChromeURLSearch()

    # print(f" manual getting: {autoChrome.validate_url('GIRL SCOUTS OF CENTRAL AND WESTERN MASSACHUSETTS INC', 'gscwm')}. ")

    # return 0


    # # Test the function
    # url = 'https://www.exam63846-273-ple.org/some/path'
    # base_url, sec, url_text = autoChrome.parse_url(url)
    # print(f'Base URL: {base_url}')
    # print(f'Domain Text: {sec}')
    # print(f'URL Text: {url_text}')

    # return True

    ## initialize chromedriver and search bar element
    autoChrome.start_driver()
    # short_list = npo_list[:10]

    # urls_list = autoChrome.iterate_for_list(short_list)
    urls_list = autoChrome.iterate_for_list(npo_list)
    # print(f" FINISHED getting urls. Go the top 25 urls: \n{urls_list}." )
    print(f" FINISHED getting urls. Go the top 25 urls: \n{urls_list[:25]}." )

    ## once all urls are found and validated, add to df 
    # return 0

    out_df = npo_df.copy()
    out_df["domain_url"] = urls_list
    print(f"checking out df : {out_df}")

    ## df of validated_profiles and profiles of cityWorcester cross both df and take validated_profiles URL if urls are different 
    out_file = "validated_profiles_url_cityWorcester.csv"
    out_df.to_csv(out_file)
    print("\n Done. ")



if __name__ == "__main__":
    import sys
    main(sys.argv)



