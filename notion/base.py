import requests
import sys


from utils import *

"""
Base class for Notion APIs
"""


class NotionBaseApi:
    def __init__(self) -> None:
        self.endpoint = "https://api.notion.com/v1"
        self.token = "secret_s6zhSzRMCv1s9zf9rwPLbd6SVc5H9656QCGyWgd4s1F"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }
        self.workspace_name = "Jo's Notion"

    def post(self, route, payload: dict = None, **kwargs):
        """
        POST request to Notion API
        :param route: API route
        :param payload: API request body
        :return: response
        """
        url = self.endpoint + route
        response = requests.post(url, json=payload, headers=self.headers)
        return response

    def get(self, route, payload: dict = None, **kwargs):
        """
        GET request to Notion API
        :param route: API route
        :param payload: API request body
        :return: response
        """
        url = self.endpoint + route
        response = requests.get(url, json=payload, headers=self.headers)
        return response


"""
Database APIs
"""


class DatabaseApi(NotionBaseApi):
    def retrieve(self, database_id):
        """
        Retireve a database from notion with database_id
        """
        route = f"/databases/{database_id}/"
        response = self.get(route)
        response.raise_for_status()
        return response.json()
