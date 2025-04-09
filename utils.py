def get_top_10(df, column_name):
    top_10 = df[column_name].nlargest(10).reset_index()
    top_10.columns = ['Date', column_name]
    top_10['Date'] = top_10['Date'].dt.strftime('%d/%m/%Y')
    return top_10
