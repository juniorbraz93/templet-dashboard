def get_top_n(df, column_name, n=18):
    top_n = df[column_name].nlargest(n).reset_index()
    top_n.columns = ['Date', column_name]
    top_n['Date'] = top_n['Date'].dt.strftime('%d/%m/%Y')
    return top_n
