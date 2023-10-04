import wx
import wx.grid
from Selection_Window import Selection_Window
from f1 import Retrieve_By_Time
from f2 import Housing_Price_Trend
from f3 import Keyword_Search
# from f4 import Cleanliness_Analysing
from f5 import Properties_Rating


class App(wx.App):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        #four windows display
        self.Selection_Window=Selection_Window(None, title="Property Information Retrieval",pos=(100,100),size=(1000, 630))
        self.Time_Window = Retrieve_By_Time(None, title="Retrieve By Time", pos=(100,100), size=(1000, 630))
        self.Price_Window = Housing_Price_Trend(None, title="Housing Price Trend",pos=(100,100),size=(1000, 630))
        self.Keyword_Window = Keyword_Search(None, title="Keyword Search",pos=(100,100),size=(1000, 630))
        # self.Cleanliness_Window = Cleanliness_Analysing(None, title="Analysing Properties Cleanliness", pos=(200,100),size=(1000, 630))
        self.Rating_Window = Properties_Rating(None, title="Properties Rating", pos=(100,100),size=(1000, 630))

        #switch from main to other windows
        self.Selection_Window.Time_signal.connect(self.Time_Window_show)
        self.Selection_Window.Price_signal.connect(self.Price_Window_show)
        self.Selection_Window.Keyword_signal.connect(self.Keyword_Window_show)
        # self.Selection_Window.Cleanliness_signal.connect(self.Cleanliness_Window_show)
        self.Selection_Window.Rating_signal.connect(self.Rating_Window_show)

        #Return to main windows
        self.Time_Window.return_signal.connect(self.Selection_Window_show)
        self.Price_Window.return_signal.connect(self.Selection_Window_show)
        self.Keyword_Window.return_signal.connect(self.Selection_Window_show)
        # self.Cleanliness_Window.return_signal.connect(self.Selection_Window_show)
        self.Rating_Window.return_signal.connect(self.Selection_Window_show)

        #windows display
        self.Selection_Window.Show()
        self.previousWindow = self.Selection_Window

    # Main windows
    def Selection_Window_show(self):
        self.Selection_Window.Show()
        self.previousWindow.Hide()
        self.previousWindow = self.Selection_Window

    #Time windows
    def Time_Window_show(self):
        self.Time_Window.Show()
        self.previousWindow.Hide()
        self.previousWindow = self.Time_Window

    #Price windows
    def Price_Window_show(self):
        self.Price_Window.Show()
        self.previousWindow.Hide()
        self.previousWindow = self.Price_Window

    #Keyword windows
    def Keyword_Window_show(self):
        self.Keyword_Window.Show()
        self.previousWindow.Hide()
        self.previousWindow = self.Keyword_Window

    #Cleanliness windows
    #def Cleanliness_Window_show(self):
    #    self.Cleanliness_Window.Show()
    #    self.previousWindow.Hide()
    #    self.previousWindow = self.Cleanliness_Window

    #Rating windows
    def Rating_Window_show(self):
        self.Rating_Window.Show()
        self.previousWindow.Hide()
        self.previousWindow = self.Rating_Window

if __name__ == '__main__':
    app = App()  # create app
    app.MainLoop()  # main loop application
