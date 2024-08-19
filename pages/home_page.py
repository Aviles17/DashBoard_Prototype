import dash_bootstrap_components as dbc
from dash import html, dcc, callback
from dash.dependencies import Input, Output
from components.kpi import kpi
from Util.data_functions import Get_Balance, get_history
import Util.graph_functions as gf
def home_page_layout():
    
    global df
    
    df, profit, trend, prop_positives, prop_negatives, prop_count_positives, prop_count_negatives = get_history()
    
    kpi0 = kpi("Balance Total", str(Get_Balance("USDT")),0)# #
    kpi1 = kpi("Tendencia",str(trend),1)
    kpi2 = kpi("Total Profit ",str(profit),2)
    graph_1 = dcc.Graph(
        id="graph_1",
        figure = gf.create_history_barplot(df)
    )
    
    user_input = dcc.Dropdown(
        id='user-input',
        options=[
            {'label': 'P&L%', 'value': 'Porcentaje'},
            {'label': 'Values', 'value': 'Numerico'}
        ],
        style={
        "color": "white",
        "background-color": "#919191",
        "border-radius": "1rem",
        "high": "100px"
        }
    )
    
    layout = dbc.Container([
        dbc.Row([
            dbc.Col(f"General Managment", style={"color": "white","font-size": "2rem", "padding-top": "1rem", "padding-left": "14.5rem", "padding-bottom": "1rem"})]),
        html.Br(),
        html.Br(),
        html.Br(),
        # Add your content for home page here
        dbc.Row([
            dbc.Col([
                dbc.Row(user_input, style={"width": "100%"}),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                dbc.Row(kpi0.display()),
                html.Br(),
                html.Br(),
                html.Br(),
                dbc.Row(kpi2.display()),
                html.Br(),
                html.Br(),
                html.Br(),
                dbc.Row(kpi1.display()),
            ]),
            # History of orders graph
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("History of Orders", style={"color": "white","font-size": "1.5rem", "padding-top": "1rem", "padding-left": "1rem"}),
                    dbc.CardBody(
                        dbc.Col(graph_1)
                    )
                ], style={"backgroundColor": "#494949", "width": "925px", "border-radius": "1rem"})
            )
        ], id='graph_1-container', style={
                                    "display": "flex", 
                                    "justify-content": "space-between", 
                                    "margin-left": "14rem",
                                    "gap": "15px"}), 
        
        html.Br(),

        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Monthly Effective Rate", style={"color": "white","font-size": "1.5rem", "padding-top": "1rem", "padding-left": "1rem"}),
                    dbc.CardBody(
                        dbc.Col(f"")
                    )
                ], style={"backgroundColor": "#494949", "width": "565px", "border-radius": "1rem"}),
            ),

            dbc.Card([
                    dbc.CardHeader("Revenue per Ticker", style={"color": "white","font-size": "1.5rem", "padding-top": "1rem"}),
                    dbc.CardBody(
                        dbc.Col(f"")
                    )
                ], style={"backgroundColor": "#494949", "width": "565px", "border-radius": "1rem"}),
        ], id='graph_1-container', style={
                                    "display": "flex", 
                                    "margin-left": "14rem",
                                    "gap": "15px"}), 

    ])
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