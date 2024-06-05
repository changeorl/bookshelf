#######################################
# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @author: chenzh05
# @Desc: { notion api implementation }
# @Date: 2023/08/09 15:29
#######################################
# notion-api: https://developers.notion.com/reference/intro

import json
import requests

def jprint(dict):
    print(json.dumps(dict, indent=4, ensure_ascii=False))

class Config:
    token = "secret_s6zhSzRMCv1s9zf9rwPLbd6SVc5H9656QCGyWgd4s1F"
    endpoint = "https://api.notion.com/v1"
    user_id = "5b02b983-2356-4012-b7ff-bea7da21ef08"
    workspace_name = "Jo's Notion"

    db_inbox = "48de1468a76942dc9c93128fc56babb1"
    db_daily_paper = "08a9b64c5d344a72967cd3bfdf8f8368"
    db_book = "61abd05763c84033a98f577e7e92ad16"
    db_test = "e04e534cad4a44c5b1c0c11f869f0197"
    db_fleeto = "5bc1dbd4865244dc9149722c9ab999af"
    db_bookshelf = "87aa9c79d3944c57ad7a7ffb97eb9ade"

def notion_api(method, route, headers=None, json=None):
    """
    General API call template to notion
    """
    url = Config.endpoint + route
    if not headers:
        headers = {
            "Authorization": f"Bearer {Config.token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }
    response = requests.request(method, url, headers=headers, json=json)
    return response


def database_retireve(database_id):
    """
    Retireve a database from notion with database_id
    """
    method = "GET"
    route = f"/databases/{database_id}"
    response = notion_api(method=method, route=route)
    response.raise_for_status()
    return response


def database_query(database_id):
    """
    Query a database from notion with database_id
    """
    method = "POST"
    route = f"/databases/{database_id}/query"
    response = notion_api(method=method, route=route)
    response.raise_for_status()
    return response


def database_update(database_id, parent=None, properties=None, children=None, icon=None, cover=None):
    method = "PATCH"
    route = f"/databases/{database_id}"
    data = dict()
    if parent:
        data["parent"] = parent
    if properties:
        data["properties"] = properties
    if children:
        data["children"] = children
    if icon:
        data["icon"] = icon
    if cover:
        data["cover"] = cover
    if data == {}:
        print("no data to update")
        exit()
    response = notion_api(method=method, route=route, json=data)
    # response.raise_for_status()
    return response


def page_create(parent, properties, children=None, icon=None, cover=None):
    """
    create a new page attached either to a page or a database
    """
    method = "POST"
    route = f"/pages"
    data = {
        "parent": parent,
        "properties": properties,
        "children": children,
        "icon": icon,
        "cover": cover,
    }
    response = notion_api(method=method, route=route, json=data)
    # response.raise_for_status()
    return response


def page_retrieve(page_id: str):
    """
    Get a page
    """
    method = "GET"
    route = f"/pages/{page_id}"
    response = notion_api(method=method, route=route)
    response.raise_for_status()
    return response
