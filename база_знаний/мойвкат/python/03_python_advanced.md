---
tags:
  - python
  - advanced
  - notebook-summary
source: C:/Users/pavel/Downloads/python_4_advanced.ipynb
duplicate_source: C:/Users/pavel/Downloads/python_4_advanced (1).ipynb
---

# 03. Продвинутый Python

## Главное

В этом блоке появляются более компактные и выразительные инструменты Python: множества, тернарные выражения, comprehensions, обработка ошибок, кортежи и понимание изменяемости объектов.

## Множество `set`

`set` хранит уникальные элементы без гарантии порядка.

```python
some_set = set([3, 11, 2])
also_set = {1, 2, 3}
empty_set = set()
```

Важно: `{}` создает пустой словарь, а не множество.

```python
type({})      # dict
type(set())   # set
```

В множество можно превратить итерируемый объект:

```python
set(range(10))
set("abca")  # {"a", "b", "c"}
```

`in` в множестве работает очень быстро, потому что множество оптимизировано для проверки наличия.

```python
1 in some_set
```

## Методы множества

```python
some_set.add("a")
some_set.remove(11)   # ошибка, если элемента нет
some_set.discard(11)  # не падает, если элемента нет
some_set.pop()        # удаляет и возвращает произвольный элемент
```

Если элемент уже есть, повторный `add()` ничего не меняет.

## Операции над множествами

```python
pasithelle = {"A", "B", "C"}
koriger = {"B", "C", "D"}

pasithelle | koriger  # объединение
pasithelle & koriger  # пересечение
koriger - pasithelle  # разность
pasithelle <= koriger # является ли подмножеством
pasithelle >= koriger # является ли надмножеством
```

Сокращенные операции:

```python
some_set |= koriger
some_set -= {"A"}
```

## Тернарный оператор

Тернарное выражение выбирает значение по условию.

```python
value = "odd" if number % 2 else "even"
```

Форма:

```python
value_if_true if condition else value_if_false
```

Лучше не вкладывать тернарные выражения слишком глубоко. Если строка становится трудной для чтения, обычный `if` лучше.

## Comprehensions

Comprehension это компактный способ создать коллекцию.

### Список

```python
squares = [i ** 2 for i in range(10)]
even_squares = [i ** 2 for i in range(10) if i % 2 == 0]
```

### Тернарное выражение внутри comprehension

```python
values = [i ** 2 if i % 2 == 0 else i // 2 for i in range(10)]
```

Важно различать:

- `... for i in items if condition`: фильтрует элементы.
- `a if condition else b for i in items`: выбирает значение для каждого элемента.

### Множество

```python
unique_values = {i ** 2 for i in range(10)}
```

### Словарь

```python
mapping = {i: i ** 2 for i in range(10)}
```

## Обработка ошибок `try-except`

`try-except` нужен, когда ошибка возможна и у программы есть понятный способ продолжить.

```python
data = {"name": "Bob", "age": 30}

try:
    city = data["city"]
except KeyError:
    city = "unknown"
```

Для словаря часто проще использовать `get()`:

```python
city = data.get("city", "unknown")
```

## Изменяемые и неизменяемые типы

Неизменяемые:

- `int`
- `float`
- `bool`
- `str`
- `tuple`
- `NoneType`

Изменяемые:

- `list`
- `dict`
- `set`

`id()` показывает идентификатор объекта в памяти.

```python
x = 123
old_id = id(x)
x += 1
new_id = id(x)
```

Для неизменяемых объектов операция создает новый объект. Для изменяемых объект может измениться на месте.

```python
items = [1, 2, 3]
same_items = items
items.append(4)

same_items  # [1, 2, 3, 4]
```

## Опасность изменяемых значений по умолчанию

Плохой вариант:

```python
def add_item(item, items=[]):
    items.append(item)
    return items
```

Список создается один раз при определении функции и переиспользуется между вызовами.

Хороший вариант:

```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

## Кортеж `tuple`

Кортеж похож на список, но сам кортеж неизменяем.

```python
point = (3, 5)
single = (1,)
empty = tuple()
```

Зачем нужны кортежи:

- вернуть несколько значений из функции;
- зафиксировать структуру данных;
- использовать как ключ словаря, если внутри только hashable-значения.

```python
def get_user_info():
    return "Bob", 30

name, age = get_user_info()
```

## Изменяемые объекты внутри кортежа

Нельзя заменить элемент кортежа, но можно изменить изменяемый объект внутри него.

```python
sneaky_tuple = (1, 2, [10, 20])

# sneaky_tuple[2] = [30]  # ошибка
sneaky_tuple[2].append(30)
```

Кортеж защищает свои ссылки, но не делает вложенные списки неизменяемыми.

## Операции над кортежами

```python
(1, 2) + (3, 4)
(1, 2) * 3
len((1, 2, 3))
2 in (1, 2, 3)
```

## Стиль именования

- Переменные и функции: `snake_case`.
- Классы: `PascalCase`.
- Константы: `SCREAMING_SNAKE_CASE`.
- Внутренние переменные и методы: `_snake_case`.

```python
user_name = "Bob"

def get_user_name():
    return user_name

class UserProfile:
    pass

MAX_ATTEMPTS = 3
_internal_value = 10
```

## Практика

- Создать множество из списка `words`.
- Найти слова, у которых совпадает хотя бы одна буква с выбранным словом.
- Найти слова, все буквы которых присутствуют в выбранном слове.
- Найти слова, в которых присутствуют все буквы из выбранного слова.
- Переписать обычный `if` через тернарное выражение.
- Обработать `KeyError` при обращении к отсутствующему ключу `"city"`.
- Сохранить в списке только непустые кортежи, не меняя порядок.
- Распаковать кортеж, который возвращает `get_user_info`.
- Добавить число `4` в список внутри кортежа, не пересоздавая сам кортеж.

## Частые ошибки

- Писать `{}` и ожидать пустой `set`.
- Использовать `remove()`, когда элемент может отсутствовать.
- Делать слишком сложные однострочные comprehensions.
- Ловить слишком общий `Exception` без причины.
- Использовать изменяемый объект как значение аргумента по умолчанию.
- Считать, что `tuple` делает неизменяемыми все вложенные объекты.
