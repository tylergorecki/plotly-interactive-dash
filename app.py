#############################################################
################# NCAA Basketball Dashboard #################
#############################################################

# import necessary packages
from dash import Dash, dash_table, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px

#############################################################
###################### Data Cleaning ########################
#############################################################

# read in and clean data
data = pd.read_csv('data.csv')

# create new column names
data.columns = ['Position', 'Height', 'EligibilityYear', 'Conference', 'ConfTier', 'Pts100', '3FG_cond', 'Reb100', 'Blk40', 'Blk40_cond', 
                'ATO_cond', '3FGpFGA', 'TV_name', 'Name', 'Reb100_cond', '3FGApFGA_cond', 'FT_cond', 'Pts100_cond', 'Team', 'ATO', '3FG', 'FT']

# drop columns of all NAs
data.drop('TV_name', axis = 1, inplace=True)

# reorder columns
data = data[['Name', 'Team', 'Position', 'Height', 'EligibilityYear', 'Conference', 'ConfTier', 
             'Pts100', 'Reb100', '3FG', '3FGpFGA', 'ATO', 'FT', 'Blk40', 
             'Pts100_cond', 'Reb100_cond', '3FG_cond', '3FGApFGA_cond', 'ATO_cond', 'FT_cond', 'Blk40_cond']]

# modify shooting percentage columns to percentage values (instead of proportions out of 1)
data['3FG'] = data['3FG'] * 100
data['FT'] = data['FT'] * 100

# remove all players that don't have an eligibility year
# this is something that I would look to fix from data source in future but no eligibility year hurts the filtering ability later on
data = data[data.EligibilityYear.isna() == False]

# also removing players without a position, only 5 (likely data connection error from combination of datasets)
data = data[data.Position.isna() == False]

# filling NA values with 0; knowing the data, players of certain position have NA values in their conditional column because we aren't worried about that stat for them
# example is 1s having NA for rebounds and blocks; can adjust for this another way later, but don't want NA values in current dataset
data = data.fillna(0)

#############################################################
######################## App Layout #########################
#############################################################

# load the css stylesheet
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# initialize app
app = Dash(__name__, external_stylesheets = stylesheets)
server = app.server

# actual layout
app.layout = html.Div([

    # dashboard title
    html.H1('NCAA Basketball Transfer Portal Dashboard'), 
    
    # filter options
    html.Div([
        # player name search box
        html.Div(
            dcc.Dropdown(
                id = 'players', 
                options = data.Name, 
                value = list(data.Name[0]), 
                multi = True
            ), 
            className = 'two columns'
        ), 

        # team name search box
        html.Div(
            dcc.Dropdown(
                id = 'teams', 
                options = data.Team, 
                value = list(data.Team[0]), 
                multi = True
            ), 
            className = 'two columns'
        ), 

        # position dropdown box (only select one, default 1s)
        html.Div(
            dcc.Dropdown(
                id = 'position', 
                options = data.Position, 
                value = list(data.Position[0]), 
                multi = False
            ), 
            className = 'two columns'
        ), 

        # conference tier dropdown (can select multiple)
        html.Div(
            dcc.Dropdown(
                id = 'conference', 
                options = data.ConfTier, 
                value = list(data.ConfTier[0]), 
                multi = True
            ), 
            className = 'two columns'
        ), 

        # eligibility dropdown (can select multiple)
        html.Div(
            dcc.Dropdown(
                id = 'eligibility', 
                options = data.EligibilityYear, 
                value = list(data.EligibilityYear[0]), 
                multi = True
            ), 
            className = 'two columns'
        )
    ]), 

    # data table from filters above
    html.Div(
        dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in sorted(df.columns)],
            sort_action="native",
            page_size=10,
            style_table={"overflowX": "auto"},
        )
    )
])
