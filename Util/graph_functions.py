import pandas as pd
import plotly.graph_objects as go

def create_supertrend_graph(plot_df: pd.DataFrame, symbol: str):
    fig = go.Figure(data=[go.Candlestick(x=plot_df['Time'],
                                     open=plot_df['Open'],
                                     high=plot_df['High'],
                                     low=plot_df['Low'],
                                     close=plot_df['Close'],
                                     hovertext = True,
                                     name='ETHUSDT',
                                     increasing_line_color= 'cyan', 
                                     decreasing_line_color= 'mediumorchid'),
                      go.Scatter(x=plot_df['Time'], y=plot_df['ST_Inferior'], mode='lines', name='Buy', line={'color': 'cyan'}),
                      go.Scatter(x=plot_df['Time'], y=plot_df['ST_Superior'], mode='lines', name='Sell', line={'color': 'mediumorchid'}),
                      go.Scatter(x=plot_df['Time'], y=plot_df['DEMA800'], mode='lines', name='DEMA800', line={'color': 'limegreen'})])
    fig.update_layout(xaxis_rangeslider_visible=True,
                    showlegend=False,
                    plot_bgcolor='black',
                    xaxis=dict(
                        showgrid=True, 
                        zeroline=True, 
                        tickfont=dict(color='dimgray'),
                        gridcolor='dimgray',
                        zerolinecolor='dimgray',
                        ),
                    yaxis=dict(
                        showgrid=True, 
                        zeroline=True, 
                        tickfont=dict(color='dimgray'), 
                        gridcolor='dimgray',
                        zerolinecolor='dimgray',
                        ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=20, r=20, b=20, t=35) )
    
    return fig

def create_order_graph(plot_df: pd.DataFrame, entry: float, stoploss: float, symbol: str, side: str):
    if(side == 'Buy'):
        y_array = plot_df['ST_Inferior']
        color = 'cyan'
    elif(side == 'Sell'):
        y_array = plot_df['ST_Superior']
        print(y_array)
        color = 'magenta'
    else:
        y_array = [0] * len(plot_df['Time'])
        color = 'white'
        
    arr_entry = [entry] * len(plot_df['Time'])
    arr_stoploss = [stoploss] * len(plot_df['Time'])
    if(entry != 0 and stoploss != 0):
        fig = go.Figure(data=[go.Candlestick(x=plot_df['Time'],
                                            open=plot_df['Open'],
                                            high=plot_df['High'],
                                            low=plot_df['Low'],
                                            close=plot_df['Close'],
                                            hovertext = True,
                                            name=symbol,
                                            increasing_line_color= 'cyan', 
                                            decreasing_line_color= 'mediumorchid'),
                            go.Scatter(x=plot_df['Time'], y=arr_entry, mode='lines', name='Entry-Profit', line={'color': 'green'}),
                            go.Scatter(x=plot_df['Time'], y=arr_stoploss, mode='lines', name='Stoploss', line={'color': 'red'}),
                            go.Scatter(x=plot_df['Time'], y=y_array, mode='lines', name='Supertrend', line={'color': color})])
        fig.update_layout(xaxis_rangeslider_visible=True,
                    showlegend=False,
                    plot_bgcolor='black',
                    xaxis=dict(
                        showgrid=False, 
                        zeroline=False, 
                        tickfont=dict(color='white'),
                        ),
                    yaxis=dict(
                        showgrid=False, 
                        zeroline=False, 
                        tickfont=dict(color='white'), 
                        ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=20, r=20, b=20, t=35) )
        return fig
    else:
        fig = go.Figure(data=[go.Candlestick(x=plot_df['Time'],
                                            open=plot_df['Open'],
                                            high=plot_df['High'],
                                            low=plot_df['Low'],
                                            close=plot_df['Close'],
                                            hovertext = True,
                                            name=symbol,
                                            increasing_line_color= 'cyan', 
                                            decreasing_line_color= 'mediumorchid')])
        
        fig.update_layout(
                    xaxis_rangeslider_visible=True,
                    showlegend=False,
                    plot_bgcolor='black',
                    xaxis=dict(
                        showgrid=False, 
                        zeroline=False, 
                        tickfont=dict(color='white'),
                        ),
                    yaxis=dict(
                        showgrid=False, 
                        zeroline=False, 
                        tickfont=dict(color='white'), 
                        ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=20, r=20, b=20, t=35) )
        return fig
        