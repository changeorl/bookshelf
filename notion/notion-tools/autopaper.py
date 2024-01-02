"""
python autopaper.py -d 0705
python autopaper.py
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime,date
import json
from apis import insert_database, get_database
from settings import *
import time
import argparse
from utils import api_debug

def get_daily_papers_hf(search_date: str):
    #https://huggingface.co/papers?date=2023-07-06

    domain = 'https://huggingface.co'
    # Send a GET request to the website
    # _date = f'?date={search_date}' if search_date else None
    url = f'https://huggingface.co/papers?date={search_date}'

    response = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    timestamp = soup.find_all('time')[0]['datetime']    
    datetime_obj = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    print(f'{datetime_obj.strftime("%A, %B %d, %Y")}\n')
    print('crawling from huggingface...\n')
    if datetime.strptime(search_date, "%Y-%m-%d").date() != datetime_obj.date():
        print(f'nothing published on {search_date}')
        exit()

    papers_today = list()
    response = get_database(DATABASE.daily_paper)
    for paper in response.json()['results']:
        if not paper['properties']['published']['date']:
            continue
        _published =  paper['properties']['published']['date']['start']
        _datetime_obj = datetime.strptime(_published, "%Y-%m-%dT%H:%M:%S.%f%z")
        if _datetime_obj.date() == datetime_obj.date():
            airxID = paper['properties']['airxID']['rich_text'][0]['plain_text']
            papers_today.append(airxID)

    papers = list()

    # Find all the paper entries on the page
    paper_entries = soup.find_all('h3')#, class_='m-1')

    # Iterate over each paper entry and extract the link and name
    for index, entry in enumerate(paper_entries, 1):
        name = entry.text
        link = f"{domain}{entry.find('a')['href']}"
        #print(index,name,link)

        # Send a GET request to the pdflink
        pdflink_response = requests.get(link)

        # Create a BeautifulSoup object for the pdflink
        pdflink_soup = BeautifulSoup(pdflink_response.content, 'html.parser')

        # Find all the links inside the pdflink
        pdflinks = pdflink_soup.find_all('a')

        # Iterate over each pdflink and extract the link
        for pdflink in pdflinks:
            pdflink_href = pdflink.get('href')
            if pdflink_href and pdflink_href.startswith('https://arxiv.org/pdf/'):
                airxID = pdflink_href.split('/')[-1]
                _exist = True if airxID in papers_today else False
                papers.append((airxID, name,link, pdflink_href,timestamp, _exist))
                print(f'{index}, `{name}`, {airxID},{link}, {pdflink_href},{timestamp}')
                break
        
        #     break

    filename = f'daily-paper/.cache/{datetime_obj.date()}.json'
    with open(filename, 'w') as json_file:
        json.dump(papers, json_file)

    return papers,filename


def send_daily_paper_notion(papers):
    print("\nsending to Notion...\n")
    _sucess = 0
    for index, paper in enumerate(papers, 1):
        (airxID, name,link, pdflink_href, published, _exist) = paper

        if _exist:
            print(f'{index} Already existed `{name}`')
            continue

        row = {
            "title": {
                "id": "title",
                "type": "title",
                "title": [{'type': 'text', 'text': {'content': name}}]
            },
            "airxID": {
                "id": "QLE_",
                "type": "rich_text",
                "rich_text": [{'type': 'text', 'text': {'content': airxID}}]
            },
            "hflinks": {
                "id": "~iC%3A",
                "type": "url",
                "url": link
            },
            "pdf": {
                "id": "%7DlnA",
                "type": "url",
                "url": pdflink_href
            },
            "published": {
                "id": "%40P%3Dx",
                "type": "date",
                "date": {
                    "start": published,
                    "end": None,
                    "time_zone": None
                }
            },
        }

        response = insert_database(DATABASE.daily_paper,row)
        if response.ok:
            print(f'{index} Successfully added `{name}`')
            _sucess+=1
            time.sleep(1)
        else:
            print(f'{index} Failed to send `{name}`')
            time.sleep(1)
            continue
    
    return _sucess


parser = argparse.ArgumentParser(description='Send daily paper to Notion.')
parser.add_argument('-d','--date', default=None, help='Input file path')
args, unknown = parser.parse_known_args()
_date = args.date

if _date:
    search_date = f"2023-{_date[:2]}-{_date[2:]}"
    # print(search_date)
    if datetime.strptime(search_date, "%Y-%m-%d").date() > date.today():
        print(f'\n{search_date} is a future date.')
        exit()
else:
    search_date = date.today().strftime("%Y-%m-%d")


papers, _ = get_daily_papers_hf(search_date=search_date)
_sucess = send_daily_paper_notion(papers)

print(f"\n{_sucess} papers added to daily_paper@Jo's Notion.")


