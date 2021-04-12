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

# books = get_books_url(base_url, 'a', 'bookTitle')
# print(books)

book_base_url = 'https://www.goodreads.com/book/show/13496.A_Game_of_Thrones'

book_base_page = rq.get(book_base_url)

book_base_content = BeautifulSoup(book_base_page.content, 'html.parser')

title = book_base_content.find_all('h1', id = 'bookTitle')[0].text
print(title)
print(type(title))