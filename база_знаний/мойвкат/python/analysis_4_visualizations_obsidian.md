---
title: "Визуализация данных в Python"
source: "analysis_4_visualizations.ipynb"
tags:
  - python
  - data-analysis
  - visualization
  - matplotlib
  - seaborn
---

# Визуализация данных в Python

Визуализация помогает быстро увидеть структуру данных: динамику, распределения, выбросы, связи между признаками и различия между категориями.

Основные библиотеки из ноутбука:

- `matplotlib` - базовая библиотека для построения графиков.
- `seaborn` - библиотека поверх `matplotlib`, удобная для статистических графиков.
- `pandas` - подготовка и агрегация данных перед визуализацией.

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

df = pd.read_csv("analysis_data/df_orders.csv")
events = pd.read_csv("analysis_data/df_events.csv")
```

> [!tip]
> Методы и параметры графиков не нужно зубрить. Важно понимать, какой график для какой задачи подходит, а синтаксис можно быстро посмотреть в документации или старых ноутбуках.

## Общий шаблон графика в Matplotlib

`pyplot` - основной модуль `matplotlib`. Через него можно создать фигуру, построить график, подписать оси и показать результат.

```python
x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]

plt.figure(figsize=(6, 4))
plt.plot(
    x,
    y,
    color="crimson",
    linewidth=3,
    linestyle="--",
    label="y = x^2"
)
plt.title("Пример графика в Matplotlib")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()
```

Важные параметры:

- `figsize=(width, height)` - размер графика.
- `color` - цвет линии или точек.
- `linewidth` - толщина линии.
- `linestyle` - стиль линии.
- `label` - подпись для легенды.
- `plt.title()` - заголовок.
- `plt.xlabel()` и `plt.ylabel()` - подписи осей.
- `plt.legend()` - показать легенду.
- `plt.show()` - вывести график.

## Линейный график

Линейный график используют, когда нужно показать изменение числового показателя по порядку или во времени.

Хорошо подходит для:

- динамики заказов по дням;
- динамики выручки;
- изменения метрики во времени;
- сравнения трендов.

## Временной ряд

Чтобы построить динамику заказов по дням, нужно сначала привести дату к типу `datetime`, затем сгруппировать данные по дням.

```python
orders_daily = (
    df.assign(event_date=pd.to_datetime(df["event_date"]))
    .groupby(pd.Grouper(key="event_date", freq="D"))
    .agg(orders_cnt=("order_id", "nunique"))
    .reset_index()
)
```

Построение графика:

```python
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    orders_daily["event_date"],
    orders_daily["orders_cnt"],
    marker="o",
    linestyle="-"
)

