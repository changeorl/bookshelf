import requests
import json
import csv

from typing import Optional, Dict

from config import NotionConfig
from client_abstract import (
    Database,
    Page,
    User,
    QueryResult,
)


def jprint(dict):
    print(json.dumps(dict, indent=4, ensure_ascii=False))


class NotionApi:
    """Notion API Client

    Attributes:
        endpoint (str):
            Notion API endpoint
        access_token (str):
            Notion API token
        workspace_name (str):
            Notion workspace name
        headers (dict):
            Notion API headers
    """

    def __init__(self, token: Optional[str] = None, workspace: Optional[str] = None):
        """Initialize the Notion API Client

        Args:
            token (Optional[str], optional):
                Notion API token. Defaults to None.
            workspace (Optional[str], optional):
                Notion workspace name. Defaults to None.
        """

        self.endpoint = "https://api.notion.com/v1"
        self.access_token = token if token else NotionConfig.token
        self.workspace_name = workspace if workspace else NotionConfig.workspace_name
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }

    def _make_request(
        self,
        method: str,
        route: str,
        json: dict = None,
        params: dict = None,
        error_handler: bool = False,
        **kwargs,
    ):
        """Execute the request method of the Session object

        Args:
            method (str):
                HTTP Method passed to the session object
                [ GET, POST, PUT, PATCH, DELETE ]
            route (str):
                Sub-route of the API endpoint, this is NOT a full address of url.
            json (dict, optional):
                API Body if required. Defaults to None.
            params (dict, optional):
                API parameters to be wrapped in url. Defaults to None.

        Returns:
            requests.Response:
                http response return by the API endpoint

        Raises:
            requests.HTTPError:
                errors raised by `requests.raise_for_status()`
        """
        url = self.endpoint + route
        results = requests.request(
            method,
            url,
            headers=self.headers,
            json=json,
            params=params,
            **kwargs,
        )

        if results.ok:
            return results

        results.raise_for_status()

    def list_all_users(self):
        """
        List all users
        """
        method = "GET"
        route = "/users"
        r = self._make_request(method=method, route=route)
        return r.json()

    def retrieve_a_user(self, user_id: str):
        """
        Retrieve a user
        """
        method = "GET"
        route = f"/users/{user_id}"
        r = self._make_request(method=method, route=route)
        return User(**r.json())

    def database_retireve(self, database_id):
        """Retireve a database from notion with database_id

        Args:
            database_id ([type]): [description]
        """
        method = "GET"
        route = f"/databases/{database_id}"
        r = self._make_request(method=method, route=route)
        return Database(**r.json())

    def query_a_database(self, database_id: str, fileter: Dict = None):
        """
        Query a database
        """
        method = "POST"
        route = f"/databases/{database_id}/query"
        r = self._make_request(method=method, route=route, json=fileter)
        data = r.json()
        pages = [Page(**i) for i in data["results"]]
        data["results"] = pages
        return QueryResult(**data)

    def page_create(
        self,
        parent,
        properties,
        children=None,
        icon=None,
        cover=None,
    ):
        """
        create a new page attached either to a page or a database
        """
        method = "POST"
        route = f"/pages"
        data = dict(
            parent=parent,
            properties=properties,
            children=children,
            icon=icon,
            cover=cover,
        )
        r = self._make_request(method=method, route=route, json=data)
        return Page(**r.json())

    def page_retrieve(self, page_id: str):
        """
        Get a page
        """
        method = "GET"
        route = f"/pages/{page_id}"
        r = self._make_request(method=method, route=route)
        return Page(**r.json())


def show_abstract(r: requests.Response):
    with open("api_response.json", "w") as f:
        json.dump(r.json(), f, indent=4, ensure_ascii=False)

    for i in r.json().keys():
        print(f"{i}:Dict")
    print(len(r.json().keys()))


sess = NotionApi()

filter = {
    "filter": {
        "property": "cover localized",
        "checkbox": {"equals": False},
    },
    "sorts": [{"property": "title", "direction": "ascending"}],
}
r = sess.query_a_database(NotionConfig.db_bookshelf, filter)
# show_abstract(r)
# print(len(r.json()["results"]))
# jprint(r.__dict__)

with open("no_cover.csv", "a", newline="") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=",")
    for p in r.results:
        try:
            tilte = p.properties["title"]["title"][0]["plain_text"]
            cover_url = p.properties["cover_url"]["files"][0]["external"]["url"]
            spamwriter.writerow([tilte, cover_url])
            print(f"✔️ {tilte}")
        except:
            print(f"❌ {tilte}")
            continue
