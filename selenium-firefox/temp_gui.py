from selenium import webdriver
import pandas as pd
import numpy as np
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd
import numpy as np
import requests as rq
from bs4 import BeautifulSoup
import PySimpleGUI as sg


options = Options()
options.headless = True


sg.theme('DarkGrey13')


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

def get_whole_book_links(dir_base_url, pages):
    whole_book_url_list = []
    human_like_time = np.random.uniform(2, 7)
    for i, link in enumerate(get_base_page_list(dir_base_url, pages)):
        whole_book_url_list += get_books_url_per_page(link, 'a', 'bookTitle')
        print(f'link {i}: {link}')
    # whole_book_url_list = [link for subs in whole_book_url_list for link in subs]
    return whole_book_url_list

#browse_page = 3 
#start_time = time.time()
#whole_book_url_list_ = get_whole_book_links('https://www.goodreads.com/list/show/50.The_Best_Epic_Fantasy_fiction_?page=', browse_page)

#link_df = pd.DataFrame({'url': whole_book_url_list_})
#print(link_df)
#link_df.to_csv('./links_temp.csv')
#print("time taken: %s seconds ---" % (time.time() - start_time))

# analyse task2
def func_mean_minmax_norm_ratings(authorname, df2):
    f=df2[df2.loc[:,'author'] == 'J.K. Rowling']
    desired_book = f[f.loc[:,'minmax_norm_ratings']== f['minmax_norm_ratings'].max()]
    return desired_book.title

def scraper(dir_base_url, browse_page):
    whole_book_url_list_ = get_whole_book_links(dir_base_url, browse_page)
    print(type(whole_book_url_list_))
    myDict1 = {}
    start_time = time.time()
    da = pd.read_csv('../links.csv')
    url_list = da['url'].tolist()
    for page_num in range(0, 2):
        print(page_num,end = " ")
        browser = webdriver.Firefox(options=options, executable_path="./drivers/geckodriver")
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
    dfn = df.convert_dtypes()
    dfn['series'] = dfn['series'].astype('bool')
    dfn.to_csv('filename.csv')
    
def preprocessing(csv_path):
    df = pd.read_csv(csv_path)  # csv_path
    #df2['awards'].isna().any()
    df5 = df 
    df5['Awards_count'] = df5.awards.str.count(',')+1
    df5['Awards_count'] = df5['Awards_count'].fillna(value=0) 
    
    # min-max
    df1 = df5
    max_min_value = df['avg_rating'].max() - df['avg_rating'].min()
    min_value = df['avg_rating'].min()
    df1['minmax_norm_ratings'] = 1 + (df1['avg_rating'] - min_value) / (max_min_value) * 9
    
    # mean
    max_min_value = df1['avg_rating'].max() - df1['avg_rating'].min()
    mean_value = df1['avg_rating'].mean()
    df1['mean_norm_ratings'] = 1 + (df1['avg_rating'] - mean_value) / (max_min_value) * 9
    return df1

def analyse(df):
    # task 1
    df2 = df
    #df2.dropna(inplace=True)
    df2['original_publish_year'].dropna(inplace=True) 
    df2['original_publish_year'].nunique()
    min_1 = df2['original_publish_year'].quantile(0.01)
    min_2 = df2['original_publish_year'].quantile(0.99)
    df2['original_publish_year'] = np.where(df2['original_publish_year'] < min_1, min_1,df2['original_publish_year'])
    df2['original_publish_year'] = np.where(df2['original_publish_year'] > min_2, min_2,df2['original_publish_year'])
    s = df2.groupby(['original_publish_year'])['minmax_norm_ratings'].mean()
    df3 = s.to_frame()
    df3.plot()  # .get_figure()
    # task 2
    bookname = func_mean_minmax_norm_ratings('J.K. Rowling',df2)          # function above
	
def open_window():
	layout = [[sg.Text('Hufflepuff_Scrapper')],
	#[sg.Image(r'../index.png')],
	[sg.Text('Enter Url to scrapp')],
	[sg.Input()],
	[sg.Button('Scrapp'), sg.Button('Exit')],
	[sg.ProgressBar(1, orientation='h', size=(20, 20), key='progress')]]
	dir_base_url = 'https://www.goodreads.com/list/show/50.The_Best_Epic_Fantasy_fiction_?page='
	#scraper(dir_base_url)
	csv_path = 'final_01.csv'
	df = preprocessing(csv_path)
	analyse(df
	#This Creates the Physical Window
	window = sg.Window('Hufflepuff_Scrapper', layout, resizable=True, icon='../index.png').Finalize()
	progress_bar = window.FindElement('progress')
	while True:
		event, values = window.read()   # Read the event that happened and the values dictionary
		print(event, values)
		if event == sg.WIN_CLOSED or event == 'Exit':     # If user closed window with X or if user clicked "Exit" button then exit
			break
		if event == 'Scrapp':
			print('You pressed the button')
			break
	#This Updates the Window
	#progress_bar.UpdateBar(Current Value to show, Maximum Value to show)
	url = values
	progress_bar.UpdateBar(0, 5)
	time.sleep(.5)
	progress_bar.UpdateBar(1, 5)
	time.sleep(.5)
	progress_bar.UpdateBar(2, 5)
	time.sleep(.5)
	progress_bar.UpdateBar(3, 5)
	time.sleep(.5)
	progress_bar.UpdateBar(4, 5)
	time.sleep(.5)
	progress_bar.UpdateBar(5, 5)
	time.sleep(.5)
	window.close()
	return url


def main():
	layout = [[sg.Button("Open Window", key="open")],[sg.Image(r'../index.png')]]
	window = sg.Window("Main Window", layout,icon='../index.png')
	while True:
		event, values = window.read()
		if event == "Exit" or event == sg.WIN_CLOSED:
			break
		if event == "open":
			open_window()
			window.Maximze()
			window.close()

if __name__ == "__main__":
    main()
