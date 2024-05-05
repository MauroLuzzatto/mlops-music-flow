from typing import Any, List, Optional

from pydantic import BaseModel


class ExternalUrls(BaseModel):
    spotify: str


class Followers(BaseModel):
    href: Any
    total: int


class Image(BaseModel):
    height: int
    url: str
    width: int


class Model(BaseModel):
    external_urls: ExternalUrls
    followers: Followers
    genres: List[str]
    href: str
    id: str
    images: List[Image]
    name: str
    popularity: int
    type: str
    uri: str
