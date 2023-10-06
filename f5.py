# Show the rating of properties based on the customers’ experience and their satisfaction toward the property

import wx
import wx.grid
from support import Signal, MyGridTable5
import sqlite3

rows = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']

class Properties_Rating(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.return_signal = Signal(name='Return Back')
        self.con = sqlite3.connect('Sydney_Airbnb.db')
        self.cur = self.con.cursor()

        # Initialization
        self.setup_ui()
        # close window
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)



    def setup_ui(self):
        self.sql = "SELECT id, name, review_scores_rating, review_scores_cleanliness, number_of_reviews FROM Listings_Dec18 WHERE id IN (SELECT DISTINCT listing_id FROM Calendar_Dec18 WHERE substr(date, 1, 4) || substr(date, 6, 2) || substr(date, 9, 2) BETWEEN '{}' AND '{}')".format(
            20181207, 20181208)
        self.cur.execute(self.sql)  # execute
        self.data = self.cur.fetchall()  # fetchall all rows
        self.page = 0  # first page
        self.index = rows  # set index

        # panel
        self.panel = wx.Panel(self)

        # define component
        self.mainButton = wx.Button(self.panel, label='Back', size=(100, 30))
        self.grid = wx.grid.Grid(parent=self.panel)

        # Title text
        title_text = "Show the rating of properties based on the customers’ experience and their satisfaction toward the property"
        self.title_label = wx.StaticText(self.panel, label=title_text, style=wx.ALIGN_RIGHT)

        # Manually set the column labels
        self.grid.SetColLabelValue(0, "id")
        self.grid.SetColLabelValue(1, "name")
        self.grid.SetColLabelValue(2, "review_scores_rating")
        self.grid.SetColLabelValue(3, "review_scores_cleanliness")
        self.grid.SetColLabelValue(4, "number_of_reviews")

        self.backButton = wx.Button(self.panel, label='<', size=(40, 20))
        self.nextButton = wx.Button(self.panel, label='>', size=(40, 20))

        # Table set
        self.table_set(self.data[self.page * 20: self.page * 20 + 20])

        # Layout (sizer)
        self.Rating_layout()
        # Button bind
        self.mainButton.Bind(wx.EVT_BUTTON, self.back_mainWindow)
        self.backButton.Bind(wx.EVT_BUTTON, lambda event, page=-1: self.get_page(event, page))
        self.nextButton.Bind(wx.EVT_BUTTON, lambda event, page=1: self.get_page(event, page))

    # table data reading
    def table_set(self, data):
        # Set up the table with the extracted data
        table = MyGridTable5(data, self.index)
        self.grid.SetTable(table, True)
        self.grid.AutoSize()

    def Rating_layout(self):
        # Create a main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Create a horizontal sizer for the title
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title_sizer.Add(self.title_label, flag=wx.ALL, border=0)

        # Create a horizontal sizer for the main button
        main_button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_button_sizer.AddSpacer(20)
        main_button_sizer.Add(self.mainButton, flag=wx.ALL, border=0)

        # Add the title and main button sizers to the main sizer
        main_sizer.AddSpacer(5)
        main_sizer.Add(main_button_sizer, flag=wx.ALIGN_LEFT)
        main_sizer.Add(title_sizer, flag=wx.ALIGN_CENTER)
        main_sizer.AddSpacer(15)

        # Create a horizontal sizer for the table
        table_sizer = wx.BoxSizer(wx.HORIZONTAL)
        table_sizer.Add(self.grid, flag=wx.ALIGN_CENTER)

        # Add the table sizer to the main sizer
        main_sizer.Add(table_sizer, flag=wx.ALIGN_CENTER, border=10)  # Add a margin of 10 pixels below the table

        main_sizer.AddSpacer(15)

        # Create a horizontal sizer for the back and next buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(self.backButton, flag=wx.ALL, border=5)
        button_sizer.AddSpacer(20)  # Add space between the back and next buttons
        button_sizer.Add(self.nextButton, flag=wx.ALL, border=5)

        # Add the button sizer to the main sizer
        main_sizer.Add(button_sizer, flag=wx.ALIGN_CENTER)

        # Set the main sizer for the panel
        self.panel.SetSizer(main_sizer)

    def get_page(self, event, page):
        if page == -1 and self.page == 0:
            pass
        elif page == 1 and int(self.index[-1]) >= len(self.data):
            pass
        else:
            self.page += page  # first page
            self.index = list(map(lambda x: str(int(x) + page * 20), self.index))  # index
            self.table_set(self.data[self.page * 20: self.page * 20 + 20])  # get data

    #Return to main window
    def back_mainWindow(self,event):
        self.return_signal.emit()

    #Close window
    def OnCloseWindow(self,event):
        wx.Exit()

if __name__ == '__main__':
    con = sqlite3.connect('Sydney_Airbnb.db')
    cur = con.cursor()
    sql = "SELECT id, name, review_scores_rating, review_scores_cleanliness, number_of_reviews FROM Listings_Dec18 WHERE id IN (SELECT DISTINCT listing_id FROM Calendar_Dec18 WHERE substr(date, 1, 4) || substr(date, 6, 2) || substr(date, 9, 2) BETWEEN '{}' AND '{}')".format(
        20181207, 20181208)
    cur.execute(sql)
    data = cur.fetchall()
    print(data)
