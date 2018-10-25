

Steps to run:

1. install elastic search client 
	pip install elastic search
2. Download elastic search for ubuntu and install.
3. start elastic search service
	sudo systemctl start elasticsearch
4. check if the elastic search is working
	import requests
	res = requests.get('http://localhost:9200')
	print(res.content)
5. install flask
	pip install flask
6. Start the backend
	flask run
7. Go to url to check results and report 
	http://127.0.0.1:5000/


Directory structure

Data/
	wikibooks.py : script to scrape wikibooks Java programming data.
	oracle.py : script to scrape oracle TM data.
	data.csv : wikibooks java programming records
	oracleTM.csv : oracle java programming records.
templates/
	index.html : main user interface of the application
elasticsearch/
	create_es_indices.py: code to create elastic search indices for wikibooks and oracle data.
app.py: backend web services code



** Summary

* Collection of Data
	For data collection I have implemented a web scraping scripts (wikibooks.py/ oracle.py) in python using library BeautifulSoup.

	The script takes main page url and scrapes the data in the underlying liks. It igonres all the non-textual data tags such as 'style', 'script', 'head', 'title', 'meta', '[document]'.

	For wikibooks i have scraped data section by section and for oracle I scraped the data link by link.

	The script records title for each section and its web url. Collected output in a .csv files with data attributes such as url, title, text.

	There are 670 records for wikibook java programming page and 2157 records for oracle TM page.

* Indexing the Content
	For indexing the data I have used ElasticSearch. It uses Apache Lucene and BM25 algorithm at the core for indexing the data.

	I inserted all the csv data to the ElasticSearch using the script create_indexs.py from the source folder.

	Before inserting, I performed natural language preprocessing on data to remove stop words, non_ascii characters.

* Web app
	I have developed a web application using python flask as a backend and simple html, jquery page as a front end

	On application start the backend makes call to elastic search engine with predefined queries provided as queries.xlsx

	Along with predefiend query search an API is provided to get recommendation for any new search query in ElasticSearch.

* Originality
	Scraped Content for wikibooks and oracle TM.

	I have used nltk python package to pre process the data/ search query before adding it to ElasticSearch. I have performed stemming, removal of stop words, removal of non ascii characters which improves overall data quality and recommendation results.

	Provided an API to call ElasticSearch with new search query.

	Performed indexing in Elasticsearch using similarity algorithm BM25, also applied the english analyzer in index mapping while building of indices.

	Created two different indexes for oracle and wikibooks and i found that the search results are dominated by the oracle data as it has more content. With two different indices I show search results from both oracle data and wikibooks data.

