# Copyright 2020 IBM Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ast
import datetime
from itertools import chain
from typing import Any

import numpy as np
import pandas as pd

try:
    import pyspark.sql.functions as pysql
    from pyspark.ml.feature import StringIndexer

    # noqa in the imports here because those get used dynamically and flake fails.
    from pyspark.sql.functions import hour as spark_hour  # noqa
    from pyspark.sql.functions import lit  # noqa
    from pyspark.sql.functions import to_timestamp  # noqa
    from pyspark.sql.functions import minute as spark_minute  # noqa
    from pyspark.sql.functions import month as spark_month  # noqa

    from pyspark.sql.functions import (  # noqa; isort: skip
        create_map,
        dayofmonth,
        dayofweek,
        dayofyear,
    )

    spark_installed = True
except ImportError:
    spark_installed = False


from lale.expressions import Expr
from lale.helpers import (
    _is_ast_attribute,
    _is_ast_subscript,
    _is_pandas_df,
    _is_spark_df,
)


class categorical:
    """Creates a callable for projecting categorical columns with sklearn's ColumnTransformer or Lale's Project operator.

    Parameters
    ----------
    max_values : int

        Maximum number of unique values in a column for it to be considered categorical.

    Returns
    -------
    callable
        Function that, given a dataset X, returns a list of columns,
        containing either string column names or integer column indices."""

    def __init__(self, max_values: int = 5):
        self._max_values = max_values

    def __repr__(self):
        return f"lale.lib.lale.categorical(max_values={self._max_values})"

    def __call__(self, X):
        def is_categorical(column_values):
            unique_values = set()
            for val in column_values:
                if val not in unique_values:
                    unique_values.add(val)
                    if len(unique_values) > self._max_values:
                        return False
            return True

        if _is_pandas_df(X):
            result = [c for c in X.columns if is_categorical(X[c])]
        elif isinstance(X, np.ndarray):
            result = [c for c in range(X.shape[1]) if is_categorical(X[:, c])]
        else:
            raise TypeError(f"unexpected type {type(X)}")
        return result


class date_time:
    """Creates a callable for projecting date/time columns with sklearn's ColumnTransformer or Lale's Project operator.

    Parameters
    ----------
    fmt : str

        Format string for `strptime()`, see https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior

    Returns
    -------
    callable
        Function that, given a dataset X, returns a list of columns,
        containing either string column names or integer column indices."""

    def __init__(self, fmt):
        self._fmt = fmt

    def __repr__(self):
        return f"lale.lib.lale.date_time(fmt={self._fmt})"

    def __call__(self, X):
        def is_date_time(column_values):
            try:
                for val in column_values:
                    if isinstance(val, str):
                        datetime.datetime.strptime(val, self._fmt)
                    else:
                        return False
            except ValueError:
                return False
            return True

        if _is_pandas_df(X):
            result = [c for c in X.columns if is_date_time(X[c])]
        elif isinstance(X, np.ndarray):
            result = [c for c in range(X.shape[1]) if is_date_time(X[:, c])]
        else:
            raise TypeError(f"unexpected type {type(X)}")
        return result


def replace(df: Any, replace_expr: Expr, new_column_name: str):
    re: Any = replace_expr._expr
    column_name = re.args[0].attr
    if new_column_name is None:
        new_column_name = column_name
    mapping_dict = ast.literal_eval(re.args[1].value)
    if _is_pandas_df(df):
        new_column = df[column_name].replace(mapping_dict)
        df[new_column_name] = new_column
        if new_column_name != column_name:
            del df[column_name]
    elif spark_installed and _is_spark_df(df):
        mapping_expr = create_map([lit(x) for x in chain(*mapping_dict.items())])  # type: ignore
        df = df.withColumn(new_column_name, mapping_expr[df[column_name]])  # type: ignore
        if new_column_name != column_name:
            df = df.drop(column_name)
    else:
        raise ValueError(
            "function replace supports only Pandas dataframes or spark dataframes."
        )
    return new_column_name, df


