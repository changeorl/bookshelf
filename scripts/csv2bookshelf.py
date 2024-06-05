from typing import List, Optional
from db2csv import read_local_datastore, JosBook
import csv


def create_page_properties(
    ibsn: Optional[str],
    source: Optional[List],
):
    epub = {
        "id": "c8099942-3c2a-4df2-96f5-19be8bf14339",
        "name": "epub",
        "color": "orange",
    }
    ibook = {
        "id": "d61f095c-3600-4ec1-bf35-a630b8543540",
        "name": "ibook",
        "color": "gray",
    }

    return {
        "ibsn": {"id": "%3Cki~", "type": "number", "number": ibsn},
        "source": {
            "id": "IZdP",
            "type": "multi_select",
            "multi_select": [
                {
                    "id": "c8099942-3c2a-4df2-96f5-19be8bf14339",
                    "name": "epub",
                    "color": "orange",
                },
                {
                    "id": "d61f095c-3600-4ec1-bf35-a630b8543540",
                    "name": "ibook",
                    "color": "gray",
                },
            ],
        },
        "author": {
            "id": "W%7CQm",
            "type": "rich_text",
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": "qwewq", "link": None},
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default",
                    },
                    "plain_text": "qwewq",
                    "href": None,
                }
            ],
        },
        "tags": {"id": "%5C%5BOS", "type": "multi_select", "multi_select": []},
        "publication": {
            "id": "aCh%3C",
            "type": "rich_text",
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": "qweqweq", "link": None},
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default",
                    },
                    "plain_text": "qweqweq",
                    "href": None,
                }
            ],
        },
        "douban_rating": {"id": "gxzW", "type": "number", "number": 8.7},
        "douban_id": {"id": "l%5CSW", "type": "number", "number": 1231313},
        "Status": {
            "id": "uxY%7C",
            "type": "status",
            "status": {
                "id": "1d000ce4-cf2e-48aa-8a21-7304335adcd3",
                "name": "Not started",
                "color": "default",
            },
        },
        "cover_url": {
            "id": "%7B%5CTQ",
            "type": "files",
            "files": [
                {
                    "name": "https://img3.doubanio.com/view/subject/l/public/s31284757.jpg",
                    "type": "external",
                    "external": {
                        "url": "https://img3.doubanio.com/view/subject/l/public/s31284757.jpg"
                    },
                }
            ],
        },
        "sub_title": {
            "id": "%7C_zi",
            "type": "rich_text",
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": "2213", "link": None},
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default",
                    },
                    "plain_text": "2213",
                    "href": None,
                }
            ],
        },
        "title": {
            "id": "title",
            "type": "title",
            "title": [
                {
                    "type": "text",
                    "text": {"content": "weq ", "link": None},
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default",
                    },
                    "plain_text": "weq ",
                    "href": None,
                }
            ],
        },
    }


with open("asserts/datastore_douban.csv", newline="") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=",", quotechar="|")
    books = [row for row in spamreader]

cols, infos = books[0], books[1:]

for i, b in enumerate(infos, 2):
    if i == 15:
        print(b)

        for k in cols:
            print(k, b[cols.index(k)])
        # print(i, b)
        print()
        print(dict(zip(cols, b)))
        break
