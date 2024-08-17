import json
import dash_bootstrap_components as dbc

def load_configuration(path:str)->tuple:
    try:
        with open(path, 'r') as file:
            parsed_data = json.load(file) #Read config.json file
            return parsed_data[0],parsed_data[1] #Colors, Coin Support
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None,None
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' contains invalid JSON.")
        return None,None
    except PermissionError:
        print(f"Error: You do not have permission to read the file '{file_path}'.")
        return None,None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None

def create_linktree_navbar(coin_support:list)->list:
    nav_items = []
    nav_links =[]
    nav_items.append(dbc.NavItem(dbc.NavLink("HOME", href="/", className="custom-nav-link",active="exact")))
    nav_links.append("/")
    for coin in coin_support:
        page_name = coin.lower()
        display_text = coin.upper()
        nav_items.append(dbc.NavItem(dbc.NavLink(
                                                display_text, 
                                                href=f"/{page_name}", 
                                                className="custom-nav-link", 
                                                active="exact")
                                                ))
        nav_links.append(f"/{page_name}")
    return nav_items, nav_links






