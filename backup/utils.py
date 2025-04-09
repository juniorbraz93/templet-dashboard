def get_top_n(df, column_name, n=25):
    top_n = df[column_name].nlargest(n).reset_index()
    col_name_pt = {
    'Sales': 'Vendas',
    'Revenue': 'Receita'
    }.get(column_name, column_name)
    top_n.columns = ['Data', col_name_pt]
    top_n['Data'] = top_n['Data'].dt.strftime('%d/%m/%Y')
    return top_n
