import pytest
from unittest.mock import MagicMock, Mock
import sqlite3
import wx

from f1 import Retrieve_By_Time


class MockGUI:
    def GetValue(self):
        return "2022-01-01"


@pytest.fixture
def setup_retrieve_by_time(monkeypatch):
    con = MagicMock(spec=sqlite3.Connection)
    cur = MagicMock(spec=sqlite3.Cursor)

    con.cursor.return_value = cur
    cur.fetchall.return_value = []

    monkeypatch.setattr("sqlite3.connect", lambda _: con)

    # Mock wx.App and instantiate it
    class MockApp(wx.App):
        def OnInit(self):
            return True

    mock_app = MockApp(redirect=False)
    monkeypatch.setattr(wx, 'App', MockApp)

    # Mock wx.MessageBox
    monkeypatch.setattr(wx, 'MessageBox', Mock())

    frame = Retrieve_By_Time(None)
    frame.file1 = MockGUI()
    frame.file2 = MockGUI()

    return frame, con, cur


def test_search(setup_retrieve_by_time):
    frame, _, cur = setup_retrieve_by_time

    # Mocking the GetValue methods
    frame.file1.GetValue = Mock(return_value='2022-01-01')
    frame.file2.GetValue = Mock(return_value='2023-01-01')

    frame.search(Mock())

    expected_sql = ("select * from Listings_Dec18 where id in "
                    "(select distinct listing_id from Calendar_Dec18 where "
                    "substr(date,1,4) || substr(date,6,2) || substr(date,9,2) "
                    "between '20220101' and '20230101')")

    cur.execute.assert_called_with(expected_sql)

