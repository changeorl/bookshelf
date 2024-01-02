import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
from settings import *

domain = "https://arxiv.org"

url = "https://arxiv.org/abs/1706.03762"  #'https://arxiv.org/abs/1810.04805'
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")
title = soup.find("h1", {"class": "title mathjax"}).text.split("Title:")[-1]
# link = domain + soup.find('a', {'class' : 'abs-button download-pdf'})['href']
link = f"https://arxiv.org/pdf/{url.split('/')[-1]}"
