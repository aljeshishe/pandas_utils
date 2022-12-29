"""Sample unit test module using pytest-describe and expecter."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison
import logging

import pandas as pd

from pandas_utils import utils


def test_install(caplog):
    caplog.handler.formatter = logging.Formatter("%(levelname)s: %(name)s: %(message)s")

    utils.install()
    expected = """INFO: pandas_utils.utils: Adding new methods to DataFrame
INFO: pandas_utils.utils: reorder_columns: Add specified columns from the begining.
INFO: pandas_utils.utils: drop_from: Drop records from query_df from df.
INFO: pandas_utils.utils: drop_duplicates: Drop duplicates from dataframe.
INFO: pandas_utils.utils: d: Open dataframe in browser.
INFO: pandas_utils.utils: i: Display dataframe.
"""
    assert caplog.text == expected


def test_drop_duplicates(caplog):
    utils.install()
    caplog.clear()
    caplog.handler.formatter = logging.Formatter("%(levelname)s: %(name)s: %(message)s")

    df = pd.DataFrame({"a": [1, 2, 3, 3]})
    df = df.drop_duplicates(subset="a")
    assert df.compare(pd.DataFrame({"a": [1, 2, 3]})).empty

    expected = """DEBUG: pandas_utils.utils: Dropping duplicates
DEBUG: pandas_utils.utils: Dropping rows
DEBUG: pandas_utils.utils: 1 rows
INFO: pandas_utils.utils:    a
3  3
DEBUG: pandas_utils.utils: Rows count before:4 after_count:3
"""
    assert caplog.text == expected


def test_reorder_columns():
    utils.install()

    df = pd.DataFrame({"a": [1], "b": [2], "c": [3]})
    df = df.reorder_columns("c", "b")
    pd.testing.assert_frame_equal(df, pd.DataFrame({"c": [3], "b": [2], "a": [1]}))
