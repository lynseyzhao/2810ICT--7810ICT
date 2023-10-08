import pytest
import sqlite3
import wx
from f3 import Keyword_Search


@pytest.fixture
def keyword_search():
    app = wx.App(False)
    return Keyword_Search(None)


@pytest.fixture
def mock_connection(mocker):
    # Mocking the cursor method to return another mock object
    mock_cursor = mocker.Mock()
    mock_connection = mocker.Mock()
    mock_connection.cursor.return_value = mock_cursor

    return mock_connection, mock_cursor

def test_search_db_call(mocker, keyword_search, mock_connection):
    mock_con, mock_cursor = mock_connection
    mocker.patch('f3.sqlite3.connect', return_value=mock_con)
    mocker.patch('f3.wx.MessageBox')

    mocker.patch.object(keyword_search.file1, 'GetValue', return_value='2018-12-07')
    mocker.patch.object(keyword_search.file2, 'GetValue', return_value='2019-12-06')
    mocker.patch.object(keyword_search.file3, 'GetValue', return_value='pool')

    try:
        keyword_search.search(None)
    except Exception as e:
        print("Exception during search:", str(e))

    print("file1 value:", keyword_search.file1.GetValue())
    print("file2 value:", keyword_search.file2.GetValue())
    print("SQL Query Used:", keyword_search.sql)

    expected_sql = """select * from Listings_Dec18 where id in (select distinct listing_id from Calendar_Dec18 where substr(date,1,4) || substr(date,6,2) || substr(date,9,2) between '20181207' and '20191206')and (id in (select distinct listing_id from Reviews_Dec18 where comments LIKE '%pool%') or id in (select distinct id from Listings_Dec18 where summary LIKE '%pool%') or id in (select distinct id from Listings_Dec18 where description LIKE '%pool%') or id in (select distinct id from Listings_Dec18 where neighborhood_overview LIKE '%pool%') or id in (select distinct id from Listings_Dec18 where amenities LIKE '%pool%'))"""

    assert keyword_search.sql.strip() == expected_sql.strip(), "Mismatch in SQL Query"

    try:
        mock_cursor.execute.assert_called_once_with(expected_sql)
        mock_cursor.fetchall.assert_called_once()
    except AssertionError as ae:
        print("Assertion error:", str(ae))
        print("SQL queries executed:", [call[0][0] for call in mock_cursor.execute.call_args_list])
        raise

