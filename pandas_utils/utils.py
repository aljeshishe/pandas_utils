import logging
from typing import Hashable, Literal, Sequence, Union

import dtale
import pandas as pd

log = logging.getLogger(__name__)


def drop_from(query_df: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:
    """Drop records from query_df from df.

    params:
        query_df: dataframe to drop from df
    """
    before_count = len(df)
    after_df = df.drop(query_df.index)
    after_count = len(after_df)

    log.debug("Dropping rows")
    i(query_df)
    log.debug("Rows count before:%d after_count:%d", before_count, after_count)

    return after_df


def drop_duplicates(
    df: pd.DataFrame,
    subset: Union[Hashable, Sequence[Hashable], None] = None,
    keep: Literal["first", "last", False] = "first",
) -> pd.DataFrame:
    """Drop duplicates from dataframe.

    params:
        subset : column label or sequence of labels, optional
            Only consider certain columns for identifying duplicates, by
            default use all of the columns.
        keep : {'first', 'last', False}, default 'first'
            Determines which duplicates (if any) to mark.

            - ``first`` : Mark duplicates as ``True`` except for the first occurrence.
            - ``last`` : Mark duplicates as ``True`` except for the last occurrence.
            - False : Mark all duplicates as ``True``.

    returns:
        Series
            Boolean series for each duplicated rows.
    """

    log.debug("Dropping duplicates")
    duplicates_df = df[df.duplicated(subset=subset, keep=keep)]
    return drop_from(duplicates_df, df)


def reorder_columns(self, *columns: list[str]) -> pd.DataFrame:
    """Add specified columns from the begining.

    params:
        columns: list of columns to add to the begining

    returns:
        dataframe with columns reordered
    """
    new_columns = list(columns) + [item for item in self.columns if item not in columns]
    return self[new_columns]


def d(df: pd.DataFrame) -> None:
    """Open dataframe in browser."""
    dtale.show(df).open_browser()


def i(df: pd.DataFrame, count: int = 5) -> None:
    """Display dataframe.

    params:
        df: dataframe to display
        count: number of rows to display
    """
    log.debug("%d rows", len(df))
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
    doc = ""
    if method is not None:
        doc = method.__doc__.splitlines()[0].strip()
    return f"{name}: {doc}"
