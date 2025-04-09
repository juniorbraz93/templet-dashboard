import dash
from layout import layout
from dashboard_callbacks import register_callbacks

app = dash.Dash(__name__)
app.layout = layout

register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)
