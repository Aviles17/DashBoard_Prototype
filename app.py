import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Dash
from dash.dependencies import Input, Output
from Util.configuration_functions import load_configuration, create_linktree_navbar
from pages import home_page, coin_page

app = dash.Dash(__name__,suppress_callback_exceptions=True)
server = app.server

colors, coin_support = load_configuration("config.json")
coin_support = coin_support["supported-coins"]
nav_items, nav_links = create_linktree_navbar(coin_support)

ACT_Img = html.Div(
    children=[
        html.Img(
            src=app.get_asset_url("Logo_S&S_Yellow_Circle.png"),
            style={'height': '80%', 'width': '80%', 'margin-left': '20px' , 'border': '0px', 'padding':'0px'}
        ),
        html.P("S&S Investment", style={'textAlign': 'center', 'fontSize': '25px', 'fontWeight': 'bold', 'color': colors['color-gold']}),
    ],
)

# Sidebar navigation links
navbar = dbc.Nav(nav_items, vertical=True, pills=True, className="custom-nav")

# Sidebar Layout
sidebar = html.Div(
    [
        ACT_Img,
        html.Hr(),
        html.Br(),
        navbar,
        html.Hr(),
    ],
    id="SIDEBAR_STYLE"
)

# Define callbacks for changing the page content
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/":
        return home_page.home_page_layout()
    elif pathname in nav_links:
        return coin_page.general_coin_page_layout(pathname.lstrip('/'))
    else:
        return "404 Page Not Found"

# Main layout
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    dbc.Container([
        dbc.Row([
            dbc.Col([sidebar], width=2),
            dbc.Col([html.Div(id="page-content", className="content-column")], width=10),
        ], className="container-wrapper")
    ], fluid=True),
], className="page-wrapper")

if __name__ == "__main__":
    app.run_server(debug=True)