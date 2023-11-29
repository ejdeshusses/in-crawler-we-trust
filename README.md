# in-crawler-we-trust

Updated 11/28/23: 
> NPO_whitelist_2names.csv - file of 236 NPOs we may be interested in. Data sourced from the IRS: EO BMF datasets (https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf , Last updated 10/09/23) --> eo_ma.csv for Massachusetts. Parsed for charities and nonprofits of a certain profile.
  > includes [index in eo_ma.csv, EIN, NAME, ICO, SORT_NAME ]

> NpoUrlGetterTest.py - uses Selenium to automate searching Google and getting urls for each of the whitelisted NPOs.

> url_getter.ipynb - [ rename to NPO name getter] script loads  data from the NPO_whitelist_2names.csv file and attempts some parsing. under developed. use may have been outlived. 
