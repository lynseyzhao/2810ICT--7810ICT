# Retrieve all records that contain a keyword (user entered), e.g. pool, pet.
# Retrieve all records that contain a keyword (user entered), e.g. pool, pet.
import wx, wx.grid
import sqlite3
from support import Signal,MyGridTable


# rows number
rows = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']

class Keyword_Search(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.return_signal = Signal(name='Return Back')

        #dataset connection
        self.con = sqlite3.connect('Sydney_Airbnb.db')# connect with dataset
        self.cur = self.con.cursor()#cursor

        #initialization of windows
        self.setup_ui()
        #window close
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def setup_ui(self):
        self.sql = "select * from Listings_Dec18 limit 20"#Only present 2000 details of record, otherwise crash
        self.cur.execute(self.sql)# execute
        self.data = self.cur.fetchall() #fetchall all rows
        self.page = 0# firstpage
        self.index = rows# set index

        # panel
        self.panel = wx.Panel(self)
        # define component
        self.mainButton = wx.Button(self.panel, label='Back', size=(100, 30))
        self.text1 = wx.StaticText(self.panel, label='StartDate:',size=(60, 30))
        self.text2 = wx.StaticText(self.panel, label='EndDate:',size=(60, 30))
        self.text3 = wx.StaticText(self.panel, label='Date Format: YYY-MM-DD', size=(200, 30))
        self.text4 = wx.StaticText(self.panel, label='Range: 2018-12-07 - 2019-12-06', size=(300, 30))
        self.text5 = wx.StaticText(self.panel, label='Search for homestays that can be continuously rented within a given time period', size=(650, 30))
        self.text6 = wx.StaticText(self.panel, label='Keywords:',size=(60, 30))
        self.file1 = wx.TextCtrl(self.panel, size=(150, 30))
        self.file2 = wx.TextCtrl(self.panel, size=(150, 30))
        self.file3 = wx.TextCtrl(self.panel, size=(150, 30))
        self.searchButton = wx.Button(self.panel, label='Find', size=(100, 30))
        self.grid = wx.grid.Grid(parent=self.panel)
        self.backButton = wx.Button(self.panel, label='<', size=(40, 20))
        self.nextButton = wx.Button(self.panel, label='>', size=(40, 20))

        #table set
        self.table_set(self.data[self.page * 20: self.page * 20 + 20])
        # layout(sizer)
        self.Keyword_layout()

        # button bind
        self.mainButton.Bind(wx.EVT_BUTTON, self.back_mainWindow)
        self.searchButton.Bind(wx.EVT_BUTTON, self.search)
        self.backButton.Bind(wx.EVT_BUTTON, lambda event, page=-1: self.get_page(event, page))
        self.nextButton.Bind(wx.EVT_BUTTON, lambda event, page=1: self.get_page(event, page))

    #data retrived and layout
    def table_set(self, data):
        table = MyGridTable(data, self.index)
        self.grid.SetTable(table, True)
        self.grid.AutoSize()

    #wxWidgets
    def Keyword_layout(self):
        self.sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer4 = wx.BoxSizer(wx.VERTICAL)
        #text notes display
        self.sizer1.Add(self.text3, flag=wx.ALL, border=0)
        self.sizer1.Add(self.text4, flag=wx.ALL, border=0)
        #begin input display
        self.sizer2.AddSpacer(10)
        self.sizer2.Add(self.text1, flag=wx.ALL, border=5)
        self.sizer2.Add(self.file1, flag=wx.ALL, border=0)
        #end input display
        self.sizer2.AddSpacer(10)
        self.sizer2.Add(self.text2, flag=wx.ALL, border=5)
        self.sizer2.Add(self.file2, flag=wx.ALL, border=0)
        #keyword display
        self.sizer2.AddSpacer(10)
        self.sizer2.Add(self.text6, flag=wx.ALL, border=5)
        self.sizer2.Add(self.file3, flag=wx.ALL, border=0)
        #search and page navigation
        self.sizer2.AddSpacer(30)
        self.sizer2.Add(self.searchButton, flag=wx.ALL, border=0)
        self.sizer2.AddSpacer(30)
        self.sizer2.Add(self.mainButton, flag=wx.ALL, border=0)
        # flip page
        self.sizer3.Add(self.text5, flag=wx.ALL, border=5)
        self.sizer3.Add(self.backButton, flag=wx.ALL, border=5)
        self.sizer3.Add(self.nextButton, flag=wx.ALL, border=5)
        # vertical Display
        self.sizer4.Add(self.sizer1, flag=wx.ALL, border=0)
        self.sizer4.Add(self.sizer2, flag=wx.ALL, border=0)
        self.sizer4.Add(self.grid, flag=wx.ALL, border=0)
        self.sizer4.Add(self.sizer3, flag=wx.ALL | wx.ALIGN_RIGHT, border=0)
        # panel
        self.panel.SetSizer(self.sizer4)

    #Search/find button
    def search(self, event):
        if len(self.file1.GetValue()) == 10 and len(self.file2.GetValue()) == 10 and len(self.file1.GetValue().replace('-', '')) == 8 and len(self.file2.GetValue().replace('-', '')) == 8:
            global start, end
            start = self.file1.GetValue().split('-')[0] + self.file1.GetValue().split('-')[1] + self.file1.GetValue().split('-')[2]
            end = self.file2.GetValue().split('-')[0] + self.file2.GetValue().split('-')[1] + self.file2.GetValue().split('-')[2]
            keyword=self.file3.GetValue()
            self.sql ="select * from Listings_Dec18 where id in (select distinct listing_id from Calendar_Dec18 where substr(date,1,4) || substr(date,6,2) || substr(date,9,2) between '{}' and '{}')".format(start, end)+\
                "and (id in (select distinct listing_id from Reviews_Dec18 where comments LIKE '%{}%') ".format(keyword)+\
                "or id in (select distinct id from Listings_Dec18 where summary LIKE '%{}%') ".format(keyword)+\
                "or id in (select distinct id from Listings_Dec18 where description LIKE '%{}%') ".format(keyword)+\
                "or id in (select distinct id from Listings_Dec18 where neighborhood_overview LIKE '%{}%') ".format(keyword)+\
                "or id in (select distinct id from Listings_Dec18 where amenities LIKE '%{}%')) ".format(keyword)
            self.cur.execute(self.sql)
            self.data = self.cur.fetchall()
            l=len(self.data)
            if l == 0:
                wx.MessageBox("Not Found: Please enter value within date range / incorrect date and keywords")
            else:
                if l <20:
                    for i in range(20-l):
                        self.data.append((" ",)*95)
                self.page = 0 # first page
                self.index = rows# set index
                self.table_set(self.data[self.page: self.page + 20])# get data
        else:
            wx.MessageBox("Not Found: Please enter right date format and keywords")

    # flip page
    def get_page(self, event, page):
        if page == -1 and self.page == 0:
            pass
        elif page == 1 and int(self.index[-1]) >= len(self.data):
            pass
        else:
            self.page += page# first page
            self.index = list(map(lambda x: str(int(x) + page * 20), self.index))# index
            self.table_set(self.data[self.page * 20: self.page * 20 + 20])# get data

    #Return to main window
    def back_mainWindow(self,event):
        self.return_signal.emit()

    #close window
    def OnCloseWindow(self,event):
        wx.Exit()

if __name__ == '__main__':
    con = sqlite3.connect('Sydney_Airbnb.db')# connect with dataset
    cur = con.cursor()#cursor
    keyword="Internet,Wifi"
    sql ="select * from Listings_Dec18 where id in (select distinct listing_id from Calendar_Dec18 where substr(date,1,4) || substr(date,6,2) || substr(date,9,2) between '{}' and '{}')".format("20181207", "20181208")+\
        "and (id in (select distinct listing_id from Reviews_Dec18 where comments LIKE '%{}%') ".format(keyword)+\
        "or id in (select distinct id from Listings_Dec18 where summary LIKE '%{}%') ".format(keyword)+\
        "or id in (select distinct id from Listings_Dec18 where description LIKE '%{}%') ".format(keyword)+\
        "or id in (select distinct id from Listings_Dec18 where neighborhood_overview LIKE '%{}%') ".format(keyword)+\
        "or id in (select distinct id from Listings_Dec18 where amenities LIKE '%{}%')) ".format(keyword)
    cur.execute(sql)
    data = cur.fetchall()
    print(data[0])
