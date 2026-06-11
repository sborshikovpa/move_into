---
tags:
  - python
  - architecture
  - oop
  - notebook-summary
source: C:/Users/pavel/Downloads/python_3_architecture.ipynb
---

# 02. Архитектура проекта и первые классы

## Главное

Когда программа растет, код удобно раскладывать по модулям, настройки выносить в конфиг, а связанные данные и поведение объединять в классы.

## Модули

Модуль в Python это обычный файл `.py`, который можно импортировать.

```python
import my_module

my_module.some_value
my_module.print_value()
```

Импорт конкретных имен:

```python
from my_module import some_value, print_value

some_value
print_value()
```

Импорт из папки:

```python
from scripts.script import some_util
```

## Конфиг и константы

Константы это значения, которые не планируется менять во время выполнения программы. По соглашению их пишут большими буквами.

```python
MAP_HEIGHT = 5
MAP_WIDTH = 10
MAP_SYMBOL = "."
```

Их удобно вынести в `config.py`:

```python
from config import MAP_HEIGHT, MAP_WIDTH, MAP_SYMBOL
```

Так настройки проекта можно менять в одном месте.

## Классы и объекты

Класс описывает тип объекта. Объект это конкретный экземпляр класса.

```python
class Tree:
    pass

tree_1 = Tree()
tree_2 = Tree()
```

Атрибуты можно хранить внутри объекта:

```python
tree_1.leaves = 10
tree_2.leaves = 32
```

`tree_1` и `tree_2` разные объекты, поэтому их атрибуты не связаны.

## Конструктор `__init__`

Конструктор задает начальное состояние объекта.

```python
class Tree:
    def __init__(self, leaves, height):
        self.leaves = leaves
        self.height = height

tree = Tree(leaves=8, height=3.0)
```

`self` это ссылка на объект, для которого вызывается метод.

## Методы

Метод это функция внутри класса, которая работает с объектом.

```python
class Tree:
    def __init__(self, leaves, height):
        self.leaves = leaves
        self.height = height

    def grow(self):
        self.height += 1
        self.leaves += 10

tree = Tree(8, 3.0)
tree.grow()
```

Когда вызывается `tree.grow()`, в `self` автоматически подставляется `tree`.

## Пример с персонажем

Класс удобен, когда у сущности есть состояние и действия.

```python
class Character:
    def __init__(self, hp, damage):
        self.hp = hp
        self.damage = damage

    def attack(self, target):
        target.hp -= self.damage

hero = Character(hp=10, damage=3)
enemy = Character(hp=8, damage=2)

hero.attack(enemy)
```

## Инкапсуляция

Инкапсуляция помогает спрятать внутреннее устройство объекта и оставить понятный интерфейс.

В Python одинарное подчеркивание означает: "это внутренняя часть, не трогай напрямую без причины".

```python
class Character:
    def __init__(self, hp):
        self._hp = hp

    def heal(self, amount):
        self._hp += amount

    def is_alive(self):
        return self._hp > 0
```

Это не жесткая защита, а соглашение.

## Наследование

Наследование позволяет вынести общее поведение в базовый класс.

```python
class Entity:
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

    def check_cell(self, x, y):
        return self.x == x and self.y == y

class Character(Entity):
    def __init__(self, x, y, symbol, hp):
        super().__init__(x, y, symbol)
        self._hp = hp
```

`super().__init__()` вызывает конструктор родительского класса и убирает дублирование.

## Общая функция для разных сущностей

Если у всех объектов есть `x`, `y` и `symbol`, их можно рисовать одинаково.

```python
def draw(entities):
    for entity in entities:
        print(entity.x, entity.y, entity.symbol)
```

Функции не важно, персонаж это, предмет или другой объект, если нужные атрибуты есть.

## Практика из ноутбука

### `Cell`

Создать класс `Cell`:

- принимает координаты `x` и `y`;
- умеет перемещаться методом `move(dx, dy)`;
- умеет возвращать координаты.

```python
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
```

### `Hero`

Создать класс `Hero`:

- хранит `_name`;
- хранит `_stamina`, по умолчанию `100`;
- методы должны менять состояние через понятный интерфейс, а не прямым доступом снаружи.

### `Weapon` и `MagicWand`

Базовый класс `Weapon` наносит урон. Наследник `MagicWand` должен расширить или изменить это поведение.

```python
class Weapon:
    def __init__(self, damage):
        self.damage = damage

    def hit(self, target):
        target.hp -= self.damage

class MagicWand(Weapon):
    def hit(self, target):
        target.hp -= self.damage
        target.magic_effect = True
```

## Частые ошибки

- Забыть `self` в методе.
- Назвать атрибут в `__init__` одним именем, а читать потом другим.
- Дублировать код родителя вместо `super()`.
- Слишком рано строить сложную иерархию классов.
- Делать все атрибуты публичными и менять объект снаружи хаотично.

## Мини-чеклист архитектуры

- Повторяющиеся настройки лежат в `config.py`.
- Повторяющийся код вынесен в функции или методы.
- Связанные данные и поведение живут в классе.
- Общие поля разных сущностей вынесены в базовый класс.
- Внешний код вызывает методы объекта, а не постоянно правит его внутренности напрямую.
