import requests
from bs4 import BeautifulSoup
import json
from settings import *
from utils import api_debug

def crawler(book_id):
    content = dict()

    #book_id = '36104531'
    url= 'https://book.douban.com/subject/{}/'.format(book_id)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',}

    r=requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    l = [ i.text.strip() for i in soup.find('div',{'id':'info'}) if i.text.strip() != '' ]

    content['title'] = soup.find('h1').find('span').text

    content['sub_title'] = ''
    for i in range(len(l)):
        if l[i] == '副标题:':
            content['sub_title'] = l[i+1]

    content['author'] = ''.join([c for c in l[0].split(':')[-1].strip() if c != '\n' and c != ' ' ])

    content['publication'] = l[2]
    
    try :
        rate = soup.find('strong').text.strip()
        num_rate = soup.find_all('a',{'class':'rating_people'})[0].span.text
        content['rating'] = rate + ' by ' + num_rate
    except: content['rating'] = ' '
    
    content['ISBN'] = l[-1].split(':')[-1].strip()
    
    content['DBID'] = book_id
    
    content['img_url'] = soup.find('a',{'class':'nbg'}).get('href')
        
    return content

def notion_helper(book):
    
    secret = INFO.token
    database = DATABASE.book

    url = 'https://api.notion.com/v1/pages'

    # Headers
    headers = {
        'Authorization': f'Bearer {secret}',
        'Content-Type': 'application/json',
        'Notion-Version': '2021-08-16'
    }

    #book = crawler(book_id)

    # Data input
    data_input = {
        "parent": { "database_id": f"{database}" },

        'properties':{

          #'我是number（这里对应你database的属性名称）':{'type': 'number', 'number': int(数据)},
          #'我是title':{
          #      'id': 'title', 'type': 'title', 
          #      'title': [{'type': 'text', 'text': {'content': str(数据)}, 'plain_text': str(数据)}]
          #  },
          #'我是select': {'type': 'select', 'select': {'name': str(数据)}},
          #'我是date': {'type': 'date', 'date': {'start': str(数据), 'end': None}},
          #'我是Text': {'type': 'rich_text', 'rich_text': [{'type': 'text', 'text': {'content': str(数据)},  'plain_text': str(数据)}]},
          #'我是multi_select': {'type': 'multi_select', 'multi_select': [{'name': str(数据)}, {'name': str(数据)}]}
          #'我是checkbox':{'type': 'checkbox', 'checkbox': bool(数据)}
            'title':{
                'id': 'title', 'type': 'title', 
                'title': [{'type': 'text', 'text': {'content': book['title']}}]
            },
            'sub_title': {'type': 'rich_text', 'rich_text': [{'type': 'text', 'text': {'content': book['sub_title']}}]},
            'author': {'type': 'rich_text', 'rich_text': [{'type': 'text', 'text': {'content': book['author']}}]},
            'publication': {'type': 'rich_text', 'rich_text': [{'type': 'text', 'text': {'content': book['publication']}}]},
            'rating': {'type': 'rich_text', 'rich_text': [{'type': 'text', 'text': {'content': book['rating']}}]},
            'DBID':{'type': 'number', 'number': int(book['DBID'])},
            'ISBN':{'type': 'number', 'number': int(book['ISBN'])},
            'cover': {'files': [{'type': 'external', 'name': 'cover', 'external': {'url': book['img_url']}}]},
        }
    }
    

    # check request 
    response = requests.post(url, headers=headers, json=data_input)
    print('{} has been added to you Notion library!'.format(book['title']))
    
    
if __name__ == '__main__':
    book_id = 1
    names = list()
    books = list()
    
    while (book_id):
        print('-----------------------------')
        book_id = int(input('book id or 0 for quit：\n'))

        if book_id: 
            content = crawler(book_id)
            books.append(content)
            names.append(content['title'])
            notion_helper(content)

    print('-----------------------------')
    print(names,len(names), 'books were added to the database.')