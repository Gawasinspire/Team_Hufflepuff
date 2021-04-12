import pandas as pd
import numpy as np
import requests as rq
from bs4 import BeautifulSoup




base_url = 'https://www.goodreads.com/list/show/50.The_Best_Epic_Fantasy_fiction_'

def get_books_url(base_url, tag, tag_class):

    book_url_list = []
    base_page = rq.get(base_url)
    base_content = BeautifulSoup(base_page.content, 'html.parser')

    for a in base_content.find_all(tag, class_= tag_class):
        book_url_list.append('https://www.goodreads.com/' + a['href'])
    
    return book_url_list
