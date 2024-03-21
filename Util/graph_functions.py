import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def create_supertrend_graph(plot_df: pd.DataFrame, symbol: str):
    fig = go.Figure(data=[go.Candlestick(x=plot_df['Time'],
                                     open=plot_df['Open'],
                                     high=plot_df['High'],
                                     low=plot_df['Low'],
                                     close=plot_df['Close'],
                                     hovertext = True,
                                     name=symbol,
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
        color = 'magenta'
    else:
        y_array = [0] * len(plot_df['Time'])
        color = 'white'
        
    arr_entry = [entry] * len(plot_df['Time'])
    arr_stoploss = [stoploss] * len(plot_df['Time'])
    if (entry - stoploss) <= 0.1:
        mode_plot_st = 'markers'
        mode_plot_entry = 'lines'
    else:
        mode_plot = 'lines'
        mode_plot_entry = 'lines'
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
                            go.Scatter(x=plot_df['Time'], y=arr_entry, mode=mode_plot_st, name='Entry-Profit', line={'color': 'green'}),
                            go.Scatter(x=plot_df['Time'], y=arr_stoploss, mode=mode_plot_entry, name='Stoploss', line={'color': 'red'}),
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

def create_history_barplot(plot_df: pd.DataFrame, type_l: str="P&L"):
    # Crear el gráfico de barras con Plotly Express
    fig = px.bar(plot_df, x="Time", y=type_l, title="Historial de Órdenes",
                color_discrete_map={'positive': 'green', 'negative': 'red'},
                labels={"Time": "Tiempo", type_l: "Valor"},)

    # Personalizar diseño del gráfico
    fig.update_layout(
        xaxis_rangeslider_visible=True,
        plot_bgcolor='black',
        xaxis_title='', 
        yaxis_title='', 
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(color='white'),
            dtick=len(plot_df) // 10  # Mostrar una etiqueta cada 10 puntos de datos
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(color='white')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, b=20, t=35)
    )

    # Asignar colores basados en el valor positivo/negativo
    fig.data[0].marker.color = [
        'green' if val >= 0 else 'red' for val in plot_df[type_l]
    ]

    return fig


def create_kpi_piechart(positive_prop: float, negative_prop: float, titulo: str = "Default"):
    pie_trace = go.Pie(
        labels=['Profit', 'Loss'],
        values=[positive_prop, negative_prop],
        marker=dict(colors=['green', 'red']), 
        hole=0.5,  
        textinfo='percent+label'  # Display both percentage and label in the hover text
    )

    layout = go.Layout(
        title= titulo
    )
    # Create figure
    fig = go.Figure(data=[pie_trace], layout=layout)
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