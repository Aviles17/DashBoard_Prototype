from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from components.kpi import kpi
import Util.data_functions as dt
import Util.graph_functions as gf

def oneusdt_page_layout():
    # Define the layout for ONE/USDT page
    global df
    df = dt.get_data('ONEUSDT','15')
    df = dt.CalculateSupertrend(df)
    df = dt.get_clean_data(df)
    
    # Create two empty Divs for the graphs, you can insert your Plotly graphs here
    graph1 = dcc.Graph(
        id='graph1',
        figure=gf.create_supertrend_graph(df,'ONEUSDT')
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
    
    global graph_2 
    global kpi1, kpi2, kpi3, kpi4
    
    graph_2 = dcc.Graph(
        id="graph_2",
        figure = gf.create_order_graph(df,0,0,'ONEUSDT', None)
    )
    
    kpi1 = kpi("KPI 1", "Value 1",1)
    kpi2 = kpi("KPI 2", "Value 2",2)
    kpi3 = kpi("KPI 3", "Value 3",3)
    kpi4 = kpi("KPI 4", "Value 4",4)
    
    title2 = html.H3("ONE/USDT Positions")
    title1 = html.H3("ONE/USDT Live Chart")
        
    # Define the overall layout of the page
    layout = dbc.Container([
        dcc.Interval(
        id='graph1-update-interval',
        interval=60*1000,  # Update every 5 minutes (in milliseconds)
        n_intervals=0,
        ),
        dbc.Row([
            dbc.Col(title1, md=12),  # Place the title in a single column
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col(graph1),  # Place static graph_1 in a single column
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col(title2, md=12),  # Place the title in a single column
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(user_input, md=4),  # Place the dropdown in the first column
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(graph_2),  # Place graph_2 in the first column
        ], id='graph-2-container', className="mb-4"),  # Container for graph_2

        dbc.Row([
            dbc.Col(kpi1.display(), md=3),  # Place KPI 1 in the first column
            dbc.Col(kpi2.display(), md=3),  # Place KPI 2 in the second column
            dbc.Col(kpi3.display(), md=3),  # Place KPI 3 in the third column
            dbc.Col(kpi4.display(), md=3),  # Place KPI 4 in the fourth column
        ])
    ], style={'width': '100%', 'padding': '20px'})
    
    return layout
    
# Define a callback to show/hide graph_2 and KPIs based on user input
@callback(
    [Output('graph_2', 'figure'),
    Output('kpi1', 'children'),
    Output('kpi2', 'children'),
    Output('kpi3', 'children'),
    Output('kpi4', 'children')],
    Input('user-input', 'value'),
    prevent_initial_call=True
)
def update_content(user_input):
    if user_input == 'Long':
        size, entry, stoploss, pyl = dt.get_position("Buy",'ONEUSDT',df)
        figure_2 = gf.create_order_graph(df,float(entry),float(stoploss),'ONEUSDT', 'Buy')
        graph_2 = {
            'data': figure_2.data,
            'layout': figure_2.layout
        }
        kpi1.set_data("Order Size", size)
        kpi2.set_data("P&L %", pyl)
        kpi3.set_data("Entry - Profit", entry)
        kpi4.set_data("Stoploss",stoploss)
        return graph_2, kpi1.display(), kpi2.display(), kpi3.display(), kpi4.display()
        
    elif user_input == 'Short':
        size, entry, stoploss, pyl = dt.get_position("Sell",'ONEUSDT',df)
        figure_2 = gf.create_order_graph(df,float(entry),float(stoploss),'ONEUSDT', 'Sell')
        graph_2 = {
            'data': figure_2.data,
            'layout': figure_2.layout
        }
        kpi1.set_data("Order Size", size)
        kpi2.set_data("P&L %", pyl)
        kpi3.set_data("Entry - Profit", entry)
        kpi4.set_data("Stoploss",stoploss)
        return figure_2, kpi1.display(), kpi2.display(), kpi3.display(), kpi4.display()
    else:
        # Handle any other cases here
        graph_2 = None  # Set to None or an empty figure if needed
        kpi1.set_data("Order Size", "")
        kpi2.set_data("P&L %", "")
        kpi3.set_data("Entry - Profit", "")
        kpi4.set_data("Stoploss", "")
        return graph_2, kpi1.display(), kpi2.display(), kpi3.display(), kpi4.display()
    
# Define Callback para la actualización de graph 1
@callback(
    Output('graph1', 'figure'),
    [Input('graph1-update-interval', 'n_intervals')],
    prevent_initial_call=True
)
def update_graph1(n_intervals):

    # Obtenemos los datos actualizados para graph1
    df = dt.get_data('ONEUSDT','15')
    df = dt.CalculateSupertrend(df)
    df = dt.get_clean_data(df)

    # Creamos y devolvemos la figura actualizada para graph1
    graph1 = gf.create_supertrend_graph(df, 'ONEUSDT')

    return graph1





