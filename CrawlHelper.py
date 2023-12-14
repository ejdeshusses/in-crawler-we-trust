import numpy as np 
import pandas as pd 
import queue 



''' crawled_data: {
    'url': WebPage object, 
    'url': WebPage object, 
    'url': WebPage object, 
    ....
    }   
    
    '''


class CrawlerData: 
    def __init__(self, seed):
        self.seed = seed
        self.crawl_count = 0
        self.queue = queue.PriorityQueue()
        self.crawled_data = dict

    def enqueue(self, url):
        self.queue.put(url)
        return True
    
    def offqueue(self, url):
        self.queue.task_done(url)
        return True
    
    def add_page(self, page):
        self.crawled_data[page.url] = page
        self.crawl_count += 1
        return self.crawl_count

    

''' links: {
    'url': {(REL, int), (REL, int)}, 
    'url': {(REL, int), (REL, int)}, 
    'url': {(REL, int), (REL, int), (REL, int), (REL, int)}, 
    ....
    }   
    
    '''

## Struct for webpage 
class WebPage:
    # def __init__(self, url, link_type, base_url, relationship_type):
    def __init__(self, url):
        self.url = url
        self.whitelinks = set
        self.links = dict
        self.out_types = { ".com": 0, 
         ".edu": 0, 
         ".gov": 0, 
         ".org": 0, 
         ".net": 0, 
         "other": 0
         }
        self.rel_types = { "partner": 0, 
         "donor": 0, 
         "sponsor": 0, 
         "news": 0, 
         "other": 0
         }
        # self.relationship_type = relationship_type

    ''' increment dict counter for link domain extension type '''
    def link_type(self, link_type):
        if self.out_types[link_type]:
            self.out_types[link_type] += 1
            return self.out_types[link_type]
        
        self.out_types["other"] += 1
        return self.out_types["other"]
    

    ''' increment dict counter for relationship_type'''
    def rel_type(self, rel_type):
        if self.rel_types[rel_type]:
            self.rel_types[rel_type] += 1
            return self.out_types[rel_type]
        
        self.rel_types["other"] += 1
        return self.out_types["other"]
        
    ''' add link and the relationship type found for this link'''
    def add_link(self, url, rel_type):
        # def check_and_add(dictionary, key):
        if url in self.links:
            for tup in self.links[url]:
                if tup[0] == rel_type:
                    tup[1] += 1
                    break
            self.links[url].add((rel_type, 1))
        else:
            self.links[url] = {(rel_type, 1)}

        ## add relationship demographic -- or do this at the end using this collected data
        return True






        # if self.links[url] 
        # self.links
        ## if url in whitelist, then add to whitepages


class CrawlHelp:
    def __init__(self): 
        self.data_df = pd.DataFrame
        self.data_set = set 
        # self.data_df = pd.DataFrame
        pass 

    def init_data(self, dataset): 
        self.data_df = pd.DataFrame(dataset)
        return True
    
    # def init_set(self, dataset): 
    #     self.data_set = set
    #     return True


    def is_link_whitelisted(self, url):

        ## search for url in dataframe of whitelisted NPOs
        if url in self.data_set: 
            return True
        
        return False
    






class ProcessPage: 
    def __init__(self, self_domain):
        self.self_domain = self_domain
        self.total_count = None 
        self.whitelist = set


    def process_links(self):
        ## get unique domains 
        return 0



