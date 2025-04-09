def get_top_n(df, column_name, n=25):
    top_n = df[column_name].nlargest(n).reset_index()
    
    col_name_pt = {
        'Sales': 'Vendas',
        'Revenue': 'Receita'
    }.get(column_name, column_name)

    top_n.columns = ['Data', col_name_pt]
    top_n['Data'] = top_n['Data'].dt.strftime('%d/%m/%Y')

    # Formatar valores da receita com 2 casas decimais
    if col_name_pt == 'Receita':
        top_n['Receita'] = top_n['Receita'].map(lambda x: f"{x:.2f}")

    return top_n
