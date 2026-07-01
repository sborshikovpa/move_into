from enteties.base_hero import BaseHero

class Enemie(BaseHero):

    def __init__(
        self,
        name: str,
        hp: int,
        defense: int,
        attack: int,
        x: int,
        y: int,
        map_symbol: str,
        inventory: list = [],
        abilities: list = []
    ):
        super().__init__(name, hp, defense, attack, x, y, map_symbol, inventory, abilities)