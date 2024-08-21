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
                                     increasing_line_color= '#FFD700', 
                                     decreasing_line_color= 'dimgray'),
                      go.Scatter(x=plot_df['Time'], y=plot_df['ST_Inferior'], mode='lines', name='Buy', line={'color': '#FFD700'}),
                      go.Scatter(x=plot_df['Time'], y=plot_df['ST_Superior'], mode='lines', name='Sell', line={'color': 'dimgray'}),
                      go.Scatter(x=plot_df['Time'], y=plot_df['DEMA800'], mode='lines', name='DEMA800', line={'color': '#7100ff'})])
    fig.update_layout(xaxis_rangeslider_visible=True,
                    showlegend=False,
                    plot_bgcolor='#131313',
                    xaxis=dict(
                        showgrid=True, 
                        zeroline=True, 
                        tickfont=dict(color='white'),
                        gridcolor='dimgray',
                        zerolinecolor='dimgray',
                        ),
                    yaxis=dict(
                        showgrid=True, 
                        zeroline=True, 
                        tickfont=dict(color='white'), 
                        gridcolor='dimgray',
                        zerolinecolor='dimgray',
                        ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=20, r=20, b=20, t=35) )
    
    return fig

def create_order_graph(plot_df: pd.DataFrame, entry: float, stoploss: float, symbol: str, side: str):
    if(side == 'Buy'):
        y_array = plot_df['ST_Inferior']
        color = '#FFD700'
    elif(side == 'Sell'):
        y_array = plot_df['ST_Superior']
        color = 'dimgray'
    else:
        y_array = [0] * len(plot_df['Time'])
        color = 'white'
        
    arr_entry = [entry] * len(plot_df['Time'])
    arr_stoploss = [stoploss] * len(plot_df['Time'])
    arr_profit = [((2*entry)-stoploss)] * len(plot_df['Time'])
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
                                            increasing_line_color= '#FFD700', 
                                            decreasing_line_color= 'dimgray'),
                            go.Scatter(x=plot_df['Time'], y=arr_entry, mode=mode_plot_st, name='Entry-Profit', line={'color': '#0028ff'}),
                            go.Scatter(x=plot_df['Time'], y=arr_stoploss, mode=mode_plot_entry, name='Stoploss', line={'color': '#d700ff'}),
                            go.Scatter(x=plot_df['Time'], y=arr_profit, mode=mode_plot_entry, name='Profit', line={'color': '#00ff0b'}),
                            go.Scatter(x=plot_df['Time'], y=y_array, mode='lines', name='Supertrend', line={'color': color})])
        fig.update_layout(xaxis_rangeslider_visible=True,
                    showlegend=False,
                    plot_bgcolor='#131313',
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
                                            increasing_line_color= '#FFD700', 
                                            decreasing_line_color= 'dimgray')])
        
        fig.update_layout(
                    xaxis_rangeslider_visible=True,
                    showlegend=False,
                    plot_bgcolor='#131313',
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

def create_history_barplot(plot_df: pd.DataFrame, type_l: str="Profit"):
    # Crear el gráfico de barras con Plotly Express
    fig = px.bar(plot_df, x="Time", y=type_l, title="",
                labels={"Time": "Tiempo", type_l: "Valor"},)

    # Personalizar diseño del gráfico
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        plot_bgcolor='#494949',
        xaxis_title='', 
        yaxis_title='', 
        xaxis=dict(
            showgrid=True,
            zeroline=False,
            tickfont=dict(color='white'),
            gridcolor='dimgray',
            dtick=len(plot_df) // 10  # Mostrar una etiqueta cada 10 puntos de datos
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            gridcolor='dimgray',
            tickfont=dict(color='white')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, b=20, t=35)
    )
    fig.update_traces(marker_line_color='black', marker_line_width=0.5)

    # Asignar colores basados en el valor positivo/negativo
    fig.data[0].marker.color = [
        '#FFD700' if val >= 0 else '#919191' for val in plot_df[type_l]
    ]

    return fig


def create_monthly_efective_rate_graph(profit: float, actual_amount: float):
    percentage = (profit/(actual_amount-profit))*100
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=percentage,
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#FFD700"},
            'steps': [
                {'range': [0, 5], 'color': "#919191"},
                {'range': [5, 10], 'color': "#3e3e9d"},
                {'range': [10, 100], 'color': "#4dff54"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 10},  # The mark at 5%

        },
        number={'suffix': "%"}
    ))
    # Update layout for better appearance
    fig.update_layout(
        font={"family": "Helvetica",'size': 18, 'color': "white"},
        plot_bgcolor="#494949",
        paper_bgcolor="#494949",
        width=500,
        height=400 
    )
    return fig

def create_barplot_per_ticker(cumulative_sum: dict):
    colors = ["#919191" if value < 0 else "#FFD700" for value in cumulative_sum.values()]
    fig = go.Figure([
        go.Bar(x=list(cumulative_sum.keys()), y=list(cumulative_sum.values()), marker_color=colors)
    ])

    fig.update_layout(
        xaxis_title="Ticker",
        yaxis_title="Total Revenue",
        font={"family": "Helvetica",'size': 18, 'color': "white"},
        plot_bgcolor="#494949",
        paper_bgcolor="#494949",
        width=500,
        height=400,
        yaxis=dict(
            showgrid=True,
            gridcolor='dimgray',
            tickfont=dict(color='white')
        ),
    )

    return fig