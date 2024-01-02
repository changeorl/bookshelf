import requests
import csv
import time

from typing import List, Dict,Optional,Literal
from bs4 import BeautifulSoup
from pathlib import Path
from dataclasses import dataclass
from tqdm.auto import tqdm

@dataclass
class JosBook:
    """A book class for Jo
    
    Attributes:
        title (str): 
            title of the book

        douban_title (Optional[str], optional):
            douban title of the book. Defaults to None.

        sub_title (Optional[str], optional):
            sub title of the book. Defaults to None.

        author (Optional[str], optional):
            author of the book. Defaults to None.

        publication (Optional[str], optional):
            publication of the book. Defaults to None.

        ibsn (Optional[str], optional):
            ibsn of the book. Defaults to None.

        douban_id (Optional[str], optional):
            douban id of the book. Defaults to None.

        douban_rating (Optional[str], optional):
            douban rating of the book. Defaults to None.

        cover_url (Optional[str], optional):
            cover url of the book. Defaults to None.

        device (Optional[Literal['epub','ibook','pdf','paper']], optional):
            device of the book. Defaults to None.
        """
    title: str
    douban_title: Optional[str] = None
    sub_title: Optional[str] = None
    author: Optional[str]  = None
    publication: Optional[str] = None
    ibsn: Optional[str] = None
    douban_id: Optional[str] = None
    douban_rating: Optional[str] = None
    cover_url: Optional[str]  = None
    # douban_url: Optional[str]  = None
    # amazon_url: Optional[str]  = None
    device: Optional[Literal['epub','ibook','pdf','paper']]  = None

    def aprint(self):
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
        input_dict = self.__dict__
        max_key_length = max(len(key) for key in input_dict.keys())
        for key, value in input_dict.items():
            key += ":"
            if value:
                formatted_key = f"{key:{max_key_length+1}}"
                print(f"{formatted_key} {value}")


def get_douban_info_by_id(dbid: str, title: str) -> JosBook:
    """Get book info from douban by douban id
    
    Args:
        dbid (str): douban id of the book
        
    Returns:
        JosBook: A JosBook instance
    """

    book = JosBook(title,douban_id=dbid)

    url= 'https://book.douban.com/subject/{}/'.format(dbid)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',}
    r=requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    douban_title = soup.find('h1').find('span').text
    book.douban_title = douban_title

    info_div = [ i.text.strip() for i in soup.find('div',{'id':'info'}) if i.text.strip() != '' ]
    def get_meta_by_key(key, l:List[str] = info_div) -> Optional[str]:
        return next((l[i+1] for i in range(len(l)) if l[i] == key), None)
    book.sub_title = get_meta_by_key("副标题:")
    book.publication = get_meta_by_key("出版社:")

    book.author =  ''.join([c for c in info_div[0].split(':')[-1].strip() if c != '\n' and c != ' ' ])
    book.ibsn = info_div[-1].split(':')[-1].strip()

    rate = soup.find('strong').text.strip()
    book.douban_rating = rate if rate!='' else None

    book.cover_url= soup.find('a',{'class':'nbg'}).get('href')
    # book.douban_url= url

    return book


def read_local_datastore(in_file: str='asserts/datastore.csv') -> List[JosBook]:
    """
    Read datastore.csv and return a list of dict

    The file should be a csv file with the following columns:
        title, device, douban_id, cover_url
    The last column is optional, can be empty but a comma is required.
    For example:
        Working Backwards,epub ibook,35363202,
        Your Money or Your Life,epub ibook,1342400,https://m.media-amazon.com/images/I/71AL7FJJw3L._SL1500_.jpg
            
    Args:
        in_file (str, optional): 
            Defaults to 'asserts/datastore.csv' if not provided.

    Returns:
        List[JosBook]: 
            A list of JosBook instances, of which only contains the following attributes:
                title, device, douban_id, cover_url.
    """
    with open(in_file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        books = [[col if col != '' else None for col in row] for row in spamreader]
    
    cols, infos = books[0], books[1:]
    return [JosBook(**dict(zip(cols,b))) for b in infos]


s_i = 1
books = read_local_datastore()
books.insert(0,books[0].__dict__.keys())
for i,b in enumerate(tqdm(books[s_i-1:], desc="", unit="book"), s_i):
    with open('asserts/datastore_douban.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        if i == 1:
            spamwriter.writerow(b)
            tqdm.write(f"{i} {','.join(b)}")
        else:
            mark = '✔️' if b.douban_id else '❌'
            if not b.douban_id:
                d_book = b
            else:
                d_book = get_douban_info_by_id(b.douban_id, b.title)
                d_book.device = b.device
                d_book.cover_url = b.cover_url if b.cover_url else d_book.cover_url

            spamwriter.writerow(d_book.__dict__.values())
            tqdm.write(f"{mark} {i} {d_book.title}")

