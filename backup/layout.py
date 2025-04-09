import dash_html_components as html
import dash_core_components as dcc
import dash_table
from data import vendedores, df

layout = html.Div([
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
                html.H4('DIAS COM MAIS VENDAS'),
                dash_table.DataTable(id='top_sales_table')
            ], className='rank-card'),

            html.Div([
        html.H4('TOP 10 VENDEDORES'),

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
                    html.Td(html.Img(src=row['Foto'], className='foto-vendedor')),
                    html.Td(html.Strong(row['Nome'])),
                    html.Td(f"{row['Vendas']} vendas", style={'color': '#000000', 'textAlign': 'right'})
                ]) for index, row in vendedores.head(18).iterrows()
            ])
        ], className='tabela-vendedores')

    ], className='rank-card'),


        html.Div([
            html.H4(' RECEITAS'),
            dash_table.DataTable(id='top_revenue_table')
        ], className='rank-card'),

        html.Div([
            html.H4('MÉDIA DE VENDAS'),
            dash_table.DataTable(id='average_sales_table')
        ], className='rank-card'),
    ], className='section'),

    html.Div([
        dcc.Graph(id='column_graph', style={'display': 'inline-block', 'width': '48%'}),
        dcc.Graph(id='pie_graph', style={'display': 'inline-block', 'width': '48%'})
    ])
])
