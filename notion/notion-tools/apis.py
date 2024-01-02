import requests
from settings import *
from utils import api_debug
import pandas as pd


def notion_api(method, route, headers=None, data=None):
    """
    General API call template to notion
    """
    url = INFO.endpoint + route
    if not headers:
        headers = {
            "Authorization": f"Bearer {INFO.token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }
    response = requests.request(method, url, headers=headers, json=data)
    return response


def get_database(id: str):
    """
    Retireve a database from notion with database_id
    """
    method = "POST"
    route = f"/databases/{id}/query"
    response = notion_api(method=method, route=route)
    response.raise_for_status()
    return response


def insert_database(row_data: dict):
    """
    Insert a row into a database with database_id, and row data

    The following database properties cannot be updated via the API:
    - formula
    - select
    - status
    - Synced content
    - A multi_select database property's options values. An option can be removed, but not updated.
    """
    method = "POST"
    route = f"/pages"
    # data = {"parent": {"database_id": databaseID}, 
    #         "cover": {"external": {"url": coverURL}},
    #         "properties": properties}
    response = notion_api(method=method, route=route, data=row_data)
    # api_debug(response,0,0,1,0)
    response.raise_for_status()
    return response

def get_page(id: str):
    """
    Retireve a page from notion with page_id
    """
    method = "GET"
    route = f"/pages/{id}"
    response = notion_api(method=method, route=route)
    response.raise_for_status()
    return response


def get_block(id: str):
    """
    Retireve a block from notion with block_id
    """
    method = "GET"
    route = f"/blocks/{id}"
    response = notion_api(method=method, route=route)
    response.raise_for_status()
    return response