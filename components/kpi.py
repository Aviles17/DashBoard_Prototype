from dash import html 
import dash_bootstrap_components as dbc

class kpi:
    def __init__(self, title, data,id):
        self.title = title
        self.data = data
        self.id = id
        self.color = None
    
    def display(self):
        layout = dbc.Card(id=f"kpi{self.id}")  # Add id attribute here
        layout.children = [
            dbc.CardBody([
                html.H4(f"{self.title}", className="card-title"),
                html.P(f"{self.data}", className="card-text"),
            ])
        ]
        return layout
    def set_data(self, title, value):
        self.title = title
        self.data = value
        
    def set_color(self, base_data: float, position_side: str):
        pass