import pandas as pd
import numpy as np
import requests as rq
from bs4 import BeautifulSoup

url_df= pd.read_csv('./links.csv')
url_list = url_df.url.to_list()

# print(url_list)

# url = 'https://www.goodreads.com/book/show/30.J_R_R_Tolkien_4_Book_Boxed_Set'

genre_list = []
awards_list = []
title_list = []
author_list = []
num_reviews_list = []
avg_ratings_list = []
num_pages_list = []
original_publish_year_list = []
is_series_list = []
palces_list = []





#url title author num_reviews num_ratings avg_ratings num_pages original_publish_year series genres awards palces

for link in url_list[:20]:
    page = rq.get(link)
    page_content = BeautifulSoup(page.content, 'html.parser')

    # get the genres
    genre_per_book = []
    for i in range(3):
        genre = page_content.find_all('a', class_ = 'actionLinkLite bookPageGenreLink')[i].text
        genre_per_book.append(genre)
    genre_list.append(genre_per_book)

    # get the awards (if any)
    if page_content.find_all('div', itemprop = 'awards'):
        awards = page_content.find_all('div', itemprop = 'awards')[0].text
        awards_list.append(awards)
    else:
        awards_list.append(np.nan)
    
    # get the title
    title = page_content.find_all('h1', itemprop = 'name')[0].text
    title = title.replace('\n','').strip()
    title_list.append(title)


    
# page = rq.get(url)
# page_content = BeautifulSoup(page.content, 'html.parser')

# title = page_content.find_all('div', id = 'bookDataBox')[0].find_all('div', class_ = 'clearFloats')[0].find_all('div', class_ = 'infoBoxRowItem')[0].text
# title = page_content.find_all('h1', itemprop = 'name')[0].text

# print(title)

print(genre_list)
print(awards_list)
print(title_list)