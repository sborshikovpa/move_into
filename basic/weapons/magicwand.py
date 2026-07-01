from weapons.base_weapon import BaseWeapon


class MagicWand(BaseWeapon):

    def __init__(
        self,
        name: str,
        damage: int,
        mana_cost: int
    ):
        super().__init__(
            name=name,
            damage=damage
        )

        self._mana_cost = mana_cost

    def attack(self, target, caster):
        if caster._mana >= self._mana_cost:
            caster._mana -= self._mana_cost
            super().attack(target)