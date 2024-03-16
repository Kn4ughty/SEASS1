from dataclasses import dataclass
import time
import json
import pygame as pg 


# I need a better way to get this than importing pygame
prefPath = pg.system.get_pref_path("naught", "MOONLANDER")


@dataclass
class User:
    uuid: str
    name: str
    creationTime: float = time.time()



user1 = User("wao", "jambo")
print(user1)


