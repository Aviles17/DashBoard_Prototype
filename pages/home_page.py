import dash_bootstrap_components as dbc
from dash import html, dcc, callback
from dash.dependencies import Input, Output
from components.kpi import kpi
from Util.data_functions import Get_Balance, get_kpi_history
from Util.configuration_functions import load_configuration
import Util.graph_functions as gf
def home_page_layout():
    
    global df
    colors, coin_support = load_configuration("config.json")
    df, profit, profit_mean, cumulative_ticker = get_kpi_history(coin_support)
    
    kpi0 = kpi("Total Balance", str(Get_Balance("USDT")),0)
    kpi1 = kpi("Operation Amount",str(len(df)),1)
    kpi2 = kpi("Total Profit ",str(profit),2)
    graph_1_home = dcc.Graph(
        id="graph_1_home",
        figure = gf.create_history_barplot(df)
    )
    
    graph_2_home = dcc.Graph(
        id="graph_2_home",
        figure = gf.create_monthly_efective_rate_graph(profit,float(Get_Balance("USDT")))
    )

    graph_3_home = dcc.Graph(
        id="graph_3_home",
        figure = gf.create_barplot_per_ticker(cumulative_ticker)
    )
    
    layout = dbc.Container([
        dbc.Row([
            dbc.Col(f"General Managment", style={"color": "white","font-size": "2rem", "padding-top": "1.5%", "padding-left": "19.5%", "padding-bottom": "2%"})]),
        html.Br(),
        html.Br(),
        # Add your content for home page here
        dbc.Row([
            dbc.Col([
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
                    dbc.CardHeader("History of Orders", style={"color": "white","font-size": "1.5rem", "padding-top": "1.5%", "padding-left": "1.5%"}),
                    dbc.CardBody(
                        dbc.Col(graph_1_home)
                    )
                ], style={"backgroundColor": "#494949", "width": "65.5vw", "border-radius": "1rem"})
            )
        ], id='graph_1_home-container', style={
                                    "display": "flex", 
                                    "justify-content": "space-between", 
                                    "margin-left": "19.25%",
                                    "gap": "2%"}), 
        
        html.Br(),

        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Monthly Effective Rate", style={"color": "white","font-size": "1.5rem", "padding-top": "3%", "padding-left": "3%"}),
                    dbc.CardBody(
                        dbc.Col(graph_2_home),
                        style = {"padding-left": "9%"}
                    )
                ], style={"backgroundColor": "#494949", "width": "40vw", "border-radius": "1rem"}),
            ),

            dbc.Card([
                    dbc.CardHeader("Revenue per Ticker", style={"color": "white","font-size": "1.5rem", "padding-top": "3%", "padding-left": "3%"}),
                    dbc.CardBody(
                        dbc.Col(graph_3_home),
                        style = {"padding-left": "16%"}
                    )
                ], style={"backgroundColor": "#494949", "width": "43vw", "border-radius": "1rem"}),
        ], style={
                                    "display": "flex", 
                                    "margin-left": "19.25%",
                                    "gap": "2%",
                                    "width": "82vw"}), 
        html.Br()

    ])
    return layout
