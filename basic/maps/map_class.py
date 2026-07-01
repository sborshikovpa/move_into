class MapClass:

    def __init__(self, x: int, y: int, map_symbol: str):
        self._x = x
        self._y = y
        self._map_symbol = map_symbol

    def check_cell(self, entity, x, y):
        return entity._x == x and entity._y == y

    def draw(self, entities):
        for y in range(self._y):
            for x in range(self._x):
                is_empty = True

                for entity in entities:
                    if self.check_cell(entity, x, y):
                        print(entity._map_symbol, end='  ')
                        is_empty = False
                        break

                if is_empty:
                    print(self._map_symbol, end='  ')

            print()