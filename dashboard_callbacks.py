from dash.dependencies import Input, Output
import pandas as pd
from data import df
from utils import get_top_10

def register_callbacks(app):
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
