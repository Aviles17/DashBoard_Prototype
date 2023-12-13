from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from components.kpi import kpi
import data_functions as dt
import graph_functions as gf

def xrpusdt_page_layout():
    global df
    df = dt.get_data('XRPUSDT','15')
    df = dt.CalculateSupertrend(df)
    df = dt.get_clean_data(df)
    
    graph1 = dcc.Graph(
        figure=gf.create_supertrend_graph(df,'XRPUSDT')
    )
    # Create a dropdown for user input
    user_input = dcc.Dropdown(
        id='user-input',
        options=[
            {'label': 'Long Orders', 'value': 'Long'},
            {'label': 'Short Orders', 'value': 'Short'}
        ],
         style={"color":"black"}
    )
    
    global graph_3 
    global kpi5, kpi6, kpi7, kpi8
    
    graph_3 = dcc.Graph(
        id="graph_3",
        figure = gf.create_order_graph(df,0,0,'XRPUSDT', None)
    )
    
    kpi5 = kpi("KPI 1", "Value 1",5)
    kpi6 = kpi("KPI 2", "Value 2",6)
    kpi7 = kpi("KPI 3", "Value 3",7)
    kpi8 = kpi("KPI 4", "Value 4",8)
    
    title = html.H2("XRP/USDT Positions")
    
    # Define the overall layout of the page
    layout = dbc.Container([
        dbc.Row([
            dbc.Col(graph1),  # Place static graph_1 in a single column
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col(title, md=12),  # Place the title in a single column
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(user_input, md=4),  # Place the dropdown in the first column
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(graph_3),  # Place graph_2 in the first column
        ], id='graph-2-container', className="mb-4"),  # Container for graph_2

        dbc.Row([
            dbc.Col(kpi5.display(), md=3),  # Place KPI 1 in the first column
            dbc.Col(kpi6.display(), md=3),  # Place KPI 2 in the second column
            dbc.Col(kpi7.display(), md=3),  # Place KPI 3 in the third column
            dbc.Col(kpi8.display(), md=3),  # Place KPI 4 in the fourth column
        ])
    ], style={'width': '90%'})
    
    return layout
    
# Define a callback to show/hide graph_2 and KPIs based on user input
@callback(
    [Output('graph_3', 'figure'),
    Output('kpi5', 'children'),
    Output('kpi6', 'children'),
    Output('kpi7', 'children'),
    Output('kpi8', 'children')],
    Input('user-input', 'value'),
    prevent_initial_call=True
)
def update_content(user_input):
    if user_input == 'Long':
        size, entry, stoploss, pyl = dt.get_position("Buy",'XRPUSDT',df)
        figure_3 = gf.create_order_graph(df,float(entry),float(stoploss),'XRPUSDT','Buy')
        graph_3 = {
            'data': figure_3.data,
            'layout': figure_3.layout
        }
        kpi5.set_data("Order Size", size)
        kpi6.set_data("P&L %", pyl)
        kpi7.set_data("Entry - Profit", entry)
        kpi8.set_data("Stoploss",stoploss)
        return graph_3, kpi5.display(), kpi6.display(), kpi7.display(), kpi8.display()
        
    elif user_input == 'Short':
        size, entry, stoploss, pyl = dt.get_position("Sell",'XRPUSDT',df)
        figure_3 = gf.create_order_graph(df,float(entry),float(stoploss),'XRPUSDT','Sell')
        graph_3 = {
            'data': figure_3.data,
            'layout': figure_3.layout
        }
        kpi5.set_data("Order Size", size)
        kpi6.set_data("P&L %", pyl)
        kpi7.set_data("Entry - Profit", entry)
        kpi8.set_data("Stoploss",stoploss)
        return graph_3, kpi5.display(), kpi6.display(), kpi7.display(), kpi8.display()
    else:
        # Handle any other cases here
        graph_3 = None  # Set to None or an empty figure if needed
        kpi5.set_data("Order Size", "")
        kpi6.set_data("P&L %", "")
        kpi7.set_data("Entry - Profit", "")
        kpi8.set_data("Stoploss", "")
        return graph_3, kpi5.display(), kpi6.display(), kpi7.display(), kpi8.display()