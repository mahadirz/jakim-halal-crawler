# jakim-halal-crawler

Jakim Halal Crawler can perform search on http://www.halal.gov.my/ehalal/directory_standalone.php scrape and crawl the contents, 
and exported it into JSON or into database.

## Installation
1. Install Scrapy (http://scrapy.org/)
2. git clone https://github.com/mahadirz/jakim-halal-crawler.git
3. cd jakim-halal-crawler
4. scrapy crawl halal_crawler -a keyword=nescafe -o items.json -t json