def identity(df: Any, column: Expr, new_column_name: str):
    if _is_ast_subscript(column._expr):  # type: ignore
        column_name = column._expr.slice.value.s  # type: ignore
    elif _is_ast_attribute(column._expr):  # type: ignore
        column_name = column._expr.attr  # type: ignore
    else:
        raise ValueError(
            "Expression type not supported. Formats supported: it.column_name or it['column_name']."
        )

    if column_name is None or not column_name.strip():
        raise ValueError("Name of the column to be renamed cannot be None or empty.")
    if new_column_name is None or not new_column_name.strip():
        raise ValueError(
            "New name of the column to be renamed cannot be None or empty."
        )

    if _is_pandas_df(df):
        df = df.rename(columns={column_name: new_column_name})
    elif spark_installed and _is_spark_df(df):
        df = df.withColumnRenamed(column_name, new_column_name)
    else:
        raise ValueError(
            "Function identity supports only Pandas dataframes or spark dataframes."
        )
    return new_column_name, df


def ratio(df: Any, replace_expr: Expr, new_column_name: str):
    def get_column_name(column):
        if _is_ast_subscript(column):
            column_name = column.slice.value.s
        elif _is_ast_attribute(column):
            column_name = column.attr
        else:
            raise ValueError(
                "Expression type not supported. Formats supported: it.column_name or it['column_name']."
            )
        if column_name is None or not column_name.strip():
            raise ValueError("Name of the column cannot be None or empty.")
        return column_name

    numerator_col = replace_expr._expr.args[0]  # type: ignore
    denominator_col = replace_expr._expr.args[1]  # type: ignore
    numerator_col_name = get_column_name(numerator_col)
    denominator_col_name = get_column_name(denominator_col)

    if new_column_name is None or not new_column_name.strip():
        raise ValueError(
            """New name of the column to be renamed cannot be None or empty. You may want to use a dictionary
            to specify the new column name as the key, and the expression as the value."""
        )

    if _is_pandas_df(df):
        df[new_column_name] = df[numerator_col_name] / df[denominator_col_name]
    elif spark_installed and _is_spark_df(df):
        df = df.withColumn(
            new_column_name, df[numerator_col_name] / df[denominator_col_name]
        )
    else:
        raise ValueError(
            "Function identity supports only Pandas dataframes or spark dataframes."
        )
    return new_column_name, df


def subtract(df: Any, replace_expr: Expr, new_column_name: str):
    def get_column_name(column):
        if _is_ast_subscript(column):
            column_name = column.slice.value.s
        elif _is_ast_attribute(column):
            column_name = column.attr
        else:
            raise ValueError(
                "Expression type not supported. Formats supported: it.column_name or it['column_name']."
            )
        if column_name is None or not column_name.strip():
            raise ValueError("Name of the column cannot be None or empty.")
        return column_name

    op1_col = replace_expr._expr.args[0]  # type: ignore
    op2_col = replace_expr._expr.args[1]  # type: ignore
    op1_col_name = get_column_name(op1_col)
    op2_col_name = get_column_name(op2_col)

    if new_column_name is None or not new_column_name.strip():
        raise ValueError(
            """New name of the column to be renamed cannot be None or empty. You may want to use a dictionary
            to specify the new column name as the key, and the expression as the value."""
        )

    if _is_pandas_df(df):
        df[new_column_name] = df[op1_col_name] - df[op2_col_name]
    elif spark_installed and _is_spark_df(df):
        df = df.withColumn(new_column_name, df[op1_col_name] - df[op2_col_name])
    else:
        raise ValueError(
            "Function identity supports only Pandas dataframes or spark dataframes."
        )
    return new_column_name, df


def time_functions(
    df: Any, dom_expr: Expr, new_column_name: str, pandas_func: str, spark_func: str
):
    fmt = None
    de: Any = dom_expr._expr
    column_name = de.args[0].attr
    if new_column_name is None:
        new_column_name = column_name
    if len(de.args) > 1:
        fmt = ast.literal_eval(de.args[1])
    if _is_pandas_df(df):
        new_column = pd.to_datetime(df[column_name], format=fmt)
        df[new_column_name] = getattr(getattr(new_column, "dt"), pandas_func)
        if new_column_name != column_name:
            del df[column_name]
    elif spark_installed and _is_spark_df(df):
        df = df.withColumn(column_name, to_timestamp(df[column_name], fmt))  # type: ignore
        df = df.select(eval(spark_func + "(df[column_name])").alias(new_column_name))
        if new_column_name != column_name:
            df = df.drop(column_name)
    else:
        raise ValueError(
            "function day_of_month supports only Pandas dataframes or spark dataframes."
        )

    return new_column_name, df


