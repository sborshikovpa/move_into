from enteties.base_hero import BaseHero

class Character(BaseHero):

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
        abilities: list = [],
        stamina: int = 100
    ):
        super().__init__(name, hp, defense, attack, x, y, map_symbol, inventory, abilities)
        self._stamina = stamina
        self._mana = 100
    
    def get_stamina(self) -> int:
        return self._stamina
    
    def sprint(self, distance):
        self._stamina =  max(0, self._stamina - distance*2)