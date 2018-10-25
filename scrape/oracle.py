import urllib2
import re
import re
from bs4 import BeautifulSoup
import json
import datetime
from dateutil.parser import parse
from bs4.element import Comment
import pandas as pd

def remove_spaces(text):
    return re.sub('\s+',' ',text)
oracle_url = 'https://docs.oracle.com/javase/tutorial/'

def get_all_links(oracle_url):
    page = urllib2.urlopen(oracle_url)
    soup = BeautifulSoup(page)
    ul = soup.find_all('ul', class_="BlueArrows")
    
    domain = "https://docs.oracle.com/javase/tutorial/%s"
    links = []
    for u in ul:
        li = u.find_all('li')
        for l in li:
            a_tag = l.find('a')
            if a_tag:
                href = a_tag.get('href')
                title = a_tag.text
                if 'http' in href:
                    links.append((title, href))
                else:
                    links.append((title, domain%href))
    return links

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

def get_links_text(all_links):
    url_list = []
    url_list.extend(all_links)

    result = []
    domain = "https://docs.oracle.com/javase/tutorial/%s"
    url_set = set()
    while url_list:
        title, url, depth = url_list.pop()
        url_set.add(url)
        if depth > 6:
            continue
        try:
            page = urllib2.urlopen(url)
        except:
            continue

        soup = BeautifulSoup(page)
        body = soup.find('div', {"id":"PageContent"})
        if body:
            d = {}
            d["url"] = url
            d["title"] = title
            d["text"] = text_from_html(str(body)).encode('utf-8').strip()
            result.append(d)

            a_tags = body.find_all('a')
            for tag in a_tags:
                href = tag.get('href')
                text = tag.text
                if not href:
                    continue
                if 'http' in href:
                    href_url = href
                else:
                    href_url = url.replace('index.html', href)
                if href_url not in url_set and 'docs.oracle.com' in href_url:
                    url_list.append((text, href_url, depth+1))
    return result

links = get_all_links(oracle_url)
all_links = [(title, link, 0) for title, link in links]
result = get_links_text(all_links)
df.to_csv('oracleTM.csv')
