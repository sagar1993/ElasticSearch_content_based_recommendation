import urllib2
import re
import re
from bs4 import BeautifulSoup
import json
import datetime
from dateutil.parser import parse
from bs4.element import Comment
import pandas as pd
import collections

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def get_ascii_only(string):
    return ''.join([i if ord(i) < 128 else '' for i in string])
    

def text_from_html(body):
    # soup = BeautifulSoup(body, 'html.parser')
    try:
        texts = body.findAll(text=True)
        visible_texts = filter(tag_visible, texts)  
        return u" ".join(t.strip() for t in visible_texts)
    except:
        return ""

def parse_data_save(links):
    d_title = collections.defaultdict(int)
    result = []
    for title, link in links:
        if title in ("If you are interested in editing this book", "If you have questions related to Java"):
            continue
        page = urllib2.urlopen(link)
        soup = BeautifulSoup(page)
        text = ""
        t = ""
        for tag in content:
            if tag.name == 'table':
                continue
            if tag.name in ('h1','h2', 'h3', 'h4', 'h5'):
                d = {}
                d["url"] = link
                titt = title + " " + t
                titt = titt.replace("[edit]", "")
                d['title'] = titt
                d['text'] = text
                if text:
                    result.append(d)
                text = ""
                t = tag.text
            else:
                text += get_ascii_only(text_from_html(tag).strip())
    df = pd.DataFrame(result)
    df.to_csv('data.csv')
    return df

def remove_spaces(text):
    return re.sub('\s+',' ',text)

def get_all_wikibooks_links(wikibooks_url):
    page = urllib2.urlopen(wikibooks_url)
    soup = BeautifulSoup(page)
    main_div = soup.find('div', class_="mw-content-ltr")
    ul = main_div.find_all('ul')
    domain = "https://en.wikibooks.org/%s"
    links = []
    for u in ul:
        li = u.find_all('li')
        for l in li:
            a_tag = l.find('a', recursive=False)
            if a_tag: 
                link_text = a_tag.text
                link = domain%a_tag.get('href')
                links.append((link_text, link))
    return links
    

wikibooks_url = 'https://en.wikibooks.org/wiki/Java_Programming'
df = parse_data_save(get_all_wikibooks_links(wikibooks_url))
