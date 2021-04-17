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
	
def open_window():
	layout = [[sg.Text('Hufflepuff_Scrapper')],
	[sg.Image(r'../index.png')],
	[sg.Text('Enter Url to scrapp and analyse')],
	[sg.Input()],[sg.Button('Ok')],
	[sg.ProgressBar(1, orientation='h', size=(20, 20), key='progress')]]
	#This Creates the Physical Window
	window = sg.Window('Hufflepuff_Scrapper', layout, resizable=True, icon='../index.png').Finalize()
	progress_bar = window.FindElement('progress')

	#This Updates the Window
	#progress_bar.UpdateBar(Current Value to show, Maximum Value to show)
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

def main():
    layout = [[sg.Button("Open Window", key="open")]]
    window = sg.Window("Main Window", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "open":
            open_window()
        
    window.close()
if __name__ == "__main__":
    main()
