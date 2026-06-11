---
tags:
  - python
  - advanced
  - context-manager
  - decorators
  - iterators
  - generators
  - notebook-summary
source: C:/Users/pavel/Downloads/python_6_advanced+.ipynb
---

# 06. Очень продвинутый Python

## Главное

Этот блок про инструменты, которые делают код более профессиональным:

- `with` гарантирует корректное закрытие ресурсов;
- функции можно передавать как обычные объекты;
- `lambda`, `sorted(key=...)`, `map`, `filter` помогают описывать преобразования данных;
- декораторы добавляют поведение к функциям без изменения их кода;
- итераторы и генераторы позволяют работать с последовательностями лениво, не загружая все в память;
- `if __name__ == "__main__"` отделяет запуск файла от импорта.

## Менеджеры контекста `with`

Контекстный менеджер управляет ресурсом: открывает его перед блоком кода и гарантированно освобождает после блока, даже если внутри произошла ошибка.

Самый частый пример - работа с файлами:

```python
with open("example.txt", "w", encoding="utf-8") as file:
    file.write("Привет, мир!")
```

После выхода из блока файл закроется автоматически. Поэтому не нужно вручную писать `file.close()`.

## JSON и файлы

JSON часто используют для конфигов, обмена данными между сервисами и сохранения простых структур.

```python
import json

data = {
    "name": "Иван",
    "age": 30,
    "skills": ["Python", "SQL"],
}

with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

with open("data.json", "r", encoding="utf-8") as file:
    loaded_data = json.load(file)

print(loaded_data["skills"])
```

Важные аргументы:

- `ensure_ascii=False`: сохраняет кириллицу нормальным текстом, а не escape-последовательностями.
- `indent=4`: делает JSON читаемым.

## Свой контекстный менеджер

Класс становится контекстным менеджером, если реализует методы:

- `__enter__`: вызывается при входе в `with`, его результат попадает в переменную после `as`;
- `__exit__`: вызывается при выходе из `with`.

```python
class MyDatabaseConnection:
    def __enter__(self):
        print("Подключаемся к БД...")
        return "connection"

    def __exit__(self, exc_type, exc_value, traceback):
        print("Закрываем соединение с БД...")

with MyDatabaseConnection() as db:
    print(f"Работаем: {db}")
```

Аргументы `__exit__` связаны с ошибками:

- `exc_type`: тип ошибки;
- `exc_value`: объект ошибки;
- `traceback`: стек вызовов.

Если `__exit__` возвращает `True`, ошибка подавляется. Обычно так делать не стоит без явной причины.

## Дополнение: `contextlib`

Для простых контекстных менеджеров можно не писать класс, а использовать `contextlib.contextmanager`.

```python
from contextlib import contextmanager
import time

@contextmanager
def timer():
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print(f"Код выполнялся {end - start:.2f} секунд")

with timer():
    time.sleep(1)
```

`yield` разделяет вход и выход: код до `yield` выполняется перед блоком, код после - при выходе.

## Задача из ноутбука: `Timer`

Нужно написать менеджер контекста, который измеряет время выполнения блока.

```python
import time

class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end = time.time()
        print(f"Код выполнялся примерно {self.end - self.start:.1f} секунд")

with Timer():
    print("Код выполняется...")
    time.sleep(1)
```

## Функции как объекты

В Python функция - это объект. Ее можно сохранить в переменную, передать в другую функцию или вернуть из функции.

```python
def say_hello(name):
    return f"Привет, {name}!"

my_func = say_hello
print(my_func("Алексей"))
```

Важно: `say_hello` без скобок - сама функция, `say_hello("Алексей")` - результат вызова функции.

## `lambda`

`lambda` создает маленькую анонимную функцию в одну строку.

```python
square = lambda x: x * x
print(square(5))
```

Форма:

```python
lambda arguments: expression
```

Когда использовать `lambda`:

- короткая функция нужна один раз;
- функция передается как аргумент, например в `sorted`;
- выражение действительно простое.

Когда лучше `def`:

- логика длиннее одной простой операции;
- нужен понятный docstring;
- функцию планируется переиспользовать;
- важно удобнее отлаживать код.

