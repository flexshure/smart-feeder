from dataclasses import dataclass
from typing import Union


@dataclass
class ApiTokenAuth:
    __type = 'apiToken'
    api_token: Union[str, list[str]]


@dataclass
class PasswordAuth:
    __type = 'password'
    user_name: str
    password: str


@dataclass
class OAuthTokenAuth:
    __type = 'oAuthToken'
    oauth_token: str


DiscriminatedAuth = Union[ApiTokenAuth, PasswordAuth, OAuthTokenAuth]


@dataclass
class BasicAuth:
    user_name: str
    password: str
