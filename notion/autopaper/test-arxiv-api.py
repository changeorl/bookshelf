#######################################
#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @author: chenzh05
# @Desc: { arxiv api implementation }
# @Date: 2023/08/09 10:00
#######################################
# general usage: https://info.arxiv.org/help/api/user-manual.html#2-api-quickstart
# category lookup table: https://arxiv.org/category_taxonomy
# search_query lookup table: https://info.arxiv.org/help/api/user-manual.html#query_details

import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime


def print_aligned_dict(input_dict):
    max_key_length = max(len(key) for key in input_dict.keys()) + 1
    for key, value in input_dict.items():
        key += ":"
        formatted_key = f"{key:{max_key_length}}"
        print(f"{formatted_key} {value}")


def search_by_id(arxiv_id=None):
    if not arxiv_id:
        arxiv_id = input("Enter arXiv ID: ")

    # arxiv_id = "2308.02669"
    url = "http://export.arxiv.org/api/query"
    try:
        response = requests.get(url, params={"id_list": arxiv_id})
        response.raise_for_status()
    except Exception as e:
        print(e)
        return

    soup = BeautifulSoup(response.content, "xml").entry
    paper = {}  # ArxivPaper(arxiv_id)

    published = soup.published.text
    published = datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ")
    published = published.date().strftime("%Y-%m-%d")
    paper["published"] = published

    paper["arxiv_id"] = arxiv_id
    paper["link"] = f"http://arxiv.org/abs/{arxiv_id}"
    paper["pdf"] = f"http://arxiv.org/pdf/{arxiv_id}"
    paper["category"] = soup.category["term"]
    paper["title"] = soup.title.text
    paper["authors"] = [a.find("name").text for a in soup.find_all("author")]
    paper["summary"] = soup.summary.text.strip()

    print_aligned_dict(paper)
    return paper


paper = search_by_id()


# title = "bert"
# max_results = 20

# url = "http://export.arxiv.org/api/query"
# params = {"search_query": f"ti:{title}", "start": 0, "max_results": max_results}
# response = requests.get(url, params=params)
# response.raise_for_status()
# soup = BeautifulSoup(response.content, "xml")
# print(soup)
