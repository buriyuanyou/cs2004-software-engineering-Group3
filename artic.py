from urllib.request import urlopen, Request
import urllib3
from bs4 import BeautifulSoup
from pandas import DataFrame
import os
import requests
import random
import time
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
count  = 0
df_ret = DataFrame(columns=[" name", "time", "medium", "classification", "dimension", "artist", "location", "details", "detail_url ","photo_url", "photo_name"])
# encoding:utf-8

def details_page(url):
    
    ret = Request(url, headers=headers)
    res = urlopen(ret)
    contents = res.read()
    soup = BeautifulSoup(contents, "html.parser")

    ptag = soup.find('ul', class_ = 'm-article-header__img-thumbs')
    if ptag != None:
        
        m_photo = ptag.find('button').get('data-gallery-img-download-url')
        m_photo_name = m_photo.split('/')[-5]+'.jpg'
    else:
        return
 
    
    
    tag1 = soup.find('dd', itemprop="name")
    m_name = tag1.find('span',  class_ = 'f-secondary').get_text()

    m_artist = soup.find('dd', itemprop="creator")
    if m_artist == None:
        m_artist = 'unknown'
    else:
        m_artist = m_artist.find('a').get_text()

    m_date = soup.find('dd', itemprop="dateCreated")
    if m_date == None:
        m_date = 'unknown'
    else:
        m_date = m_date.find('a').get_text().strip()

    m_medium = soup.find('dd', itemprop="material")
    if m_medium == None:
        m_medium = 'unknown'
    else:
        m_medium = m_medium.find('span',  class_ = 'f-secondary').get_text()

    m_dimension = soup.find('dd', itemprop="size")
    if m_dimension == None:
        m_dimension = 'unknown'
    else:
        m_dimension = m_dimension.find('span', class_ = 'f-secondary').get_text()

    m_location = soup.find('dd').find('span', class_ = 'f-secondary').get_text() + ',The Art Institute of Chicago'   
    m_classification = 'unknown'

    m_details = soup.find('p', class_ = 'title f-secondary o-article__inline-header-display')
    if m_details != None:
        m_details = m_details.get_text()
    else:
        m_details = 'unknown'

    global df_ret
    #print(m_name + "        " + m_date + "           " + m_medium + "    " +  m_classification + "    " +  m_dimension + "    "+  m_artist + "    " +  m_location + "    " +  m_details + "    "+ url+ "    " + m_photo + "    " +m_photo_name)
    global count
    print(url, "ok")
    df_ret.loc[count] = [m_name, m_date, m_medium, m_classification, m_dimension, m_artist, m_location, m_details, url, m_photo, m_photo_name]
    count = count +1
        
    


def this_page(url):
   
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    ret = Request(url, headers=headers)
    res = urlopen(ret)
    contents = res.read()
    soup = BeautifulSoup(contents, "html.parser")
    

    for tag in soup.find_all('li', class_='m-listing m-listing--variable-height o-pinboard__item'):        
        details_url = tag.find('a').get('href') 
        details_url = details_url.split('/')[:5]
        details_url = '/'.join(details_url)
        details_page(details_url)

        
        
       
       

if __name__ == '__main__':
    
    for i in range(25, 30):
        liststr = ['https://www.artic.edu/collection?q=chinese&page=', repr(i)]
        next_url = ''.join(liststr)
        print("page = ", i)
        this_page(next_url)
        df_ret.to_csv('text.csv', encoding= 'utf_8')
    else:
        print("爬取完成")
