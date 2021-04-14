import pandas as pd
import numpy as np
import requests as rq
from bs4 import BeautifulSoup




base_url = 'https://www.goodreads.com/list/show/50.The_Best_Epic_Fantasy_fiction_'

def get_books_url_per_page(base_url, tag, tag_class):

    book_url_list = []
    base_page = rq.get(base_url)
    base_content = BeautifulSoup(base_page.content, 'html.parser')

    for a in base_content.find_all(tag, class_= tag_class):
        book_url_list.append('https://www.goodreads.com/' + a['href'])
    
    return book_url_list


def get_base_page_list(base_url, pages):
    base_page_list = []
    for i in range(pages):
        base_page_list.append(base_url + str(i + 1))
    
    return base_page_list


def get_whole_book_links(base_url, pages):
    whole_book_url_list = []

    for link in get_base_page_list(base_url, pages):
        whole_book_url_list.append(get_books_url_per_page(link, 'a', 'bookTitle'))

    whole_book_url_list = [link for subs in whole_book_url_list for link in subs]

    print(len(whole_book_url_list))

whole_book_url_list_ = get_whole_book_links('https://www.goodreads.com/list/show/50.The_Best_Epic_Fantasy_fiction_?page=', 36)

link_df = pd.DataFrame({'url': whole_book_url_list_})
print(link_df)
# link_df.to_csv('./links.csv')

# 'https://www.goodreads.com/list/show/50.The_Best_Epic_Fantasy_fiction_?page='





