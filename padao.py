import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

# Gerando dados fictícios
np.random.seed(42)
dates = pd.date_range(start="2022-01-01", periods=100)
data = {
    'Sales': np.random.randint(100, 1000, size=(100)),
    'Customers': np.random.randint(10, 100, size=(100)),
    'Revenue': np.random.uniform(1000, 5000, size=(100)),
}

df = pd.DataFrame(data, index=dates)

# Funções para calcular os ranks
def get_ranks(df):
    return {
        'Top Sales': df['Sales'].max(),
        'Top Customers': df['Customers'].max(),
        'Top Revenue': df['Revenue'].max(),
        'Average Sales': df['Sales'].mean(),
    }

# Inicializando o app Dash
app = dash.Dash(__name__)

# Layout do dashboard
app.layout = html.Div([
    html.Div([
        html.H1("Dashboard com Ranks e Gráficos", style={'color': '#FFFFFF', 'margin': '0'}),
        dcc.Dropdown(
            id='dropdown_column',
            options=[{'label': col, 'value': col} for col in df.columns],
            value='Sales',  # Coluna padrão selecionada
            style={'width': '30%'}
        )
    ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center', 'margin-bottom': '20px'}),
    
    # Seção de ranks (quatro grids)
    html.Div([
        html.Div([
            html.H4('Top Sales', style={'color': '#FFFFFF'}),
            html.P(id='top_sales', style={'color': '#FFFFFF'})
        ], className='rank-card'),
        
        html.Div([
            html.H4('Top Customers', style={'color': '#FFFFFF'}),
            html.P(id='top_customers', style={'color': '#FFFFFF'})
        ], className='rank-card'),
        
        html.Div([
            html.H4('Top Revenue', style={'color': '#FFFFFF'}),
            html.P(id='top_revenue', style={'color': '#FFFFFF'})
        ], className='rank-card'),
        
        html.Div([
            html.H4('Average Sales', style={'color': '#FFFFFF'}),
            html.P(id='average_sales', style={'color': '#FFFFFF'})
        ], className='rank-card'),
    ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '20px'}),
    
    # Contêiner para os dois gráficos
    html.Div([
        dcc.Graph(id='column_graph', style={'display': 'inline-block', 'width': '48%'}),
        dcc.Graph(id='pie_graph', style={'display': 'inline-block', 'width': '48%'})
    ]),
], style={'backgroundColor': '#2E2E2E', 'padding': '20px'})

# Callback para atualizar os valores de rank e gráficos
@app.callback(
    [Output('top_sales', 'children'),
     Output('top_customers', 'children'),
     Output('top_revenue', 'children'),
     Output('average_sales', 'children'),
     Output('column_graph', 'figure'),
     Output('pie_graph', 'figure')],
    [Input('dropdown_column', 'value')]
)
def update_dashboard(selected_column):
    # Calcular os ranks
    ranks = get_ranks(df)
    
    # Gráfico de colunas
    column_fig = {
        'data': [{
            'x': df.index,
            'y': df[selected_column],
            'type': 'bar',
            'name': selected_column
        }],
        'layout': {
            'title': f'Gráfico de Colunas - {selected_column}',
            'paper_bgcolor': '#2E2E2E',  # Fundo do gráfico
            'plot_bgcolor': '#2E2E2E',   # Fundo do gráfico
            'font': {'color': '#FFFFFF'}
        }
    }
    
    # Selecionando os top 5 valores para o gráfico de pizza
    top_5 = df[selected_column].nlargest(5)
    pie_fig = {
        'data': [{
            'labels': top_5.index.strftime('%Y-%m-%d'),  # Usamos as datas como labels
            'values': top_5.values,
            'type': 'pie',
            'name': selected_column
        }],
        'layout': {
            'title': f'Gráfico de Pizza - {selected_column} (Top 5)',
            'paper_bgcolor': '#2E2E2E',  # Fundo do gráfico
            'plot_bgcolor': '#2E2E2E',   # Fundo do gráfico
            'font': {'color': '#FFFFFF'}
        }
    }
    
    return (f'{ranks["Top Sales"]}', f'{ranks["Top Customers"]}', 
            f'{ranks["Top Revenue"]:.2f}', f'{ranks["Average Sales"]:.2f}', 
            column_fig, pie_fig)

# Executa o servidor
if __name__ == '__main__':
    app.run_server(debug=True)
