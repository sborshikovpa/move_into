# Pandas: конспект с примерами

Pandas - библиотека для работы с табличными данными. Главный объект pandas - `DataFrame`, то есть таблица со строками, колонками и методами для анализа данных.

Обычно pandas импортируют так:

```python
import pandas as pd
```

CSV-файл загружается через `pd.read_csv()`:

```python
df = pd.read_csv("analysis_data/df_orders.csv")
df
```

## DataFrame

`DataFrame` - это вся таблица целиком.

Полезные свойства и методы:

```python
df.shape      # количество строк и колонок
df.columns    # названия колонок
df.dtypes     # типы данных в колонках
df.info()     # общая информация о таблице
df.describe() # статистики по числовым колонкам
```

`shape` возвращает кортеж: сначала количество строк, потом количество колонок.

```python
rows_count = df.shape[0]
cols_count = df.shape[1]
```

## Series

Каждая колонка датафрейма - это `Series`.

```python
df["order_sum"]
```

Частые методы для колонок:

```python
df["delivery_fee"].value_counts()  # частоты значений
df["order_sum"].mean()             # среднее значение
df["user_id"].nunique()            # количество уникальных значений
df["order_id"].isna().sum()        # количество пропусков
```

`isna()` возвращает булеву маску: `True`, если значение пропущено, и `False`, если нет. Если вызвать `.sum()`, pandas посчитает количество `True`.

## Method Chaining

В pandas часто пишут цепочки методов. Это удобно, когда нужно сделать несколько действий подряд.

```python
missing_ratio = (
    df["order_id"]
    .isna()
    .mean()
)
```

Пример очистки таблицы цепочкой:

```python
clean_orders = (
    df
    .drop_duplicates(subset=["order_id"], keep="first")
    .dropna(subset=["order_sum"])
)
```

Создание новой колонки через `assign()`:

```python
orders_with_net = (
    df
    .assign(net_revenue=lambda x: x["order_sum"] - x["commission"] - x["delivery_fee"])
)
```

## Фильтрации

Фильтрация выбирает строки по условию.

```python
big_orders = df[df["order_sum"] > 10000]
```

Несколько условий объединяются через `&` или `|`. Каждое условие нужно брать в круглые скобки.

```python
filtered = df[(df["delivery_fee"] > 0) & (df["order_sum"] > 10000)]
```

Фильтрация по списку значений делается через `isin()`:

```python
paid_delivery = df[df["delivery_fee"].isin([990, 1490])]
```

Даты в формате `YYYY-MM-DD` можно сравнивать как строки:

```python
march_orders = df[df["event_date"] >= "2025-03-01"]
```

## Дубликаты И Пропуски

Найти строки с дубликатами:

```python
duplicates = df[df["order_id"].duplicated(keep=False)]
```

Удалить дубликаты:

```python
df_clean = df.drop_duplicates(subset=["order_id"], keep="first")
```

Посмотреть пропуски в нескольких колонках:

```python
df[["event_date", "order_sum", "commission", "delivery_fee"]].isna().sum()
```

Заполнить пропуски:

```python
df["delivery_fee"] = df["delivery_fee"].fillna(0)
```

Создать новую колонку:

```python
df["net_revenue"] = df["order_sum"] - df["commission"] - df["delivery_fee"]
```

## Объединение Таблиц

`concat()` склеивает таблицы. `axis=0` - по строкам, `axis=1` - по колонкам.

```python
events_all = pd.concat([events_early, events_late], axis=0)
```

`merge()` объединяет таблицы по ключу, как `JOIN` в SQL.

```python
orders_with_group = df.merge(
    matching[["user_id", "exp_group"]],
    on="user_id",
    how="left"
)
```

Основные варианты `how`:

- `left` - оставить все строки из левой таблицы
- `inner` - оставить только совпавшие строки
- `right` - оставить все строки из правой таблицы
- `outer` - оставить все строки из обеих таблиц

## Pivot Table

`pivot_table()` превращает длинную таблицу в широкую и сразу считает агрегацию.

```python
events_pivot = events.pivot_table(
    index="user_id",
    columns="event_type",
    values="event_date",
    aggfunc="count",
    fill_value=0
)
```

В этом примере строки - пользователи, колонки - типы событий, значения - количество событий каждого типа.

## Groupby И Агрегации

`groupby()` задает группы, `agg()` задает расчеты внутри каждой группы.

```python
orders_group_metrics = (
    orders_with_group
    .groupby("exp_group")
    .agg(
        orders_cnt=("order_id", "nunique"),
        users_cnt=("user_id", "nunique"),
        avg_order_sum=("order_sum", "mean"),
        total_revenue=("order_sum", "sum"),
        avg_commission=("commission", "mean"),
    )
)
```

Группировка по датам:

```python
orders_daily = (
    df.assign(event_date=pd.to_datetime(df["event_date"]))
    .groupby(pd.Grouper(key="event_date", freq="D"))
    .agg(
        orders_cnt=("order_id", "nunique"),
        revenue=("order_sum", "sum"),
        avg_check=("order_sum", "mean"),
    )
)
```

`pd.to_datetime()` превращает строки в даты. `pd.Grouper(freq="D")` группирует по дням.

## Мини-Шпаргалка

```python
pd.read_csv("path.csv")
df.shape
df.columns
df.dtypes
df.info()
df.describe()

df["col"].value_counts()
df["col"].mean()
df["col"].nunique()
df["col"].isna().sum()

df[df["col"] > 10]
df[(condition_1) & (condition_2)]
df["col"].isin(["A", "B"])

df.drop_duplicates(subset=["id"])
df["col"].fillna(0)

df1.merge(df2, on="id", how="left")
pd.concat([df1, df2], axis=0)

df.pivot_table(index="id", columns="type", values="value", aggfunc="count")
df.groupby("group_col").agg(metric=("value_col", "mean"))
```
