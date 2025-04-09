import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
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

# Função para obter os top 10 valores
def get_top_10(df, column_name):
    top_10 = df[column_name].nlargest(10).reset_index()
    top_10.columns = ['Date', column_name]
    top_10['Date'] = top_10['Date'].dt.strftime('%d/%m/%Y')  # Formata a data para o padrão brasileiro
    return top_10

# Inicializando o app Dash
app = dash.Dash(__name__)

# Layout do dashboard
app.layout = html.Div([
    html.Div([
        html.H1("Dashboard com Ranks e Gráficos dos Vendedores", style={'color': '#FFFFFF', 'margin': '0'}),
        dcc.Dropdown(
            id='dropdown_column',
            options=[{'label': col, 'value': col} for col in df.columns],
            value='Sales',  # Coluna padrão selecionada
            style={'width': '30%'}
        )
    ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center', 'margin-bottom': '20px'}),
    
    # Seção de ranks (top 10 valores em tabelas)
    html.Div([
        html.Div([
            html.H4('VISUALIZAR TODOS LEADS', style={'color': '#FFFFFF'}),
            dash_table.DataTable(id='top_sales_table',
                                 style_table={'overflowX': 'auto', 'backgroundColor': '#D3D3D3'},  # Fundo cinza claro
                                 style_header={'backgroundColor': '#A9A9A9'},  # Cabeçalho escuro
                                 style_data={'color': '#000000'})  # Cor do texto
        ], className='rank-card'),
        
        html.Div([
            html.H4('LEADS PERDIDOS', style={'color': '#FFFFFF'}),
            dash_table.DataTable(id='top_customers_table',
                                 style_table={'overflowX': 'auto', 'backgroundColor': '#D3D3D3'},  # Fundo cinza claro
                                 style_header={'backgroundColor': '#A9A9A9'},  # Cabeçalho escuro
                                 style_data={'color': '#000000'})  # Cor do texto
        ], className='rank-card'),
        
        html.Div([
            html.H4('OPORTUNIDADES', style={'color': '#FFFFFF'}),
            dash_table.DataTable(id='top_revenue_table',
                                 style_table={'overflowX': 'auto', 'backgroundColor': '#D3D3D3'},  # Fundo cinza claro
                                 style_header={'backgroundColor': '#A9A9A9'},  # Cabeçalho escuro
                                 style_data={'color': '#000000'})  # Cor do texto
        ], className='rank-card'),
        
        html.Div([
            html.H4('PROPPOSTAS', style={'color': '#FFFFFF'}),
            dash_table.DataTable(id='average_sales_table',
                                 style_table={'overflowX': 'auto', 'backgroundColor': '#D3D3D3'},  # Fundo cinza claro
                                 style_header={'backgroundColor': '#A9A9A9'},  # Cabeçalho escuro
                                 style_data={'color': '#000000'})  # Cor do texto
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
    [Output('top_sales_table', 'data'),
     Output('top_customers_table', 'data'),
     Output('top_revenue_table', 'data'),
     Output('average_sales_table', 'data'),
     Output('column_graph', 'figure'),
     Output('pie_graph', 'figure')],
    [Input('dropdown_column', 'value')]
)
def update_dashboard(selected_column):
    # Calcular os top 10 valores para cada métrica
    top_sales_df = get_top_10(df, 'Sales')
    top_customers_df = get_top_10(df, 'Customers')
    top_revenue_df = get_top_10(df, 'Revenue')
    
    # Criar DataFrame para a média de vendas (simulando uma média fixa para top 10)
    average_sales_df = pd.DataFrame({
        'Date': df.index[:10].strftime('%d/%m/%Y'), 
        'Average Sales': [df['Sales'].mean()] * 10
    })
    
    # Gráfico de colunas
    column_fig = {
        'data': [{
            'x': df.index,
            'y': df[selected_column],
            'type': 'bar',
            'name': selected_column
        }],
        'layout': {
            'title': f'GRAFICO TORRE QUENTE OU FRIO POR VENDEDORES',
            'paper_bgcolor': '#2E2E2E',  # Fundo do gráfico
            'plot_bgcolor': '#2E2E2E',   # Fundo do gráfico
            'font': {'color': '#FFFFFF'}
        }
    }
    
    # Selecionando os top 5 valores para o gráfico de pizza
    top_5 = df[selected_column].nlargest(5)
    pie_fig = {
        'data': [{
            'labels': top_5.index.strftime('%d/%m/%Y'),  # Usamos as datas como labels
            'values': top_5.values,
            'type': 'pie',
            'name': selected_column
        }],
        'layout': {
            'title': f'PEDIDOS DE VENDA POR VENDEDOR',
            'paper_bgcolor': '#2E2E2E',  # Fundo do gráfico
            'plot_bgcolor': '#2E2E2E',   # Fundo do gráfico
            'font': {'color': '#FFFFFF'}
        }
    }
    
    return (top_sales_df.to_dict('records'),
            top_customers_df.to_dict('records'),
            top_revenue_df.to_dict('records'),
            average_sales_df.to_dict('records'),
            column_fig,
            pie_fig)

# Executa o servidor
if __name__ == '__main__':
    app.run(debug=True)

