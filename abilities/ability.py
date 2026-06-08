class BaseAbility:
    def __init__(self, damage_bonus):
        self._damage_bonus = damage_bonus

    def use(self, user, target):
        damage = user._attack + self._damage_bonus - target._defense
        damage = max(1, damage)

        target._hp -= damage

        print(
            f"{user._name} использует {self.__class__.__name__}" 
            f"и наносит {damage} урона {target._name}"
            f"{target._name} стало {target._hp} здоровья"
        )