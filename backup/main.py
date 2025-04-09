import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import numpy as np

# Dados fictícios de vendedores com fotos realistas
vendedores = pd.DataFrame({
    'Nome': [f'Vendedor {i+1}' for i in range(10)],
    'Vendas': np.random.randint(50, 500, size=10),
    'Foto': [
        'https://randomuser.me/api/portraits/men/32.jpg',
        'https://randomuser.me/api/portraits/women/45.jpg',
        'https://randomuser.me/api/portraits/men/76.jpg',
        'https://randomuser.me/api/portraits/women/15.jpg',
        'https://randomuser.me/api/portraits/men/84.jpg',
        'https://randomuser.me/api/portraits/women/34.jpg',
        'https://randomuser.me/api/portraits/men/21.jpg',
        'https://randomuser.me/api/portraits/women/52.jpg',
        'https://randomuser.me/api/portraits/men/14.jpg',
        'https://randomuser.me/api/portraits/women/60.jpg'
    ]
})

# Ordenar pelos mais vendidos
vendedores = vendedores.sort_values(by='Vendas', ascending=False)

# Gerando dados fictícios
np.random.seed(42)
dates = pd.date_range(start="2022-01-01", periods=100)
df = pd.DataFrame({
    'Sales': np.random.randint(100, 1000, size=100),
    'Customers': np.random.randint(10, 100, size=100),
    'Revenue': np.random.uniform(1000, 5000, size=100)
}, index=dates)

# Função para obter os top 10 valores
def get_top_10(df, column_name):
    top_10 = df[column_name].nlargest(10).reset_index()
    top_10.columns = ['Date', column_name]
    top_10['Date'] = top_10['Date'].dt.strftime('%d/%m/%Y')
    return top_10

# Inicializando o app Dash
app = dash.Dash(__name__)

# Layout do dashboard
app.layout = html.Div([
    html.Div([
    html.H1("Dashboard", className='titulo-central')
]),

html.Div([
    dcc.Dropdown(
        id='dropdown_column',
        options=[{'label': col, 'value': col} for col in df.columns],
        value='Sales',
        style={'width': '30%'}
    )
], className='dropdown-container'),

    html.Div([
        html.Div([
            html.H4('TOP 10 DIAS COM MAIS VENDAS'),
            dash_table.DataTable(id='top_sales_table',
                                 style_table={'overflowX': 'auto'},
                                 style_data={'color': '#000000'})
        ], className='rank-card'),

        html.Div([
            html.H4('TOP 10 VENDEDORES'),
            html.Div([
                html.Div([
                    html.Img(src=row['Foto'], className='vendedor-img'),
                    html.Div([
                        html.Strong(row['Nome']),
                        html.Div(f"Vendas: {row['Vendas']}", style={'font-size': '12px'})
                    ])
                ], className='vendedor-container')
                for _, row in vendedores.iterrows()
            ])
        ], className='rank-card'),

        html.Div([
            html.H4('TOP 10 RECEITAS'),
            dash_table.DataTable(id='top_revenue_table',
                                 style_table={'overflowX': 'auto'},
                                 style_data={'color': '#000000'})
        ], className='rank-card'),

        html.Div([
            html.H4('MÉDIA DE VENDAS'),
            dash_table.DataTable(id='average_sales_table',
                                 style_table={'overflowX': 'auto'},
                                 style_data={'color': '#000000'})
        ], className='rank-card')
    ], className='section'),

    html.Div([
        dcc.Graph(id='column_graph', style={'display': 'inline-block', 'width': '48%'}),
        dcc.Graph(id='pie_graph', style={'display': 'inline-block', 'width': '48%'})
    ])
])

# Callback para atualizar os valores de rank e gráficos
@app.callback(
    [Output('top_sales_table', 'data'),
     Output('top_revenue_table', 'data'),
     Output('average_sales_table', 'data'),
     Output('column_graph', 'figure'),
     Output('pie_graph', 'figure')],
    [Input('dropdown_column', 'value')]
)
def update_dashboard(selected_column):
    top_sales_df = get_top_10(df, 'Sales')
    top_revenue_df = get_top_10(df, 'Revenue')
    average_sales_df = pd.DataFrame({
        'Date': df.index[:10].strftime('%d/%m/%Y'),
        'Average Sales': [df['Sales'].mean()] * 10
    })

    column_fig = {
        'data': [{
            'x': df.index,
            'y': df[selected_column],
            'type': 'bar',
            'name': selected_column
        }],
        'layout': {
            'title': f'Distribuição de {selected_column} ao longo do tempo',
            'paper_bgcolor': '#2E2E2E',
            'plot_bgcolor': '#2E2E2E',
            'font': {'color': '#FFFFFF'},
            'xaxis': {'tickformat': '%d/%m/%Y'}
        }
    }

    top_5 = df[selected_column].nlargest(5)
    pie_fig = {
        'data': [{
            'labels': top_5.index.strftime('%d/%m/%Y'),
            'values': top_5.values,
            'type': 'pie',
            'name': selected_column
        }],
        'layout': {
            'title': f'Top 5 dias em {selected_column}',
            'paper_bgcolor': '#2E2E2E',
            'plot_bgcolor': '#2E2E2E',
            'font': {'color': '#FFFFFF'}
        }
    }

    return (top_sales_df.to_dict('records'),
            top_revenue_df.to_dict('records'),
            average_sales_df.to_dict('records'),
            column_fig,
            pie_fig)

# Executa o servidor
if __name__ == '__main__':
    app.run(debug=True)
