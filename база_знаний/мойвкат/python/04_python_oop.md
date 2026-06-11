---
tags:
  - python
  - oop
  - patterns
  - notebook-summary
source: C:/Users/pavel/Downloads/python_5_OOP.ipynb
---

# 04. ООП: полиморфизм, dunder-методы, фабрика

## Главное

ООП полезно не только для хранения данных в классах. Важная идея: разные объекты могут использоваться одинаково, если у них есть общий интерфейс.

## Полиморфизм

Полиморфизм позволяет вызывать один и тот же метод у объектов разных классов и получать разное поведение.

### Переопределение методов

```python
class Animal:
    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):
        return "woof"

class Cat(Animal):
    def speak(self):
        return "meow"

animals = [Dog(), Cat(), Dog()]

for animal in animals:
    print(animal.speak())
```

Метод называется одинаково, но реализация зависит от класса объекта.

## Утиная типизация

В Python часто важен не родительский класс, а наличие нужного метода или атрибута.

```python
class Bird:
    def fly(self):
        return "bird flies"

class Airplane:
    def fly(self):
        return "airplane flies"

def make_it_fly(obj):
    return obj.fly()

make_it_fly(Bird())
make_it_fly(Airplane())
```

Функции не важно, что это за объект, если он умеет `fly()`.

## Практика: фигуры

Идея задания: создать базовый класс `Shape` и несколько фигур с общим методом, например `area()`.

```python
class Shape:
    def area(self):
        raise NotImplementedError

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2

shapes = [Rectangle(2, 3), Circle(5)]

for shape in shapes:
    print(shape.area())
```

## Магические методы

Магические методы, или dunder methods, начинаются и заканчиваются двойным подчеркиванием. Они позволяют объектам вести себя как встроенные типы.

## `__str__`

`__str__` определяет человекочитаемое строковое представление объекта.

```python
class Person:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Person: {self.name}"

person = Person("Bob")
print(person)
```

Без `__str__` вывод объекта обычно выглядит как техническая информация с адресом в памяти.

## `__add__`

`__add__` задает поведение оператора `+`.

```python
class Wallet:
    def __init__(self, amount):
        self.amount = amount

    def __add__(self, other):
        return Wallet(self.amount + other.amount)

    def __str__(self):
        return f"{self.amount}"

w1 = Wallet(100)
w2 = Wallet(50)
w3 = w1 + w2
```

Важно возвращать новый объект, если операция не должна менять исходные.

## Другие полезные dunder-методы

- `__repr__`: техническое представление объекта для разработчика.
- `__len__`: поведение `len(obj)`.
- `__eq__`: сравнение через `==`.
- `__lt__`: сравнение через `<`.
- `__getitem__`: доступ через `obj[index]`.
- `__iter__`: возможность перебирать объект в `for`.

## Практика: `Vector`

Идея задания: сделать вектор, который красиво печатается и складывается с другим вектором.

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)
```

## Паттерн Factory

Фабрика скрывает выбор конкретного класса за общим интерфейсом. Пользователь кода просит объект нужного типа, а фабрика решает, что именно создать.

## Абстрактный базовый класс

```python
from abc import ABC, abstractmethod

class BaseBackend(ABC):
    @abstractmethod
    def predict(self, data):
        pass
```

`ABC` и `@abstractmethod` помогают описать обязательный интерфейс для наследников.

## Пример фабрики моделей

```python
class SklearnBackend(BaseBackend):
    def predict(self, data):
        return "sklearn prediction"

class TorchBackend(BaseBackend):
    def predict(self, data):
        return "torch prediction"

class Model:
    def __init__(self, model_type):
        if model_type == "sklearn":
            self.backend = SklearnBackend()
        elif model_type == "torch":
            self.backend = TorchBackend()
        else:
            raise ValueError(f"Unknown model type: {model_type}")

    def predict(self, data):
        return self.backend.predict(data)

model = Model("sklearn")
model.predict([1, 2, 3])
```

Главная выгода: основной код работает одинаково с разными реализациями.

## Частые ошибки

- Проверять типы вручную там, где достаточно вызвать общий метод.
- Делать базовый класс, но не фиксировать ожидаемый интерфейс.
- Перегружать dunder-методы неожиданным поведением.
- Возвращать из `__str__` не строку.
- В `__add__` менять исходный объект, когда пользователь ожидает новый результат.
- Раздувать фабрику длинной цепочкой `if/elif`; для большого числа типов лучше словарь классов.

## Мини-чеклист

- У объектов с общим смыслом есть общий метод.
- Функции зависят от поведения, а не от конкретного класса.
- `__str__` помогает читать вывод.
- Dunder-методы делают объект удобнее, но не должны удивлять.
- Factory полезна, когда создание объекта зависит от типа, настройки или пути.