## `sorted(key=...)`

`sorted()` может принимать функцию `key`, которая говорит, по какому признаку сортировать элементы.

```python
words = ["яблоко", "кот", "автомобиль", "дом"]

sorted_by_length = sorted(words, key=len)
sorted_by_last_letter = sorted(words, key=lambda word: word[-1])
```

Сортировка списка словарей:

```python
people = [
    {"name": "Иван", "age": 15},
    {"name": "Анна", "age": 22},
    {"name": "Борис", "age": 30},
]

by_age = sorted(people, key=lambda person: person["age"])
by_name = sorted(people, key=lambda person: person["name"])
```

## `map` и `filter`

`map(func, iterable)` применяет функцию к каждому элементу.

```python
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
```

`filter(func, iterable)` оставляет элементы, для которых функция вернула `True`.

```python
evens = list(filter(lambda x: x % 2 == 0, numbers))
```

Обе функции возвращают итераторы, поэтому для просмотра результата часто используют `list()`.

## Дополнение: чаще удобнее comprehension

В Python многие такие задачи читаются проще через comprehensions.

```python
doubled = [x * 2 for x in numbers]
evens = [x for x in numbers if x % 2 == 0]
```

`map` и `filter` полезны, но если `lambda` становится сложной, comprehension обычно понятнее.

## Декораторы

Декоратор - это функция, которая принимает функцию и возвращает новую функцию с дополнительным поведением.

```python
def my_decorator(func):
    def wrapper():
        print("--> До вызова")
        func()
        print("<-- После вызова")
    return wrapper

@my_decorator
def say_hi():
    print("Всем привет!")

say_hi()
```

Синтаксис:

```python
@my_decorator
def say_hi():
    ...
```

примерно равен:

```python
say_hi = my_decorator(say_hi)
```

## Декоратор с аргументами функции

Чтобы декоратор работал с разными функциями, используют `*args` и `**kwargs`.

```python
def debug(func):
    def wrapper(*args, **kwargs):
        print(f"Вызываем {func.__name__} с аргументами: {args} {kwargs}")
        result = func(*args, **kwargs)
        print(f"Функция вернула: {result}")
        return result
    return wrapper

@debug
def add(a, b):
    return a + b

add(5, 3)
```

## Дополнение: `functools.wraps`

В реальном коде декоратор лучше писать с `functools.wraps`, чтобы сохранить имя и метаданные исходной функции.

```python
from functools import wraps

def debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Вызываем {func.__name__}: {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"Результат: {result}")
        return result
    return wrapper
```

Без `@wraps(func)` обернутая функция будет называться `wrapper`, что мешает отладке и документации.

## Итераторы

Итерируемый объект - это объект, по которому можно пройтись в `for`: список, строка, кортеж, словарь, файл.

Итератор - объект, который выдает значения по одному через `next()`.

```python
my_list = [10, 20, 30]
my_iterator = iter(my_list)

print(next(my_iterator))  # 10
print(next(my_iterator))  # 20
print(next(my_iterator))  # 30
```

Следующий `next()` вызовет `StopIteration`.

## Свой итератор

Чтобы сделать свой итератор, нужны методы:

- `__iter__`: возвращает итератор;
- `__next__`: возвращает следующий элемент или выбрасывает `StopIteration`.

```python
class MyRange:
    def __init__(self, start, end):
        self.current = start
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.end:
            raise StopIteration

        value = self.current
        self.current += 1
        return value

for number in MyRange(1, 4):
    print(number)
```

## Дополнение: iterable и iterator не одно и то же

Список - итерируемый объект, но сам он не итератор:

```python
items = [1, 2, 3]
iterator = iter(items)
```

Итератор часто "одноразовый": если пройти его до конца, он опустеет.

```python
it = iter([1, 2, 3])
list(it)  # [1, 2, 3]
list(it)  # []
```

Это важно для `map`, `filter` и генераторов.

## Задача из ноутбука: `EvenNumbers`

Нужно написать итератор, который возвращает только четные числа из переданного списка.

