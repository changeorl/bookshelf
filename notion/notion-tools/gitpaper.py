"""
python autopaper.py -d 0705
python autopaper.py
"""
from lxml import etree
import requests
from bs4 import BeautifulSoup
from datetime import datetime,date
import json
from apis import insert_database, get_database
from settings import *
import time
import argparse
from utils import api_debug


hf_domain = 'https://huggingface.co/papers/'
pdf_domain = 'https://arxiv.org/pdf/'
arxiv_domain = 'https://arxiv.org/abs/'
default_cover = 'https://info.arxiv.org/brand/images/brand-logo-primary.jpg'
target_db, target_db_name  = DATABASE.gitpaper, 'gitpaper'

class ArxivPaper(object):
    def __init__(self, 
                 arxivID: str,
                 cover: str = None,
                 media: str = None,
                 field: str = None,
                 title: str = None,
                 authors: list = None,
                 desc: str = None,
                 submission: str = None):
        
        self.arxivID = arxivID
        self.pdf_url = f'{pdf_domain}{arxivID}.pdf'
        self.arxiv_url = f'{arxiv_domain}{arxivID}'
        self.cover = cover
        self.media = media
        self.field = field
        self.title = title
        self.authors = authors
        self.desc = desc
        self.submission = submission

    def get_arxiv_paper(self, verbose: bool = True):
        response = requests.get(self.arxiv_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        field = soup.find_all('div', class_='subheader')[0].text
        field = field.split('>')[-1].strip()

        title = soup.find_all('h1', class_='title mathjax')[0].text
        title = title.replace('Title:','').strip()
        
        authors = soup.find_all('div', class_= 'authors')[0].find_all('a')
        authors = [a.text for a in authors]

        desc = soup.find_all('blockquote', class_= 'abstract mathjax')[0].text
        desc = desc.split('Abstract:')[-1].strip()
        
        submission = soup.find_all('div', class_= 'submission-history')[0].text.strip()
        submission = submission.split("\n")[4]
        submission = submission.split('(')[0].strip()
        submission_obj = datetime.strptime(submission, "%a, %d %b %Y %H:%M:%S %Z")
        submission = submission_obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        self.field = field
        self.title = title
        self.authors = authors
        self.desc = desc
        self.submission = submission

        if verbose:
            print(f'Successfully crawled arXiv - {self.arxivID}, {title}')

def get_daily_papers_hf(search_date: str, cache: bool = True):
    #https://huggingface.co/papers?date=2023-07-06

    url = f'{hf_domain}?date={search_date}'

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    timestamp = soup.find_all('time')[0]['datetime']    
    datetime_obj = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    print(f'{datetime_obj.strftime("%A, %B %d, %Y")}\n')
    print('crawling from huggingface...\n')
    if datetime.strptime(search_date, "%Y-%m-%d").date() != datetime_obj.date():
        print(f'nothing published on {search_date}')
        exit()

    papers = list()
    articles = soup.find_all('article')
    for index, article in enumerate(articles, 1):
        arxivID = [a for a in article.find_all('a') if a['href'].startswith('/papers/')]
        arxivID = arxivID[0]['href'].split('/')[-1]
        paper = ArxivPaper(arxivID=arxivID)
        try:
            vedio = article.find_all('video')[0]['src']
            paper.media = vedio
        except:
            img = article.find_all('img')[0]['src']
            paper.cover = img

        paper.get_arxiv_paper(verbose=False)
        papers.append(paper)
        print(f'{index} - {paper.arxivID}, {paper.title}')
        

    if cache:
        cacheID = datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
        filename = f'daily-paper/.cache/{cacheID}.json'
        with open(filename, 'w') as json_file:
            data = [p.__dict__ for p in papers]
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        return papers,filename
    
    return papers, "No cache"

def send_daily_paper_notion(papers: list):
    print("\nsending to Notion...\n")

    _exist = list()
    response = get_database(target_db)
    for paper in response.json()['results']:
        _exist = [i for i in response.json()['results']]
        _exist = [i['properties']['arxivID']['rich_text'][0]['text']['content'] for i in _exist]

    # print(f'existing papers: {_exist}')
    _sucess = 0
    for index, paper in enumerate(papers, 1):

        if paper.arxivID in _exist:
            print(f'{index} Already existed - {paper.title}')
            continue

        properties = {
            "title": {
                "id": "title",
                "type": "title",
                "title": [{'type': 'text', 'text': {'content': paper.title}}]
            },
            "arxivID": {
                "id": "hqID",
                "type": "rich_text",
                "rich_text": [{'type': 'text', 'text': {'content': paper.arxivID}}]
            },
            "arxivURL": {
                "id": "EWzs",
                "type": "url",
                "url": paper.arxiv_url
            },
            "pdf": {
                "id": "dzux",
                "type": "url",
                "url": paper.pdf_url
            },
            "field": {
                "id": "s%3C%3Fc",
                "type": "select",
                "select": {
                    "name": paper.field,
                }
            },
            "published": {
                "id": "TGX~",
                "type": "date",
                "date": {
                    "start": paper.submission,
                    "end": None,
                    "time_zone": None
                }
            }
        }
        children = [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": ', '.join(paper.authors)},
                        "annotations": {
                            "bold": True,
                            "italic": True,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "blue"
                        },
                    }],
                }
            },
            {
                "object": "block",
                "type": "quote",
                "quote": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": paper.desc}
                    }],
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [],
                }
            },
        ]
        if paper.media:
            children.append(
                {
                    "object": "block",
                    "type": "video",
                    "video": {
                        "caption": [],
                        "type": "external",
                        "external": {
                            "url": paper.media
                        }
                    }
                }
            )
        if paper.cover:
            children.append(
                {
                    "object": "block",
                    "type": "image",
                    "image": {
                        "caption": [],
                        "type": "external",
                        "external": {
                            "url": paper.cover
                        }
                    }
                }
            )
        
        row_data = {"parent": {"database_id": target_db}, 
                    "properties": properties,
                    "children": children}
        
        response = insert_database(row_data)
        if response.ok:
            print(f'{index} Successfully added - {paper.title}')
            _sucess+=1
            time.sleep(1)
        else:
            print(f'{index} Failed to send - {paper.title}')
            time.sleep(1)
            continue
    
    return _sucess

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send daily paper to Notion.')
    parser.add_argument('-d','--date', default=None, help='date in format of MMDD')
    parser.add_argument('-a','--arxivID', default=None, help='arxivID in format of 2307.09112')
    args, unknown = parser.parse_known_args()
    _date, _arxivID = args.date, args.arxivID

    if not _arxivID:
        if _date:
            search_date = f"2023-{_date[:2]}-{_date[2:]}"
            # print(search_date)
            if datetime.strptime(search_date, "%Y-%m-%d").date() > date.today():
                print(f'\n{search_date} is a future date.')
                exit()
        else:
            search_date = date.today().strftime("%Y-%m-%d")

        papers, cachefile = get_daily_papers_hf(search_date=search_date, cache=True)
        print(f"\n{len(papers)} papers crawled, cache@{cachefile}")

    else:
        print('')
        papers = list()
        for aID in _arxivID.split(' '):
            paper = ArxivPaper(arxivID=aID)
            paper.get_arxiv_paper()
            papers.append(paper)
            print(json.dumps(paper.__dict__, indent=4))
    _sucess = send_daily_paper_notion(papers)
    print(f"\n{_sucess} papers added to {target_db_name}@Jo's Notion.")

# s = """
# | 1 | 2 |
# | - | - |
# | a | b |
# """
# filename = 'test-readme.md'


# with open('test-readme.md', 'w') as f:
#     f.write(s)
