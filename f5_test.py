import wx
import pytest
from f5 import Properties_Rating

@pytest.fixture(scope='function')
def app():
    app = wx.App(False)
    yield app
    # Cleanup
    app.Destroy()


@pytest.fixture(scope='function')
def frame(app):
    frame = Properties_Rating(None)
    yield frame
    # Cleanup
    frame.Destroy()


def test_initialization(frame):
    # Ensure that the frame is shown
    frame.Show()
    wx.Yield()
    assert frame.IsShown()


def test_setup_ui(frame):
    # Test the setup_ui function
    frame.setup_ui()
    assert frame.grid.GetNumberCols() == 5


def test_get_page(frame):
    # Test the get_page function
    frame.page = 0
    frame.index = [str(i) for i in range(1, 21)]
    frame.get_page(None, 1)
    assert frame.page == 1
    assert frame.index == [str(i) for i in range(21, 41)]


def test_main_button(frame):
    # Redefining the Signal class to accommodate 'emitted' attribute
    class Signal:
        def __init__(self, name=None):
            self.name = name
            self.emitted = False

        def connect(self, func):
            self.slot = func

        def emit(self):
            if hasattr(self, "slot"):
                self.slot()
                self.emitted = True

    # Initialize the mock signal
    frame.return_signal = Signal(name='Return Back')

    def mock_signal_handler():
        frame.return_signal.emitted = True

    # Connect the mock handler to the signal
    frame.return_signal.connect(mock_signal_handler)

    # Emitting button event
    frame.mainButton.ProcessEvent(wx.CommandEvent(wx.EVT_BUTTON.typeId, frame.mainButton.GetId()))
    wx.Yield()

    # Assertion
    assert frame.return_signal.emitted

