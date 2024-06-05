import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path
import json
import execjs
import re

def aprint(input_dict: dict, colon=False):
    """
    print a dict in aligned format

    :param input_dict: dict to be printed
    :param colon: aligned colon or not
    :return: None

    e.g.
    >>> aprint({"a": 1, "bb": 2, "ccc": 3})
    a:   1
    bb:  2
    ccc: 3
    """
    max_key_length = max(len(key) for key in input_dict.keys())
    for key, value in input_dict.items():
        if not colon:
            key += ":"
            formatted_key = f"{key:{max_key_length+1}}"
            print(f"{formatted_key} {value}")
        else:
            formatted_key = f"{key:{max_key_length}}"
            print(f"{formatted_key}: {value}")

def jprint(input_dict: dict, indent: int = 4):
    """
    print a dict in json format

    :param input_dict: dict to be printed
    :param indent: indent of json format
    :return: None

    e.g.
    >>> jprint({"a": 1, "bb": 2, "ccc": 3})
    {
        "a": 1,
        "bb": 2,
        "ccc": 3
    }
    """
    print(json.dumps(input_dict, indent=4, ensure_ascii=False))

def read_save_books():
    with open('epub_sorted.txt', 'r') as f:
        epub = f.read().splitlines()
    print(f"epub: {len(epub)}")

    with open('ibook_sorted.txt', 'r') as f:
        ibook = f.read().splitlines()
    print(f"ibook: {len(ibook)}")

    with open('wanted.txt', 'r') as f:
        wanted = f.read().splitlines()
    print(f"wanted: {len(wanted)}")

    with open('books.txt', 'r') as f:
        books = f.read().splitlines()
    print(f"books: {len(books)}")

    books_sorted = list() #sorted(list(set(epub + ibook + wanted)))
    for i in books:
        title = i.split('@')[0]
        douban_id = i.split('@')[-1] if len(i.split('@')) > 1 else '@'
        is_epub, is_ibook = '', ''
        if title in epub:
            epub.pop(epub.index(title))
            is_epub = 'epub'
        if title in ibook:
            ibook.pop(ibook.index(title))
            is_ibook = 'ibook'

        b = dict()
        b['title'] = title
        b['catlog'] = is_epub + ' '+is_ibook
        b['douban_id'] = douban_id
        books_sorted.append(b)

    with open('books_sorted.txt', 'w') as f:
        for i,b in enumerate(books_sorted,1):
            print(f"{i:03d} {b['title']},{b['catlog']},{b['douban_id']}")
            f.write(f"{b['title']},{b['catlog']},{b['douban_id']}\n")


    with open('books_sorted.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['title', 'device', 'douban_id'])
        for i,b in enumerate(books_sorted,1):
            spamwriter.writerow([b['title'],b['catlog'],b['douban_id']])

    return books_sorted

def get_douban_by_id(dbid):
    content = dict()

    #book_id = '36104531'
    url= 'https://book.douban.com/subject/{}/'.format(dbid)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',}

    r=requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    l = [ i.text.strip() for i in soup.find('div',{'id':'info'}) if i.text.strip() != '' ]

    content['title'] = soup.find('h1').find('span').text

    content['sub_title'] = None
    for i in range(len(l)):
        if l[i] == '副标题:':
            content['sub_title'] = l[i+1]

    content['author'] = ''.join([c for c in l[0].split(':')[-1].strip() if c != '\n' and c != ' ' ])

    content['publication'] = l[2]
    
    try :
        rate = soup.find('strong').text.strip()
        # num_rate = soup.find_all('a',{'class':'rating_people'})[0].span.text
        content['rating'] = rate #+ ' by ' + num_rate
    except: content['rating'] = None
    
    content['ISBN'] = l[-1].split(':')[-1].strip()
    
    content['DBID'] = dbid
    
    content['cover_url'] = soup.find('a',{'class':'nbg'}).get('href')
        
    return content

def create_book_csv(start=1, in_file='books_sorted.csv',out_file='books_info.csv'):
    
    header = ['title', 'sub_title', 'author', 'publication', 'rating', 'ISBN', 'DBID', 'cover_url','db_title','device']
    with open(out_file, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(header)

    with open(in_file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        books = [row for row in spamreader]
    
    for i,b in enumerate(books[start:],start):
        title = b[0]
        device = [i for i in b[1].split(' ') if i != '']
        dbid = b[2] if b[2] != '@' else None
        cover_url = b[3] if b[3] else None
        print(f"\n{i:03d} {title} {device} {dbid} {cover_url}")

        if dbid:
            book_info = get_douban_by_id(dbid)
            if cover_url:
                book_info['cover_url'] = cover_url
            temp = book_info['title']
            book_info['title'] = title
            book_info['db_title'] = temp
            book_info['device'] = ';'.join(device)
        else:
            # dict_keys(['title', 'sub_title', 'author', 'publication', 'rating', 'ISBN', 'DBID', 'cover_url'])
            book_info = dict(
                title = title,
                db_title = None,
                sub_title = None,
                author = None,
                publication = None,
                rating = None,
                ISBN = None,
                DBID = dbid,
                cover_url = cover_url,
                device = ';'.join(device),
            )
        
        aprint(book_info)

        with open(out_file, 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
                                    #,quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(list(book_info.values()))
        
        print(f"✔️ {book_info['title']}")


# create_book_csv(start=1,out_file='books_info2.csv')