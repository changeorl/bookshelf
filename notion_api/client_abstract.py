from typing import *
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class User:
    object: Literal["user"]
    id: str
    type: Optional[str]
    name: Optional[str]
    avatar_url: Optional[str]
    person: Optional[Dict]
    request_id: str = None


@dataclass
class Database:
    object: Literal["database"]
    id: str
    created_time: str
    created_by: User
    last_edited_time: str
    last_edited_by: User
    title: List[Dict]
    description: List[Dict]
    icon: Dict
    cover: Dict
    properties: Dict
    parent: Dict
    url: str
    archived: bool
    is_inline: bool
    public_url: str
    request_id: str = None


@dataclass
class Page:
    object: Literal["page"]
    id: str
    created_time: str
    created_by: User
    last_edited_time: str
    last_edited_by: User
    archived: Dict
    icon: Dict
    cover: Dict
    properties: Dict
    parent: Dict
    url: Dict
    public_url: str
    request_id: str = None


@dataclass
class QueryResult:
    object: Literal["list"]
    results: List[Page]
    next_cursor: Optional[str]
    has_more: bool
    type: str
    page_or_database: Dict
    request_id: str = None