ax.set_xlabel("Дата")
ax.set_ylabel("Кол-во заказов")
ax.set_title("Динамика количества заказов по дням")

ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
plt.xticks(rotation=45)
plt.show()
```

Что важно:

- `pd.to_datetime()` переводит колонку в формат даты.
- `pd.Grouper(key="event_date", freq="D")` группирует по дням.
- `nunique` считает количество уникальных заказов.
- `marker="o"` добавляет точки на линии.
- `DateFormatter("%d.%m")` форматирует даты на оси X.
- `rotation=45` поворачивает подписи дат, чтобы они не слипались.

## Scatter plot

Диаграмма рассеяния показывает связь между двумя числовыми переменными. Каждая точка - одно наблюдение.

В ноутбуке пример: зависимость комиссии от суммы заказа.

```python
plt.figure(figsize=(5, 4))
plt.scatter(
    df["order_sum"],
    df["commission"],
    alpha=0.2,
    s=10
)
plt.title("Зависимость комиссии от суммы заказа")
plt.xlabel("Сумма заказа")
plt.ylabel("Комиссия")
plt.show()
```

Полезные параметры:

- `alpha` - прозрачность точек. Помогает, когда точек много.
- `s` - размер точек.

Использовать, когда нужно понять:

- есть ли зависимость между двумя числовыми признаками;
- линейная связь или нет;
- есть ли группы точек;
- есть ли выбросы.

## Гистограмма

Гистограмма показывает распределение одной числовой переменной. Значения разбиваются на интервалы, которые называются `bins`.

```python
plt.figure(figsize=(6, 3))
plt.hist(
    df["order_sum"],
    bins=30,
    edgecolor="white",
    alpha=0.9
)
plt.title("Распределение суммы заказа")
plt.xlabel("Сумма заказа")
plt.ylabel("Количество заказов")
plt.show()
```

Что смотреть на гистограмме:

- где большинство значений;
- есть ли длинный хвост;
- есть ли выбросы;
- похоже ли распределение на нормальное;
- есть ли несколько пиков.

## Pie chart

Круговая диаграмма показывает доли частей от целого. Ее лучше использовать, когда категорий мало.

В ноутбуке строится распределение заказов по стоимости доставки.

```python
fee_share = (
    df["delivery_fee"]
    .value_counts()
    .reset_index(name="count")
)
```

```python
plt.figure(figsize=(5, 4))
plt.pie(
    fee_share["count"],
    labels=fee_share["delivery_fee"],
    autopct="%.1f%%"
)
plt.title("Доли стоимости доставки")
plt.show()
```

Полезный параметр:

- `autopct="%.1f%%"` - выводит проценты на графике.

> [!note]
> Если категорий много, круговая диаграмма быстро становится нечитаемой. Тогда лучше использовать столбчатую диаграмму.

## Bar plot

Столбчатая диаграмма удобна для сравнения категорий.

В ноутбуке пример: количество событий по типам.

```python
event_counts = (
    events["event_type"]
    .value_counts()
    .reset_index(name="count")
)
```

```python
plt.figure(figsize=(8, 3))
sns.barplot(
    data=event_counts,
    x="event_type",
    y="count"
)
plt.title("Количество событий по типам")
plt.xticks(rotation=45)
plt.show()
```

Когда использовать:

- сравнение количества объектов в категориях;
- сравнение средних значений по группам;
- рейтинг категорий;
- частоты событий.

## Seaborn и параметр hue

В `seaborn` можно легко добавить группировку по цвету через `hue`.

Пример: сумма заказа и комиссия с разбивкой по стоимости доставки.

```python
plt.figure(figsize=(8, 4))
sns.scatterplot(
    data=df,
    x="order_sum",
    y="commission",
    hue="delivery_fee"
)
plt.title("Сумма заказа vs Комиссия с разбивкой по доставке")
plt.show()
```

`hue` полезен, когда нужно увидеть зависимость в разрезе категорий.

## Boxplot

Boxplot, или "ящик с усами", показывает распределение числовой переменной по категориям.

Он помогает увидеть:

- медиану;
- нижний и верхний квартили;
- разброс значений;
- выбросы;
- различия между группами.

```python
df["delivery_fee"].unique()
```

```python
plt.figure(figsize=(7, 4))
sns.boxplot(
    data=df,
    x="delivery_fee",
    y="order_sum",
    order=sorted(df["delivery_fee"].dropna().unique())
)
plt.title("Распределение сумм заказа по стоимости доставки")
plt.xlabel("Стоимость доставки")
plt.ylabel("Сумма заказа")
plt.show()
```

Как читать boxplot:

- линия внутри ящика - медиана;
- границы ящика - 25-й и 75-й процентили;
- "усы" - основной диапазон значений;
- отдельные точки за усами - возможные выбросы.

## Pairplot

`pairplot` строит все попарные scatter plot для числовых признаков, а на диагонали показывает распределения.

```python
sns.pairplot(
    data=df[["order_sum", "commission", "delivery_fee"]]
)
plt.show()
```

Использовать на этапе разведочного анализа, когда нужно быстро посмотреть:

- связи между признаками;
- форму распределений;
- выбросы;
- возможную корреляцию.

> [!warning]
> `pairplot` может быть тяжелым на больших датафреймах и при большом количестве колонок.

## Корреляция и Heatmap

Корреляция показывает силу линейной связи между числовыми признаками.

```python
corr = df[["order_sum", "commission", "delivery_fee"]].corr()
```

Тепловая карта удобно показывает матрицу корреляций:

```python
plt.figure(figsize=(5, 4))
sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="coolwarm"
)
plt.title("Корреляция между числовыми признаками")
plt.show()
```

Параметры:

- `annot=True` - подписывает значения в ячейках.
- `fmt=".2f"` - округляет числа до 2 знаков.
- `cmap="coolwarm"` - цветовая схема.

Как читать корреляцию:

- близко к `1` - сильная положительная связь;
- близко к `-1` - сильная отрицательная связь;
- близко к `0` - линейной связи почти нет.

> [!important]
> Корреляция не доказывает причинно-следственную связь. Она показывает только совместное изменение признаков.

## Как выбрать тип графика

| Задача | График |
|---|---|
| Динамика во времени | Линейный график |
| Связь двух числовых переменных | Scatter plot |
| Распределение одной числовой переменной | Гистограмма |
| Доли от целого | Pie chart |
| Сравнение категорий | Bar plot |
| Распределение числа по категориям | Boxplot |
| Быстрый обзор попарных связей | Pairplot |
| Матрица корреляций | Heatmap |

## Практические задания

### Задание 1

Построить линейный график динамики суммы заказов по дням.

Решение:

```python
orders_sum_daily = (
    df.assign(event_date=pd.to_datetime(df["event_date"]))
    .groupby(pd.Grouper(key="event_date", freq="D"))
    .agg(total_order_sum=("order_sum", "sum"))
    .reset_index()
)

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    orders_sum_daily["event_date"],
    orders_sum_daily["total_order_sum"],
    marker="o",
    linestyle="-"
)

