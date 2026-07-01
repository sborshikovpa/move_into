from weapons.base_weapon import BaseWeapon


class Blade(BaseWeapon):

    def __init__(
        self,
        name: str,
        damage: int,
        stamina: int
    ):
        super().__init__(
            name=name,
            damage=damage
        )

        self._stamina = stamina

    def attack(self, target, caster):
        if caster._stamina >= self._stamina:
            caster._stamina -= self._stamina
            super().attack(target)