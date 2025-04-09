import dash_html_components as html
import dash_core_components as dcc
import dash_table
from data import vendedores, df

layout = html.Div([
    # Título com imagem à esquerda
    html.Div([
        html.Img(src='/assets/logo.png', style={
            'height': '50px',
            'marginRight': '15px'
        }),
        html.H1("Dashboard de Vendas", className='titulo-central')
    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '20px'}),

    # Dropdown de seleção
    html.Div([
        dcc.Dropdown(
            id='dropdown_column',
            options=[{'label': col, 'value': col} for col in df.columns],
            value='Sales',
            style={'width': '30%'}
        )
    ], className='dropdown-container'),

    # Seções principais
    html.Div([
        # Tabela de dias com mais vendas
        html.Div([
            html.H4('DIAS COM MAIS VENDAS'),
            dash_table.DataTable(id='top_sales_table')
        ], className='rank-card'),

        # Ranking de vendedores com link
        html.Div([
            html.H4('TOP 10 VENDEDORES', style={'textAlign': 'center'}),
            html.Table([
                html.Thead(html.Tr([
                    html.Th('Rank'),
                    html.Th('Foto'),
                    html.Th('Vendedor'),
                    html.Th('Vendas')
                ])),
                html.Tbody([
                    html.Tr([
                        html.Td(index + 1),
                        html.Td(html.Img(src=row['Foto'], className='foto-vendedor', style={'width': '50px'})),
                        html.Td(html.A(row['Nome'], href=f"/vendedor/{row['Nome'].replace(' ', '-')}",
                                       style={'fontWeight': 'bold', 'color': 'black'})),
                        html.Td(f"{row['Vendas']} vendas", style={'color': '#6A0DAD', 'textAlign': 'right'})
                    ]) for index, row in vendedores.head(18).reset_index(drop=True).iterrows()
                ])
            ], className='tabela-vendedores')
        ], className='rank-card'),

        # Tabela de receitas
        html.Div([
            html.H4('RECEITAS'),
            dash_table.DataTable(id='top_revenue_table')
        ], className='rank-card'),

        # Tabela de média de vendas
        html.Div([
            html.H4('MÉDIA DE VENDAS'),
            dash_table.DataTable(id='average_sales_table')
        ], className='rank-card'),
    ], className='section'),

    # Gráficos
    html.Div([
        dcc.Graph(
            id='column_graph',
            figure={
                'data': [
                    {
                        'x': ['01/12', '02/12', '03/12', '04/12', '05/12', '06/12', '07/12', '08/12'],
                        'y': [3, 2, 7, 6.8, 5, 2, 8, 7],
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'name': 'Novos inscritos',
                        'line': {'color': 'green', 'width': 4, 'shape': 'spline'},
                        'marker': {'size': 8}
                    }
                ],
                'layout': {
                    'title': 'Crescimento de inscritos',
                    'title_x': 0.5,
                    'margin': {'t': 50, 'b': 40, 'l': 40, 'r': 20},
                    'height': 300
                }
            },
            style={'display': 'inline-block', 'width': '48%'}
        ),
        dcc.Graph(id='pie_graph', style={'display': 'inline-block', 'width': '48%'})
    ])
])

# Layout da página de detalhes do vendedor
def vendedor_layout(nome_slug):
    nome_real = nome_slug.replace('-', ' ')
    vendedor = vendedores[vendedores['Nome'] == nome_real]

    if vendedor.empty:
        return html.H3("Vendedor não encontrado.")

    vendedor = vendedor.iloc[0]

    return html.Div([
        html.Div([
            html.H2(f"Detalhes do Vendedor: {vendedor['Nome']}", style={'textAlign': 'center'}),
            html.Img(src=vendedor['Foto'], style={
                'width': '150px',
                'borderRadius': '50%',
                'display': 'block',
                'margin': '20px auto'
            }),
            html.P(f"Total de vendas: {vendedor['Vendas']} vendas", style={'textAlign': 'center', 'fontSize': '20px'}),
            html.P(f"📞 Telefone: {vendedor['Telefone']}", style={'textAlign': 'center'}),
            html.P(f"📍 Endereço: {vendedor['Endereço']}", style={'textAlign': 'center'}),
            html.Div(html.A("⬅ Voltar para o dashboard", href="/"), style={'textAlign': 'center', 'marginTop': '20px'})
        ], className='vendedor-detalhes')
    ])
