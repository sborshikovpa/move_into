class BaseHero:

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
        self._name = name
        self._hp = hp
        self._defense = defense
        self._attack = attack
        self._x = x
        self._y = y
        self._map_symbol = map_symbol

        self._experience = 0
        self.inventory = inventory
        self.abilities = abilities

    def pick_item(self, item):
        self.inventory.append(item)

    def get_experience(self, amount):
        self._experience += amount

    def calculate_damage(self, target):
        return max(1, self._attack - target._defense)

    def attack_target(self, target):
        damage = self.calculate_damage(target)
        target._hp -= damage

        print(
            f"{self._name} ударил "
            f"{target._name} на {damage} урона"
            f"{target._name} стало {target._hp} здоровья"
        )

    def use_ability(self, ability_index, target):
        ability = self.abilities[ability_index]
        ability.use(self, target)