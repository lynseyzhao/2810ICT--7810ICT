import wx, wx.grid
from support import Signal

class Selection_Window(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.Time_signal = Signal(name='Retrieve By Time')
        self.Price_signal = Signal(name='Housing Price Trend')
        self.Keyword_signal = Signal(name='Keyword Search')
        self.Cleanliness_signal = Signal(name='Analyse Cleanliness')
        self.Rating_signal = Signal(name='Properties Rating')
        self.setup_ui()

        #close window
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def setup_ui(self):
        # panel
        self.panel = wx.Panel(self)

        # layout \VERTICAL\HORIZONTAL
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # components
        self.button1 = wx.Button(self.panel, label='Retrieve By Time', size=(200, 100))
        self.button2 = wx.Button(self.panel, label='Housing Price Trend', size=(200, 100))
        self.button3 = wx.Button(self.panel, label='Keyword Search', size=(200, 100))
        self.button4 = wx.Button(self.panel, label='Analyse Cleanliness', size=(200, 100))
        self.button5 = wx.Button(self.panel, label='Properties Rating', size=(200, 100))

        # add sizer
        # self.sizer.AddSpacer(10) (35)
        self.sizer.Add(self.button1, proportion=0, flag=wx.ALL | wx.CENTER, border=15)
        self.sizer.Add(self.button2, proportion=0, flag=wx.ALL | wx.CENTER, border=15)
        self.sizer.Add(self.button3, proportion=0, flag=wx.ALL | wx.CENTER, border=15)
        self.sizer.Add(self.button4, proportion=0, flag=wx.ALL | wx.CENTER, border=15)
        self.sizer.Add(self.button5, proportion=0, flag=wx.ALL | wx.CENTER, border=15)

        # button bind
        self.button1.Bind(wx.EVT_BUTTON, self.Retrieve_By_Time_show)
        self.button2.Bind(wx.EVT_BUTTON, self.Housing_Price_Trend_show)
        self.button3.Bind(wx.EVT_BUTTON, self.Keyword_Search_show)
        self.button4.Bind(wx.EVT_BUTTON, self.Cleanliness_Analysing_show)
        self.button5.Bind(wx.EVT_BUTTON, self.Properties_Rating_show)

        # panel set
        self.panel.SetSizer(self.sizer)

    #time signal pass
    def Retrieve_By_Time_show(self,event):
        self.Time_signal.emit()

    # price signal pass
    def Housing_Price_Trend_show(self,event):
        self.Price_signal.emit()

    # keyword signal pass
    def Keyword_Search_show(self,event):
        self.Keyword_signal.emit()

    def Cleanliness_Analysing_show(self, event):
        self.Cleanliness_signal.emit()

    def Properties_Rating_show(self, event):
        self.Rating_signal.emit()

    #close window
    def OnCloseWindow(self,event):
        wx.Exit()

if __name__ == '__main__':
    app = wx.App  # create app
    app.MainLoop()  # Main loop application
