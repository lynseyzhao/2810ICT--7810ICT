# Analysing how many customers commented on factors related to cleanliness

import wx, wx.grid
import sqlite3
import pandas as pd
from support import Signal
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class Cleanliness_Analysing(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.return_signal = Signal(name='Return Back')

        # dataset connection
        self.con = sqlite3.connect('Sydney_Airbnb.db')  
        self.cur = self.con.cursor() 

        # Initialization
        self.setup_ui()
        # window close
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        # Automatically display results for the default keyword
        default_keyword = self.cleanliness_keywords[0]
        self.update_chart(default_keyword)  # Update the chart with the default keyword

    def setup_ui(self):
        # Define keywords related to cleanliness
        self.cleanliness_keywords = ["clean", "tidy", "fresh", "neat", "spotless", "hygienic", "nice", "organized",
                                     "fresh air", "healthy", "bright", "flawless", "pure"]

        # panel
        self.panel = wx.Panel(self)

        # Define a label for the cleanliness dropdown
        cleanliness_label = wx.StaticText(self.panel, label="Cleanliness Keyword:")

        # Create a dropdown menu for cleanliness keywords
        self.cleanliness_dropdown = wx.ComboBox(self.panel, choices=self.cleanliness_keywords, style=wx.CB_READONLY,
                                                size=(200, 30))
        self.cleanliness_dropdown.SetSelection(0)  # Set the default selection

        # Define component
        self.mainButton = wx.Button(self.panel, label='Back', size=(100, 30))

        # picture initialization
        self.init_picture()

        button_and_dropdown_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_and_dropdown_sizer.Add(self.mainButton, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        button_and_dropdown_sizer.AddSpacer(500)  
        button_and_dropdown_sizer.Add(cleanliness_label, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=0)
        button_and_dropdown_sizer.Add(self.cleanliness_dropdown, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)

        # Create a vertical sizer for text inputs and the combined button and dropdown sizer
        input_and_button_sizer = wx.BoxSizer(wx.VERTICAL)
        input_and_button_sizer.Add(button_and_dropdown_sizer, flag=wx.ALL | wx.ALIGN_RIGHT, border=5)

        # Create a vertical sizer for the entire layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(input_and_button_sizer, flag=wx.ALL, border=0)
        main_sizer.Add(self.cannvas, flag=wx.ALL | wx.ALIGN_CENTRE_HORIZONTAL, border=0)

        self.panel.SetSizer(main_sizer)

        self.mainButton.Bind(wx.EVT_BUTTON, self.back_mainWindow)
        self.cleanliness_dropdown.Bind(wx.EVT_COMBOBOX, self.OnSelectCleanlinessKeyword)

    def OnSelectCleanlinessKeyword(self, event):
        selected_keyword = self.cleanliness_dropdown.GetStringSelection()
        self.update_chart(selected_keyword)

    def update_chart(self, selected_keyword):
        listings_data = pd.read_csv('dataset/listings_dec18.csv', usecols=['id', 'name', 'property_type'])
        reviews_data = pd.read_csv('dataset/reviews_dec18.csv', usecols=['listing_id', 'reviewer_name', 'comments'])

        # Merge data based on 'listing_id' column
        merged_data = pd.merge(reviews_data, listings_data, left_on='listing_id', right_on='id')

        # Fill missing values in the 'comments' column with an empty string
        merged_data['comments'] = merged_data['comments'].fillna('')

        # Create a new column to check if the comment contains the selected keyword
        merged_data['contains_keyword'] = merged_data['comments'].str.contains(selected_keyword, case=False)

        # Group by 'property_type' and count the number of unique reviewers containing the keyword
        mentions_by_type = merged_data[merged_data['contains_keyword']].groupby('property_type')[
            'reviewer_name'].nunique().reset_index()
        mentions_by_type.rename(columns={'reviewer_name': 'number_of_people'}, inplace=True)

        # Update the chart with the new data
        self.draw_chart(mentions_by_type, selected_keyword)

    def draw_chart(self, data, selected_keyword):
        self.figure.clf()
        ax = self.figure.add_subplot(111)

        property_types = data['property_type']
        number_of_people = data['number_of_people']

        # Create a bar chart
        ax.bar(property_types, number_of_people)
        ax.set_xlabel('Property Type')
        ax.set_ylabel('Number of People')
        ax.set_title('Number of People Mentioning Cleanliness Keyword In Customer Review: {}'.format(selected_keyword))
        ax.legend(['Number of People'])

        # Set x-axis tick positions and labels
        x_ticks = np.arange(len(property_types))
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(property_types, rotation=90, ha='center')

        self.cannvas.draw()  

    # Initial picture
    def init_picture(self):
        property_names = ['Apartment',
                    'House',
                    'Townhouse',
                    'Condominium',
                    'Guest suite',
                    'Guesthouse',
                    'Villa',
                    'Loft',
                    'Serviced apartment',
                    'Bed and breakfast',
                    'Bungalow',
                    'Cottage',
                    'Boutique hotel',
                    'Other',
                    'Hostel',
                    'Cabin',
                    'Hotel',
                    'Boat',
                    'Tiny house',
                    'Tent',
                    'Camper/RV',
                    'Farm stay',
                    'Chalet',
                    'Aparthotel',
                    'Resort',
                    'Yurt',
                    'Hut',
                    'Casa particular(Cuba)',
                    'Island',
                    'Campsite',
                    'Earth house',
                    'Heritage hotel(India)',
                    'Tipi',
                    'Treehouse',
                    'Nature lodge',
                    'Train',
                    'Castle',
                    'Barn',
                    'Cave',
                    'Dome house']
        self.figure = Figure()
        #self.figure.tight_layout()
        self.figure.set_figheight(5.5)
        self.figure.set_figwidth(9.8)
        self.figure.subplots_adjust(left=0.09, right=0.99, bottom=0.37, top=0.92)
        self.cannvas = FigureCanvas(self.panel, -1, self.figure)

        self.axes = self.figure.add_subplot(111)
        self.axes.set_xticks(np.arange(40))  
        self.axes.set_xticklabels(property_names, rotation=-90) 
        self.axes.set_xlim(left=-1, right=40, emit=True, auto=False)  
        self.axes.set_ylim(0, 1000)
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)

    # wxWidgets layout
    def Comment_layout(self):
        self.sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer3 = wx.BoxSizer(wx.VERTICAL)

        self.sizer2.AddSpacer(30)
        self.sizer2.Add(self.mainButton, flag=wx.ALL, border=0)

        # vertical Display
        self.sizer3.Add(self.sizer1, flag=wx.ALL, border=0)
        self.sizer3.Add(self.sizer2, flag=wx.ALL, border=0)
        self.sizer3.Add(self.cannvas, flag=wx.ALL | wx.ALIGN_CENTRE_HORIZONTAL, border=0)

        # panel
        self.panel.SetSizer(self.sizer3)

    # Return to main
    def back_mainWindow(self, event):
        self.return_signal.emit()

    # Close window
    def OnCloseWindow(self, event):
        wx.Exit()


if __name__ == '__main__':
    # Load data from CSV files (replace with your actual file paths)
    listings_data = pd.read_csv('/dataset/listings_dec18.csv', usecols=['id', 'name', 'property_type'])
    reviews_data = pd.read_csv('/dataset/reviews_dec18.csv', usecols=['listing_id', 'comments'])

    # Merge data based on 'listing_id' column
    merged_data = pd.merge(reviews_data, listings_data, left_on='listing_id', right_on='id')

    # Group by 'property_type' and calculate mean review scores
    mean_review_scores_by_type = merged_data.groupby('property_type')['contains_keyword'].mean().reset_index()
    mean_review_scores_by_type.rename(columns={'contains_keyword': 'number_of_mentions'}, inplace=True)

    # Create the wxPython app
    app = wx.App(False)
    frame = Cleanliness_Analysing(None, title="Cleanliness Analysis", size=(800, 600))
    frame.Show()
    app.MainLoop()
