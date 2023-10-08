import pytest
import wx
from f2 import Housing_Price_Trend

mock_mean_price = {'price': {'Entire home/apt': 200.0, 'Private room': 100.0}}

app = wx.App(False)

@pytest.fixture
def frame():
    frame = Housing_Price_Trend(None, title='Housing Price Trend')
    frame.Show()
    yield frame
    frame.Destroy()

def test_file1(frame):
    # Test if file1 exists and if it can be set and get values
    assert hasattr(frame, 'file1')
    frame.file1.SetValue("2021-10-01")
    assert frame.file1.GetValue() == "2021-10-01"

def test_file2(frame):
    # Test if file2 exists and if it can be set and get values
    assert hasattr(frame, 'file2')
    frame.file2.SetValue("2021-10-31")
    assert frame.file2.GetValue() == "2021-10-31"

def test_draw_picture(frame):
    # Test if draw_picture exists and if it can be called with mock_mean_price
    assert hasattr(frame, 'draw_picture')
    frame.draw_picture(mock_mean_price)

def test_search(frame):
    # Test if search exists and if it can be triggered by an event
    assert hasattr(frame, 'search')
    frame.file1.SetValue("2021-10-01")
    frame.file2.SetValue("2021-10-31")
    search_event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, frame.searchButton.GetId())
    frame.GetEventHandler().ProcessEvent(search_event)

def test_back_mainWindow(frame):
    # Test if back_mainWindow exists and if it can be triggered by an event
    assert hasattr(frame, 'back_mainWindow')
    back_event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, frame.mainButton.GetId())
    frame.GetEventHandler().ProcessEvent(back_event)
