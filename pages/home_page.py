import dash_bootstrap_components as dbc
from dash import html, dcc, callback
from dash.dependencies import Input, Output
from components.kpi import kpi
from Util.data_functions import Get_Balance, get_history
import Util.graph_functions as gf
def home_page_layout():
    
    global df
    
    df, profit, trend, positive_prop, negative_prop = get_history()
    
    kpi0 = kpi("Balance Total", str(Get_Balance("USDT")),0)
    kpi1 = kpi("Tendencia",str(trend),1)
    kpi2 = kpi("Total Profit ",str(profit),2)
    print(positive_prop, negative_prop, profit)
    graph_1 = dcc.Graph(
        id="graph_1",
        figure = gf.create_history_barplot(df)
    )
    
    graph_2 = dcc.Graph(
        id="graph_2",
        figure = gf.create_kpi_piechart((positive_prop/abs(profit)), (abs(negative_prop)/abs(profit)))
    )
    user_input = dcc.Dropdown(
        id='user-input',
        options=[
            {'label': 'P&L%', 'value': 'Porcentaje'},
            {'label': 'Values', 'value': 'Numerico'}
        ],
        style={"color":"black"}
    )
    
    layout = dbc.Container([
        # Add your content for home page here
        dbc.Row([dbc.Col(user_input, md=4)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col(graph_1),
        ], id='graph_1-container', className="mb-4"), 
        
        dbc.Row([
            dbc.Col(graph_2),
            dbc.Col([
                kpi0.display(), 
                kpi1.display(), 
                kpi2.display()
            ], md=4)
        ])
    ], 
    style={'width': '100%', 'padding': '20px'})
    
    return layout

@callback(
    Output('graph_1', 'figure'),
    Input('user-input', 'value'),
    prevent_initial_call=True
)
def update_graph(user_input):
    if user_input == 'Porcentaje':
        return gf.create_history_barplot(df, 'P&L')
    else:
        return gf.create_history_barplot(df, 'Profit')