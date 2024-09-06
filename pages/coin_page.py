from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from components.kpi import kpi
import Util.data_functions as dt
import Util.graph_functions as gf


def general_coin_page_layout(coin: str):
    global df
    global working_coin

    # Initialize variables for later usage
    working_coin = coin.upper()
    df = dt.get_data(working_coin, '15')
    df = dt.CalculateSupertrend(df)
    df = dt.update_df(df)
    df = df.head(250)

    # Graph 1 -> Live Chart
    graph_1 = dcc.Graph(
        id='graph_1',
        figure=gf.create_supertrend_graph(df, working_coin)
    )

    # Graph 2 -> Position Chart
    graph_2 = dcc.Graph(
        id="graph_2",
        figure=gf.create_order_graph(df, 0, 0, 'XRPUSDT', None)
    )

    # Create a dropdown for user input -> Type of order in order graph
    user_input = dcc.Dropdown(
        id='user-input',
        options=[
            {'label': 'Long Orders', 'value': 'Long'},
            {'label': 'Short Orders', 'value': 'Short'}
        ],
        style={
            "color": "white",
            "background-color": "#919191",
            "border-radius": "1rem",
        }
    )
    global kpi1, kpi2, kpi3, kpi4
    # Define KPI graphic object with class
    kpi1 = kpi("KPI 1", "Value 1", 1)
    kpi2 = kpi("KPI 2", "Value 2", 2)
    kpi3 = kpi("KPI 3", "Value 3", 3)
    kpi4 = kpi("KPI 4", "Value 4", 4)

# Define the overall layout of the page
    layout = dbc.Container([
        dcc.Interval(
            id='graph_1_update_interval',
            interval=60*1000,  # Update every 5 minutes (in milliseconds)
            n_intervals=0,
        ),
        dbc.Row([
            dbc.Col(f"{working_coin} Managment", style={"color": "white", "font-size": "2rem", "padding-top": "1.5%", "padding-left": "20.5%", "padding-bottom": "3%"})]),

        html.Br(),

        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Live Chart", style={
                                   "color": "white", "font-size": "1.5rem", "padding-top": "1.5%", "padding-left": "1.5%"}),
                    dbc.CardBody(
                        dbc.Col(graph_1)
                    )
                ], style={"backgroundColor": "#494949", "margin-left": "20%", "width": "81.5vw", "border-radius": "1rem"})
            )
        ]),

        html.Br(),
        html.Br(),

        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Row([
                            dbc.Col(html.P("Position Chart", style={
                                    "color": "white", "font-size": "1.5rem", "padding-top": "1.5%"})),
                            dbc.Col(user_input, style={"width": "20%"})
                        ], align="center"),
                        style={"padding-left": "1.5%"}
                    ),
                    dbc.CardBody(
                        dbc.Col(graph_2)
                    )
                ], style={"backgroundColor": "#494949", "margin-left": "20%", "width": "81.5vw", "border-radius": "1rem"})
            )
        ]),

        html.Br(),

        dbc.Row([
            dbc.Col(kpi1.display()),  # Place KPI 1 in the first column
            dbc.Col(kpi2.display()),  # Place KPI 2 in the second column
            dbc.Col(kpi3.display()),  # Place KPI 3 in the third column
            dbc.Col(kpi4.display()),  # Place KPI 4 in the fourth column
        ], style={
            "display": "flex",
            "justify-content": "space-between",
            "margin-left": "20%",
            "gap": "11%"
        }),
    ], fluid=True)

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
        size, entry, stoploss, goal_price = dt.get_position(
            "Buy", working_coin, df)
        figure_2 = gf.create_order_graph(
            df, float(entry), float(stoploss), working_coin, 'Buy')
        graph_2 = {
            'data': figure_2.data,
            'layout': figure_2.layout
        }
        kpi1.set_data("Order Size", size)
        kpi2.set_data("Profit", goal_price)
        kpi3.set_data("Entry", entry)
        kpi4.set_data("Stoploss", stoploss)
        return graph_2, kpi1.display(), kpi2.display(), kpi3.display(), kpi4.display()

    elif user_input == 'Short':
        size, entry, stoploss, goal_price = dt.get_position(
            "Sell", working_coin, df)
        figure_2 = gf.create_order_graph(
            df, float(entry), float(stoploss), working_coin, 'Sell')
        graph_2 = {
            'data': figure_2.data,
            'layout': figure_2.layout
        }
        kpi1.set_data("Order Size", size)
        kpi2.set_data("Profit", goal_price)
        kpi3.set_data("Entry", entry)
        kpi4.set_data("Stoploss", stoploss)
        return figure_2, kpi1.display(), kpi2.display(), kpi3.display(), kpi4.display()
    else:
        # Handle any other cases here
        graph_2 = None  # Set to None or an empty figure if needed
        kpi1.set_data("Order Size", "")
        kpi2.set_data("P&L %", "")
        kpi3.set_data("Entry - Profit", "")
        kpi4.set_data("Stoploss", "")
        return graph_2, kpi1.display(), kpi2.display(), kpi3.display(), kpi4.display()

# Define Callback for graph 1 constant update


@callback(
    Output('graph_1', 'figure', allow_duplicate=True),
    [Input('graph_1_update_interval', 'n_intervals')],
    prevent_initial_call=True
)
def update_graph_1(n_intervals):

    # Obtenemos los datos actualizados para graph1
    df = dt.get_data(working_coin, '15')
    df = dt.CalculateSupertrend(df)
    df = dt.update_df(df)
    df = df.head(250)

    # Creamos y devolvemos la figura actualizada para graph1
    graph_1 = gf.create_supertrend_graph(df, working_coin)

    return graph_1
