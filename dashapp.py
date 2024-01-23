# This is being followed from the video below:
# https://www.youtube.com/watch?v=hSPmj7mK6ng
import dash
import pandas as pd
from dash import dcc
from dash import html
from dash.dependencies import Input,Output
import plotly.express as px
# import plotly.graph_objects as go
# Video says you can build the figure with graph_objects but he predicts it will be (mostly) obsolete soon


app = dash.Dash(__name__)


# -------- Data prep
df = pd.read_csv('intro_bees.csv')

df = df.groupby(['State','ANSI','Affected by','Year','state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
print('Some entries of the dataframe are given by')
print(df[:4])
print("Now we'll start with the app...\n")

# -------- App layout

app.layout = html.Div([
    html.H1('Web Application Dashboards with Dash',style={'text-align':'center'}),

    dcc.Dropdown(id='slct_year',
                 options = [
                     {"label":"2015","value":2015},
                     {"label":"2016","value":2016},
                     {"label":"2017","value":2017},
                     {"label":"2018","value":2018}
                 ],multi=False,value=2015,style={'width':"40%"}),
    html.Div(id='output_container',children = []), # Right now the children slot is empty. I think it holds some intermediary calculation step
    html.Br(),
    dcc.Graph(id='my_bee_map',figure = {}) # Right now the figure is empty. However, I think the script fills it in with the map!

])

# -------- Callbacks connect interface to data I think
# For each output you need an Output(). For each input you need an Input()
@app.callback(
    [Output(component_id='output_container',component_property='children'), # Connects the Div(id='output_container...') with children
    # Why are the above children necessary?
    Output(component_id='my_bee_map',component_property='figure')], # Connects the Graph(id='my_bee_map...') with figure
    [Input(component_id='slct_year',component_property='value')] # Formalizes the dropdown selection as an input
) # Outputs in one list, inputs in the other.

# ... have to put a function under each callback...

def update_graph(option_slctd):
    container = f'The year chosen was {option_slctd}'
    dff = df.copy()
    dff = dff[dff['Year'] == option_slctd] # Filters out all dataframe rows without Year matching option_slctd
    dff = dff[dff['Affected by'] == 'Varroa_mites'] # Filters out all dataframe rows without Affected by matching Varroa_mites

    # Defining fig with plotly express
    fig = px.choropleth(
        data_frame = dff,
        locationmode = 'USA-states',
        locations = 'state_code',
        scope = 'usa',
        color = 'Pct of Colonies Impacted',
        hover_data = ['State', 'Pct of Colonies Impacted'],
        color_continuous_scale = px.colors.sequential.YlOrRd,
        labels = {'Pct of Colonies Impacted':'Pct of Bee Colonies'},
        template = 'plotly_dark'
    )

    # Challenge: Make a bar chart instead of a map. 
    # fig = px.bar(dff,x = 'State', y = 'Pct of Colonies Impacted')



    return container, fig # What you return here is going into the outputs!!
    # We have two outputs [children and figure] so we return two things. If we had three outputs we'd return three things!


# ---- Actually run the damn thing
if __name__ == '__main__':
    app.run_server(debug=True)