ax.set_title("Динамика суммы заказов по дням")
ax.set_xlabel("Дата")
ax.set_ylabel("Сумма заказов")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
plt.xticks(rotation=45)
plt.show()
```

### Задание 2

Построить гистограмму распределения комиссии `commission` с `bins=40`.

Решение:

```python
plt.figure(figsize=(6, 3))
plt.hist(
    df["commission"],
    bins=40,
    edgecolor="white",
    alpha=0.9
)
plt.title("Распределение комиссии")
plt.xlabel("Комиссия")
plt.ylabel("Количество заказов")
plt.show()
```

### Задание 3

Построить boxplot для комиссии `commission` в разрезе стоимости доставки `delivery_fee`.

Решение:

```python
plt.figure(figsize=(7, 4))
sns.boxplot(
    data=df,
    x="delivery_fee",
    y="commission",
    order=sorted(df["delivery_fee"].dropna().unique())
)
plt.title("Распределение комиссии по стоимости доставки")
plt.xlabel("Стоимость доставки")
plt.ylabel("Комиссия")
plt.show()
```

## Мини-шпаргалка по синтаксису

```python
# Размер графика
plt.figure(figsize=(8, 4))

# Линейный график
plt.plot(x, y)

# Scatter plot
plt.scatter(x, y)

# Гистограмма
plt.hist(values, bins=30)

# Круговая диаграмма
plt.pie(values, labels=labels, autopct="%.1f%%")

# Bar plot
sns.barplot(data=df, x="category", y="value")

# Scatter plot с группировкой
sns.scatterplot(data=df, x="x", y="y", hue="category")

# Boxplot
sns.boxplot(data=df, x="category", y="value")

# Pairplot
sns.pairplot(data=df[["col1", "col2", "col3"]])

# Heatmap корреляций
sns.heatmap(df.corr(), annot=True, fmt=".2f")
```

## Главное из ноутбука

- Перед визуализацией данные часто нужно подготовить: привести даты, сгруппировать, посчитать агрегаты.
- `matplotlib` дает гибкий контроль над графиком.
- `seaborn` удобнее для статистических графиков и группировок.
- Тип графика выбирается по аналитической задаче, а не по красоте.
- Подписи осей, заголовок и читаемые даты делают график намного полезнее.
- Для распределений подходят гистограммы и boxplot.
- Для связей между признаками подходят scatter plot, pairplot и heatmap.
