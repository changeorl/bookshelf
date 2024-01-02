import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 

def get_projects(rankID: int, soup: BeautifulSoup):
    print('----------------------------------------------------------------------')
    targets = soup.find_all('div', class_='project-search-results')[0].find_all('a')
    for i, t in enumerate(targets):
        projectID = i + rankID
        title = t.find_all('h3')[0].text
        link = t["href"]
        print(f'{projectID}, {title}, {link}')

def get_professors(rankID: int, soup: BeautifulSoup):
    professors = list()
    print('----------------------------------------------------------------------')
    targets = soup.find_all('div', class_='profile-search-results')[0].find_all('a')
    for i, t in enumerate(targets):
        staffID = i + rankID
        img = t.find_all('img')[0]['src']
        name = t.find_all('h3')[0].text
        role = t.find_all('p', class_='card-profile__role')[0].text
        school = t.find_all('div', class_='card-profile__title')[0].text
        desc = t.find_all('div', class_='card-profile__content')[0].text
        link = t["href"]
        professors.append((staffID, name, role, school, desc, link, img))
        print(f'{staffID}, {name}, {role}, {school}')

def crawler(rankID):

    url = f'https://www.unsw.edu.au/research/hdr/find-a-supervisor'\
            '#search=&sort=date&startRank={rankID}&numRanks=12'\
            '&componentId=9b55bf87-4f96-4bd5-ac5a-77540c6557f8'
    # https://www.unsw.edu.au/research/hdr/find-a-supervisor
    # #search=&sort=date&startRank=1&numRanks=12&
    # componentId=36c3802e-58bd-404b-90f6-07d44daf6b35


    # instantiate options 
    options = webdriver.ChromeOptions() 
    
    # run browser in headless mode 
    options.headless = True 
    
    # instantiate driver 
    driver = webdriver.Chrome(service=ChromeService( 
        ChromeDriverManager().install()), options=options) 
    
    driver.get(url) 

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    return soup

if __name__ == '__main__':

    rankIDs = [i for i in range(1,23,12)]

    
    # print(rankIDs)
    for i in rankIDs:
        soup = crawler(i)
        get_projects(i, soup)
        get_professors(i, soup)
