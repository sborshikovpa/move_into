class BaseWeapon:
    def __init__(
        self,
        name:str,
        damage:int,
        ):

        self._name = name
        self._damage = damage
    
    def attack(self, target):
        target._hp = max(0, target._hp-self._damage)
        print(
            f"{self.__class__.__name__} ударили "
            f"{target._name} на {self._damage} урона "
            f"{target._name} стало {target._hp} здоровья "
        )