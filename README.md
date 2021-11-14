# 2400-DS1WSMS-Web-Scraping
This repo contains python code for the school project.

## Execution 

* run `scrapy crawl LinkSpider -o LinkLists.csv` from command line
* scrapy will ask uer to specify the *starting page* and *last page*
* run `python b_rmduplicates.py` to remove possible duplicated entries 
* after the message "Deplicates have been removed" is shown, user can start scraping the property details by using the following command
```
scrapy crawl PropertySpider -o property.csv
```
* since scrapy will call for all spiders in the spiders folder, the following prompt will be shown, however
this can be ignored by typing any integer, e.g. 1 and 1 . Please note that non-integer input will cause
error and the program will be terminated.

```
Please specify the page range (min=1, max=285):
starting page: 1
last page: 1
```

## Output

There are total 3 output files

* `LinkLists.csv` - a list of links that pointing to corresponding property details 
* `lists.csv` - the same file after duplicates are removed 
* `property.csv` - final output 

