# Produce a chart to show the distribution of prices of properties

import wx, wx.grid
import sqlite3
import pandas as pd
from support import Signal, distros, property
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class Housing_Price_Trend(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.return_signal = Signal(name='Return Back')

        # dataset connection
        self.con = sqlite3.connect('Sydney_Airbnb.db')  # connect with dataset
        self.cur = self.con.cursor()  # cursor

        # Initialization
        self.setup_ui()
        # window close
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def setup_ui(self):
        self.data = None
        self.street = "Bondi Beach, NSW, Australia"  # street selection

        # panel
        self.panel = wx.Panel(self)
        # define component
        self.mainButton = wx.Button(self.panel, label='Back', size=(100, 30))
        self.text1 = wx.StaticText(self.panel, label='StartDate:', size=(60, 30))
        self.text2 = wx.StaticText(self.panel, label='EndDate:', size=(60, 30))
        self.text3 = wx.StaticText(self.panel, label='Date Format: YYY-MM-DD', size=(200, 30))
        self.text4 = wx.StaticText(self.panel, label='Range: 2018-12-07 - 2019-12-06', size=(300, 30))
        self.text5 = wx.StaticText(self.panel, label='Street:', size=(50, 30))
        self.file1 = wx.TextCtrl(self.panel, size=(150, 30))
        self.file2 = wx.TextCtrl(self.panel, size=(150, 30))
        # drop down menu to display all streets
        self.cb = wx.ComboBox(self.panel, choices=distros, style=wx.CB_READONLY, size=(200, 30))
        self.cb.SetSelection(0)
        self.searchButton = wx.Button(self.panel, label='Find', size=(100, 30))

        # picture initialization
        self.init_picture()

        # layout(sizer)
        self.Price_layout()

        # button bind
        self.mainButton.Bind(wx.EVT_BUTTON, self.back_mainWindow)
        self.searchButton.Bind(wx.EVT_BUTTON, self.search)
        self.cb.Bind(wx.EVT_COMBOBOX, self.OnSelect)

    # retrived street
    def OnSelect(self, e):
        self.street = e.GetString()

    # Initial picture
    def init_picture(self):
        self.figure = Figure()
        self.figure.set_figheight(5.2)
        self.figure.set_figwidth(9.8)
        self.figure.subplots_adjust(left=0.05, right=0.99, bottom=0.32, top=0.98)
        self.cannvas = FigureCanvas(self.panel, -1, self.figure)

        self.axes = self.figure.add_subplot(111)
        self.axes.set_xticks(np.arange(40))  # setting X axies range。
        self.axes.set_xticklabels(property, rotation=-90)  # setting x axies label。
        self.axes.set_xlim(left=-1, right=40, emit=True,
                           auto=False)  # setting limit,user are not able to drag the frame
        self.axes.set_ylim(0, 1000)
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)

    # picture drawing
    def draw_picture(self, mean_price):
        data = []
        for i in range(40):
            if property[i] in mean_price['price']:
                data.append(mean_price['price'][property[i]])
            else:
                data.append(0.0)
        colors = np.random.rand(40, 3)  # choosen 40 colors based on number of street
        # bar chart
        self.axes.clear()
        self.axes.set_xticks(np.arange(40))  # X-axis range
        self.axes.set_xticklabels(property, rotation=-90)  # x-axis label
        self.axes.set_xlim(left=-1, right=40, emit=True, auto=False)  # user are not able to drag the frame
        self.axes.set_ylim(0, 1000)
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        self.axes.bar(property, data, color=colors, width=0.8)
        self.cannvas.draw()  # refresh

    # wxWidgets layout
    def Price_layout(self):
        self.sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer3 = wx.BoxSizer(wx.VERTICAL)
        # text notes
        self.sizer1.Add(self.text3, flag=wx.ALL, border=0)
        self.sizer1.Add(self.text4, flag=wx.ALL, border=0)
        # begin input
        self.sizer2.AddSpacer(10)
        self.sizer2.Add(self.text1, flag=wx.ALL, border=5)
        self.sizer2.Add(self.file1, flag=wx.ALL, border=0)
        # end input
        self.sizer2.AddSpacer(5)
        self.sizer2.Add(self.text2, flag=wx.ALL, border=5)
        self.sizer2.Add(self.file2, flag=wx.ALL, border=0)
        # keyword
        self.sizer2.AddSpacer(5)
        self.sizer2.Add(self.text5, flag=wx.ALL, border=5)
        self.sizer2.Add(self.cb, flag=wx.ALL, border=2)
        # search and page navigation
        self.sizer2.AddSpacer(20)
        self.sizer2.Add(self.searchButton, flag=wx.ALL, border=0)
        self.sizer2.AddSpacer(30)
        self.sizer2.Add(self.mainButton, flag=wx.ALL, border=0)
        # vertical Display
        self.sizer3.Add(self.sizer1, flag=wx.ALL, border=0)
        self.sizer3.Add(self.sizer2, flag=wx.ALL, border=0)
        self.sizer3.Add(self.cannvas, flag=wx.ALL | wx.ALIGN_CENTRE_HORIZONTAL, border=0)
        # panel
        self.panel.SetSizer(self.sizer3)

    # search/find buttion
    def search(self, event):
        if len(self.file1.GetValue()) == 10 and len(self.file2.GetValue()) == 10 and len(
                self.file1.GetValue().replace('-', '')) == 8 and len(self.file2.GetValue().replace('-', '')) == 8:
            global start, end
            start = self.file1.GetValue().split('-')[0] + self.file1.GetValue().split('-')[1] + \
                    self.file1.GetValue().split('-')[2]
            end = self.file2.GetValue().split('-')[0] + self.file2.GetValue().split('-')[1] + \
                  self.file2.GetValue().split('-')[2]
            self.sql = "select property_type , price from Listings_Dec18 where id in (select distinct listing_id from Calendar_Dec18 where substr(date,1,4) || substr(date,6,2) || substr(date,9,2) between '{}' and '{}')".format(
                start, end) + \
                       "and id in (select id from Listings_Dec18 where street LIKE '%{}%') ".format(self.street)
            self.cur.execute(self.sql)
            self.data = self.cur.fetchall()
            if len(self.data) == 0:
                wx.MessageBox("Not Found: Please enter value within date range / incorrect date")
            else:
                property_price = pd.DataFrame(self.data, columns=['property_type', 'price'])
                property_price["price"] = property_price["price"].map(
                    lambda x: float(x.replace("$", "").replace(",", "")), na_action='ignore')
                mean_price = property_price.groupby('property_type').mean()
                self.draw_picture(mean_price)
        else:
            wx.MessageBox("Not Found: Please enter right date format")

    # Return to main
    def back_mainWindow(self, event):
        self.return_signal.emit()

    # Close window
    def OnCloseWindow(self, event):
        wx.Exit()


if __name__ == '__main__':
    con = sqlite3.connect('Sydney_Airbnb.db')  # connect with dataset
    cur = con.cursor()  # cursor
    street = 'Sydney Olympic Park, NSW, Australia'
    sql = "select property_type , price from Listings_Dec18 where id in (select distinct listing_id from Calendar_Dec18 where substr(date,1,4) || substr(date,6,2) || substr(date,9,2) between '{}' and '{}')".format(
        "20181207", "20181208") + \
          "and id in (select id from Listings_Dec18 where street LIKE '%{}%') ".format(street)
    cur.execute(sql)
    data = cur.fetchall()
    data1 = pd.DataFrame(data, columns=['property_type', 'price'])
    data1["price"] = data1["price"].map(lambda x: float(x.replace("$", "").replace(",", "")), na_action='ignore')
    mean_price = data1.groupby('property_type').mean()
    print(mean_price)
    data2 = []
    for i in range(40):
        if property[i] in mean_price['price']:
            data2.append(mean_price['price'][property[i]])
        else:
            data2.append(0.0)
    print(data2)
