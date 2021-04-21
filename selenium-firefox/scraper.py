from selenium import webdriver
import pandas as pd
import numpy as np
from selenium.webdriver.firefox.options import Options
import time

options = Options()
options.headless = True


da = pd.read_csv('../links.csv')
url_list = da['url'].tolist() 

myDict1 = {}
start_time = time.time()
  
for page_num in range(0, 2):
    print(page_num,end = " ")
    browser = webdriver.Firefox( executable_path="./drivers/geckodriver")
    browser.get(url_list[page_num])
    browser.find_element_by_partial_link_text("More Details...").click()
    title = browser.find_element_by_id('bookTitle').text
    author = browser.find_element_by_class_name("authorName").text 
    avg_rating = browser.find_element_by_xpath("/html/body/div[2]/div[3]/div[1]/div[2]/div[4]/div[1]/div[2]/div[2]/span[2]").text
    num_rating = browser.find_element_by_xpath("/html/body/div[2]/div[3]/div[1]/div[2]/div[4]/div[1]/div[2]/div[2]/a[2]").text
    num_review = browser.find_element_by_xpath("/html/body/div[2]/div[3]/div[1]/div[2]/div[4]/div[1]/div[2]/div[2]/a[3]").text
    details = browser.find_element_by_id("details")
    temp1 = details.text.split("\n")
    
    page = 0
    series = 0
    
    # num rating
    try:
        num_ratings = num_rating.split()[0]
    except:
        num_ratings = 0
    
    # num review
    try:
        num_reviews = num_review.split()[0]
    except:
        num_reviews = 0

    places = np.nan
    awards = np.nan

    # total_pages
    try:
        num_pages = [int(s) for s in temp1[0].split() if s.isdigit()]
        num_pages = str(num_pages[0])
    except IndexError:
        num_pages = np.nan

    # year
    try:
        year = [int(s) for s in temp1[1].split() if s.isdigit()]
        original_publish_year = str(year[0]) 
    except IndexError:
        original_publish_year = np.nan

    # places
    for i in range(len(temp1)):
        if(temp1[i]=="Setting"):
            places = temp1[i+1]
        
    # series
    for i in range(len(temp1)):
        if(temp1[i] == "Series"):
            series = 1

    # Awards
    for i in range(len(temp1)):
        if(temp1[i] == "Literary Awards"):
            awards = temp1[i+1]
    
    # genre
    genre = browser.find_elements_by_css_selector("div.left>a.bookPageGenreLink")
    temp2 = [i.text for i in genre]

    try:
        genres = temp2[0:3]
    except IndexError:
        genres = np.nan

    myDict1[page_num] = (url_list[page_num],title, author, avg_rating, num_ratings,  num_reviews,  num_pages, original_publish_year, places, series, awards, genres)
    browser.close()

print("time taken: %s seconds ---" % (time.time() - start_time))
df = pd.DataFrame.from_dict(myDict1, orient='index', columns=['url','title', 'author', 'num_reviews', 'num_ratings', 'avg_rating',  'num_pages', 'original_publish_year', 'series', 'genres', 'awards', 'places'])
df.to_csv('filename.csv')

