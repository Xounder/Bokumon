from typing import TypedDict


class BokumonStatus(TypedDict):
    attack: int
    defense: int
    speed: int
    criticalChance: int
    atualExperience: int
    upgradeExperience: int
    totalExperience: int


class BokumonData(TypedDict):
    name: str
    atualName: str
    level: int
    maxLife: int
    atualLife: int
    bokuBall: int
    status: BokumonStatus
    moves: list


class PlayerData(TypedDict):
    name: str
    status: str
    position: tuple
    tickets: int
    bokumons: BokumonData
    bokumonStorage: BokumonData
    bag: dict
