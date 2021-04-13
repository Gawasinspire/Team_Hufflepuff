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
places_list = []





#url title author num_reviews num_ratings avg_ratings num_pages original_publish_year series genres awards palces

for link in url_list[:20]:
    page = rq.get(link)
    page_content = BeautifulSoup(page.content, 'html.parser')

    # get the genres
    # genre_per_book = []
    # for i in range(3):
    #     genre = page_content.find_all('a', class_ = 'actionLinkLite bookPageGenreLink')[i].text
    #     genre_per_book.append(genre)
    # genre_list.append(genre_per_book)

    # get awards (if any)
    # if page_content.find_all('div', itemprop = 'awards'):
    #     awards = page_content.find_all('div', itemprop = 'awards')[0].text
    #     awards_list.append(awards)
    # else:
    #     awards_list.append(np.nan)
    
    # get title
    # title = page_content.find_all('h1', itemprop = 'name')[0].text
    # title = title.replace('\n','').strip()
    # title_list.append(title)

    # get author name
    # author = page_content.find_all('div', class_ = 'authorName__container')[0].find_all('span', itemprop = 'name')[0].text
    # author_list.append(author)

    # get num_reviews
    # num_reviews = page_content.find_all('meta', itemprop = 'reviewCount')[0].attrs['content']
    # num_reviews_list.append(num_reviews if page_content.find_all('meta', itemprop = 'reviewCount')[0].attrs['content'] else np.nan)

    # get avg_ratings
    # avg_ratings = page_content.find_all('div', itemprop = 'aggregateRating')[0].find_all('span', itemprop = 'ratingValue')[0].text
    # avg_ratings_list.append(avg_ratings)

    # get num_pages
    # num_pages = page_content.find_all('span', itemprop="numberOfPages")[0].text
    # num_pages_list.append(num_pages[:-6])

    # get original_publish_year
    # if page_content.find_all('nobr', class_ = "greyText"):
    #     original_publish_year = page_content.find_all('nobr', class_ = "greyText")[0].text.strip()
    #     original_publish_year_list.append(original_publish_year[-6:-1])
    # else:
    #     original_publish_year = page_content.find_all('div', class_ = "uitext darkGreyText")[0].find_all('div', class_ = 'row')[1].text.split('\n')
    #     original_publish_year_list.append(original_publish_year[2][-4:])

    # get is_series
    if page_content.find_all('div', id = "bookDataBox")[0].find_all('div', class_ = 'clearFloats')[0].find_all('div', class_ = "infoBoxRowTitle")[0].text == 'Original Title':
        is_series = page_content.find_all('div', id = "bookDataBox")[0].find_all('div', class_ = 'clearFloats')[3].find_all('div', class_ = "infoBoxRowTitle")[0].text
        is_series_list.append(1 if is_series == 'Series' else 0)
    else:
        is_series = page_content.find_all('div', id = "bookDataBox")[0].find_all('div', class_ = 'clearFloats')[3].find_all('div', class_ = "infoBoxRowTitle")[0].text
        is_series_list.append(1 if is_series == 'Series' else 0)

    # get places

# df = pd.DataFrame({'title': title_list, 'author': author_list, 'num_reviews': num_reviews_list, 'num_ratings': avg_ratings_list, 'num_pages': num_pages_list, 'original_publish_year': original_publish_year_list})

# print(df)
    



    
# page = rq.get(url)
# page_content = BeautifulSoup(page.content, 'html.parser')

# title = page_content.find_all('div', id = 'bookDataBox')[0].find_all('div', class_ = 'clearFloats')[0].find_all('div', class_ = 'infoBoxRowItem')[0].text
# title = page_content.find_all('h1', itemprop = 'name')[0].text

# print(title)

# print(genre_list)
# print(awards_list)
# print(title_list)