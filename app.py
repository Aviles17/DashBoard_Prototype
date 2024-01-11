import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output


from pages import ethusdt_page, xrpusdt_page, home_page

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG],suppress_callback_exceptions=True)

# Sidebar style
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "14rem",
    "padding": "2rem 1rem",
    "background-color": "#566573",
}
CONTENT_STYLE = {
    "padding": "1rem 1rem",
    "color": "#FDFEFE",
    "font-size": "1.4em"
    
}

ACT_Img = html.Div(
    children=[
        html.Img(
            src=app.get_asset_url("LogoXD.svg"),
            style={'height': '100%', 'width': '100%', 'margin': '0px', 'border': '0px', 'padding':'0px'}
        )
    ],
)

# Sidebar navigation links
navbar = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Home", href="/", active="exact")),
        dbc.NavItem(dbc.NavLink("ETH/USDT", href="/ethusdt", active="exact")),
        dbc.NavItem(dbc.NavLink("XRP/USDT", href="/xrpusdt", active="exact")),
        # Add more navigation links as needed
    ],
    vertical=True,
    pills=True,
)

# Sidebar Layout
sidebar = html.Div(
    [
        ACT_Img,
        html.Hr(),
        html.P("Account Stock Management", className="lead", style= CONTENT_STYLE),
        navbar,
        html.Hr(),
    ],
    style=SIDEBAR_STYLE
)

# Define callbacks for changing the page content
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/":
        return home_page.home_page_layout()
    elif pathname == "/ethusdt":
        return ethusdt_page.ethusdt_page_layout()
    elif pathname == "/xrpusdt":
        return xrpusdt_page.xrpusdt_page_layout()
    else:
        return "404 Page Not Found"

# Main layout
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    dbc.Container([
        dbc.Row([
            dbc.Col([sidebar], width=2),
            dbc.Col([html.Div(id="page-content")], width=10),
        ])
    ], fluid=True),
])

if __name__ == "__main__":
    app.run_server(debug=True)