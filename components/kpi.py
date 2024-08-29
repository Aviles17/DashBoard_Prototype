from dash import html 
import dash_bootstrap_components as dbc

class kpi:
    def __init__(self, title, data,id):
        self.title = title
        self.data = data
        self.id = id
    
    def display(self):
        return html.Div([
            html.H4(self.title, style={"font-size": "1.5rem", "padding-top": "5%", "margin": 0, "text-align": "center"}),
            html.P(self.data, style={"margin": 0, "text-align": "center"})
        ], id=f"kpi{self.id}", style={
            "background-color": "#494949",
            "border-radius": "1rem",
            "color": "white",
            "width": "15vw",
            "padding-bottom": "8%",
            "justify-content": "center",
            "align-items": "center"
        })
    
    def set_data(self, title, value):
        self.title = title
        self.data = value
    