#!/usr/bin/python
from flask import Flask, Response, render_template
from flask import request, jsonify
from bson.json_util import dumps, loads
from flask_cors import CORS
import datetime
import pandas as pd
from sklearn.feature_extraction import text
from nltk.stem.porter import PorterStemmer
import collections

from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    
def preprocessing(df_col):
    stop = text.ENGLISH_STOP_WORDS
    porter_stemmer = PorterStemmer()
    df_col = df_col.apply(lambda x: ''.join(["" if ord(i) < 32 or ord(i) > 126 else i for i in x]))
    df_col = df_col.apply(lambda x: ' '.join([porter_stemmer.stem(word.lower()) for word in x.split() if word not in (stop)]))
    return df_col

def read_queries():
	queries = pd.read_excel('queries.xlsx')
	queries['text_1'] = preprocessing(queries['text'])
	ret = []
	for index in range(len(queries)):
	    query = queries.iloc[index]['text_1']
	    query_text = queries.iloc[index]['text']
	    
	    res_wikibooks = es.search(index='java_wikibook',from_=0, size=10, body={"query": {
		"multi_match" : {
		  "query":    query,
		  "fields": [ "text"] 
		}
	    }})
	    
	    result = {}
	    result['data'] = []
	    
	    for item in res_wikibooks['hits']['hits']:
		d = {}
		title = item['_source']['title']
		url = item['_source']['url']
		d['title'] = title
		d['url'] = url
		result['data'].append(d)
		result['title'] = query_text
	    ret.append(result)
	return ret

app = Flask(__name__, static_url_path='')
CORS(app)

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/getdata', methods=['GET'])
def getdata():
	return dumps(read_queries())
