from dataclasses import dataclass
# import uuid


@dataclass(frozen=True, order=True)
class User:
    uuid: str
    name: str
