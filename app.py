import dash
import os
from dash import dcc, html
from layout import layout, vendedor_layout
from dashboard_callbacks import register_callbacks

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Dashboard de Vendas"
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

register_callbacks(app)

@app.callback(
    dash.Output('page-content', 'children'),
    dash.Input('url', 'pathname')
)
def display_page(pathname):
    if pathname.startswith('/vendedor/'):
        try:
            nome_slug = pathname.split('/')[-1]
            return vendedor_layout(nome_slug)
        except:
            return html.H3("Vendedor não encontrado.")
    return layout

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run(debug=True, host='0.0.0.0', port=port)
