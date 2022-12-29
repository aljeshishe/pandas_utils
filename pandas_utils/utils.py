import logging

import dtale
from typing import Hashable, Literal, Sequence, Union

import pandas as pd

log = logging.getLogger(__name__)


def drop_from(query_df: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop records from query_df from df
    """
    before_count = len(df)
    after_df = df.drop(query_df.index)
    after_count = len(after_df)

    log.debug(f"Dropping rows")
    i(query_df)
    log.debug(f"Rows count before:{before_count} after_count:{after_count}")

    return after_df


def drop_duplicates(
    df: pd.DataFrame,
    subset: Union[Hashable, Sequence[Hashable], None] = None,
    keep: Literal["first", "last", False] = "first",
) -> pd.DataFrame:
    """
    Drop duplicates from dataframe
    """

    log.debug(f"Dropping duplicates")
    duplicates_df = df[df.duplicated(subset=subset, keep=keep)]
    return drop_from(duplicates_df, df)


def reorder_columns(self, *columns) -> pd.DataFrame:
    """
    Add specified columns from the begining
    """
    new_columns = list(columns) + [item for item in self.columns if item not in columns]
    return self[new_columns]


def d(df) -> None:
    """
    Open dataframe in browser
    """
    dtale.show(df).open_browser()


def i(df: pd.DataFrame, count: int = 5) -> None:
    """
    Display dataframe
    """
    log.debug(f"{len(df)} rows")
    display = globals().get("display", log.info)
    display(df.head(count))


def install() -> None:
    methods = ["reorder_columns", "drop_from", "drop_duplicates", "d", "i"]
    log.info("Adding new methods to DataFrame")
    for method in methods:
        func = globals()[method]
        setattr(pd.core.frame.DataFrame, method, func)
        log.info(_describe_method(func))


def _describe_method(method) -> str:
    name = method.__name__
    doc = method.__doc__.strip() if method.__doc__ is not None else ""
    return f"{name}: {doc}"
