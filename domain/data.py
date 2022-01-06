from dataclasses import dataclass
from common.player_types import PlayerType
from typing import List


@dataclass
class Player:
    player_id: int = None
    first_name: str = ""
    last_name: str = ""
    age: int = None
    country: str = "India"
    market_value: any = 1000000
    player_type: PlayerType = None
    team_id: int = None
    player_url: str = None


@dataclass
class Team:
    team_id: int = None
    team_name: str = ""
    country: str = "India"
    account_id: int = None
    available_cash: any = 5000000
    players: List[Player] = None
    team_value: int = None


@dataclass
class User:
    user_id: int = None
    username: str = ""
    team: Team = None


@dataclass
class UserData(User):
    password: str = ""


@dataclass
class Transfer:
    transfer_id: int = None
    ask_price: int = None
    transferred: bool = False
    player_name: str = None
    player_id: int = None
    transferred_from: int = None
    transferred_to: int = None
    transfer_url: str = None


@dataclass
class UserLogin:
    id: int
    username: str
    token: str