```python
class EvenNumbers:
    def __init__(self, numbers):
        self.numbers = numbers
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.index < len(self.numbers):
            value = self.numbers[self.index]
            self.index += 1
            if value % 2 == 0:
                return value
        raise StopIteration

numbers = [1, 2, 3, 4, 5, 6]
even_iter = EvenNumbers(numbers)

assert list(even_iter) == [2, 4, 6]
```

## Генераторы `yield`

Генератор - самый простой способ создать ленивый итератор.

```python
def count_up_to(max_value):
    count = 1
    while count <= max_value:
        yield count
        count += 1

for number in count_up_to(3):
    print(number)
```

`yield` возвращает значение и ставит функцию на паузу. При следующем `next()` выполнение продолжится с того же места.

## Задача из ноутбука: Fibonacci

```python
def fibonacci(n):
    a = 0
    b = 1
    for _ in range(n):
        yield a
        a, b = b, a + b

assert list(fibonacci(7)) == [0, 1, 1, 2, 3, 5, 8]
```

## Генераторные выражения

List comprehension создает список целиком:

```python
list_comp = [x ** 2 for x in range(100000)]
```

Generator expression вычисляет элементы лениво:

```python
gen_comp = (x ** 2 for x in range(100000))
```

Генератор экономит память, потому что не хранит все значения сразу.

```python
total_sum = sum(x ** 2 for x in range(1, 1000001) if x % 2 != 0)
```

Когда генераторное выражение единственный аргумент функции, дополнительные скобки можно не писать:

```python
sum(x * x for x in numbers)
```

## `if __name__ == "__main__"`

У каждого Python-файла есть переменная `__name__`.

- Если файл запущен напрямую, `__name__ == "__main__"`.
- Если файл импортирован, `__name__` равно имени модуля.

```python
def some_useful_function():
    return 42

if __name__ == "__main__":
    print("Скрипт запущен напрямую!")
    print("Результат:", some_useful_function())
```

Это нужно, чтобы код запуска не выполнялся при импорте.

## Типичные сценарии использования

- Файл содержит функции, которые импортируются в другие файлы.
- Внизу файла есть маленькая проверка, demo или запуск CLI.
- Тестовый код не должен запускаться при `import`.

## Частые ошибки

- Открывать файл без `with` и забывать закрыть.
- Писать `json.dump()` без `ensure_ascii=False`, если в данных есть кириллица.
- Вызывать функцию при передаче вместо передачи самой функции: `key=my_func()` вместо `key=my_func`.
- Делать сложную `lambda`, которую трудно читать.
- Забывать `return result` внутри декоратора.
- Писать декоратор без `*args, **kwargs`, а потом применять его к функциям с аргументами.
- Не использовать `functools.wraps` в реальном декораторе.
- Пытаться пройти один и тот же итератор два раза.
- Использовать список там, где нужен ленивый генератор для большого объема данных.
- Писать код запуска на уровне файла и удивляться, что он выполняется при импорте.

## Мини-шпаргалка

```python
# with
with open("file.txt", "r", encoding="utf-8") as file:
    text = file.read()

# sorted key
sorted(items, key=lambda item: item["name"])

# map/filter
list(map(lambda x: x * 2, numbers))
list(filter(lambda x: x > 0, numbers))

# decorator
def decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper

# iterator protocol
iterable = [1, 2, 3]
iterator = iter(iterable)
next(iterator)

# generator
def gen():
    yield 1

# generator expression
sum(x ** 2 for x in numbers)

# main guard
if __name__ == "__main__":
    main()
```

## Практика

- Написать контекстный менеджер `Timer`.
- Сохранить словарь пользователя в JSON и прочитать его обратно.
- Отсортировать список словарей людей по возрасту и имени.
- Написать `lambda`, которая возвращает квадрат числа.
- Отфильтровать список чисел, оставив только четные.
- Написать декоратор `debug`, который печатает аргументы и результат функции.
- Реализовать итератор `EvenNumbers`.
- Написать генератор `fibonacci(n)`.
- Посчитать сумму квадратов нечетных чисел от `1` до `1_000_000` через генераторное выражение.
- Создать файл с функцией и блоком `if __name__ == "__main__"` и проверить разницу между запуском и импортом.
