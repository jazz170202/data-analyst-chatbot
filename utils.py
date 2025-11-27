import pandas as pd

def load_data(path):
    df = pd.read_csv(path, parse_dates=['order_date'])
    return df

def summarize(df):
    summary = {
        'rows': df.shape[0],
        'columns': df.shape[1],
        'column_list': list(df.columns)
    }
    return summary

def show_head(df, n=5):
    return df.head(n)

def describe_numeric(df):
    return df.select_dtypes(include=['number']).describe()

def top_values(df, column, n=5):
    if column not in df.columns:
        return None
    return df.groupby(column).size().sort_values(ascending=False).head(n)

def sum_by(df, group_col, value_col):
    if group_col not in df.columns or value_col not in df.columns:
        return None
    return df.groupby(group_col)[value_col].sum().sort_values(ascending=False)

def total_revenue(df, qty_col='quantity', price_col='unit_price'):
    if qty_col not in df.columns or price_col not in df.columns:
        return None
    return (df[qty_col] * df[price_col]).sum()

def quick_insights(df):
    insights = {}
    # Example insights: top product by quantity, revenue by region
    if 'product' in df.columns and 'quantity' in df.columns:
        insights['top_product_by_quantity'] = df.groupby('product')['quantity'].sum().sort_values(ascending=False).head(1).to_dict()
    if 'region' in df.columns and 'quantity' in df.columns and 'unit_price' in df.columns:
        df = df.copy()
        df['revenue'] = df['quantity'] * df['unit_price']
        insights['revenue_by_region'] = df.groupby('region')['revenue'].sum().sort_values(ascending=False).to_dict()
    return insights