def day_of_month(df: Any, dom_expr: Expr, new_column_name: str):
    return time_functions(df, dom_expr, new_column_name, "day", "dayofmonth")


def day_of_week(df: Any, dom_expr: Expr, new_column_name: str):
    return time_functions(df, dom_expr, new_column_name, "weekday", "dayofweek")


def day_of_year(df: Any, dom_expr: Expr, new_column_name: str):
    return time_functions(df, dom_expr, new_column_name, "dayofyear", "dayofyear")


def hour(df: Any, dom_expr: Expr, new_column_name: str):
    return time_functions(df, dom_expr, new_column_name, "hour", "spark_hour")


def minute(df: Any, dom_expr: Expr, new_column_name: str):
    return time_functions(df, dom_expr, new_column_name, "minute", "spark_minute")


def month(df: Any, dom_expr: Expr, new_column_name: str):
    return time_functions(df, dom_expr, new_column_name, "month", "spark_month")


def string_indexer(df: pd.DataFrame, dom_expr: Expr, new_column_name: str):
    de: Any = dom_expr._expr
    column_name = de.args[0].attr
    if new_column_name is None:
        new_column_name = column_name

    if _is_pandas_df(df):
        sorted_indices = df[column_name].value_counts().index
        df[new_column_name] = df[column_name].map(
            dict(zip(sorted_indices, range(0, len(sorted_indices))))
        )
        if new_column_name != column_name:
            del df[column_name]
    elif spark_installed and _is_spark_df(df):
        df = df.withColumnRenamed(
            column_name, "newColName"
        )  # renaming because inputCol and outputCol can't be the same.
        indexer = StringIndexer(inputCol="newColName", outputCol=new_column_name)
        df = indexer.fit(df).transform(df)
        df = df.drop("newColName")
    else:
        raise ValueError(
            "function day_of_month supports only Pandas dataframes or spark dataframes."
        )

    return new_column_name, df


# functions for aggregate
def grouped_sum():
    return pysql.sum


def grouped_max():
    return pysql.max


def grouped_min():
    return pysql.min


def grouped_count():
    return pysql.count


def grouped_mean():
    return pysql.mean


def grouped_first():
    return pysql.first


# functions for filter
def filter_isnan(df: Any, column_name: str):
    if _is_pandas_df(df):
        return df[df[column_name].isnull()]
    elif spark_installed and _is_spark_df(df):
        from pyspark.sql.functions import isnan

        return df.filter(isnan(df[column_name]))
    else:
        raise ValueError(
            "the filter isnan supports only Pandas dataframes or spark dataframes."
        )


def filter_isnotnan(df: Any, column_name: str):
    if _is_pandas_df(df):
        return df[df[column_name].notnull()]
    elif spark_installed and _is_spark_df(df):
        from pyspark.sql.functions import isnan

        return df.filter(~isnan(df[column_name]))
    else:
        raise ValueError(
            "the filter isnotnan supports only Pandas dataframes or spark dataframes."
        )


def filter_isnull(df: Any, column_name: str):
    if _is_pandas_df(df):
        return df[df[column_name].isnull()]
    elif spark_installed and _is_spark_df(df):
        from pyspark.sql.functions import isnull

        return df.filter(isnull(df[column_name]))
    else:
        raise ValueError(
            "the filter isnan supports only Pandas dataframes or spark dataframes."
        )


def filter_isnotnull(df: Any, column_name: str):
    if _is_pandas_df(df):
        return df[df[column_name].notnull()]
    elif spark_installed and _is_spark_df(df):
        from pyspark.sql.functions import isnull

        return df.filter(~isnull(df[column_name]))
    else:
        raise ValueError(
            "the filter isnotnan supports only Pandas dataframes or spark dataframes."
        )
