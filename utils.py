import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="whitegrid")  # Optional styling

# --- Data analysis functions ---

def basic_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Returns descriptive statistics of numeric columns."""
    return df.describe()

def group_by_analysis(df: pd.DataFrame, group_col: str, value_col: str) -> pd.DataFrame:
    """Groups by column and sums numeric values."""
    if group_col not in df.columns or value_col not in df.columns:
        raise ValueError("Selected columns are not in the dataframe.")
    grouped_df = df.groupby(group_col)[value_col].sum().reset_index()
    return grouped_df.sort_values(by=value_col, ascending=False)

def top_n_values(df: pd.DataFrame, column: str, n: int = 5) -> pd.DataFrame:
    """Returns top n values of a column."""
    return df[column].value_counts().head(n).reset_index().rename(columns={'index': column, column: 'count'})

# --- Plotting functions using matplotlib/seaborn ---

def plot_bar_chart(df: pd.DataFrame, x_col: str, y_col: str):
    if not pd.api.types.is_numeric_dtype(df[y_col]):
        st.warning(f"Column {y_col} is not numeric. Please select a numeric column.")
        return
    df_plot = df[[x_col, y_col]].dropna()
    fig, ax = plt.subplots()
    sns.barplot(data=df_plot, x=x_col, y=y_col, ax=ax)
    ax.set_title(f"{y_col} by {x_col}")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    plt.close(fig)

def plot_line_chart(df: pd.DataFrame, x_col: str, y_col: str):
    if not pd.api.types.is_numeric_dtype(df[y_col]):
        st.warning(f"Column {y_col} is not numeric. Please select a numeric column.")
        return
    df_plot = df[[x_col, y_col]].dropna()
    fig, ax = plt.subplots()
    sns.lineplot(data=df_plot, x=x_col, y=y_col, ax=ax, marker="o")
    ax.set_title(f"{y_col} over {x_col}")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    plt.close(fig)

def plot_scatter_chart(df: pd.DataFrame, x_col: str, y_col: str):
    if not pd.api.types.is_numeric_dtype(df[y_col]):
        st.warning(f"Column {y_col} is not numeric. Please select a numeric column.")
        return
    df_plot = df[[x_col, y_col]].dropna()
    fig, ax = plt.subplots()
    sns.scatterplot(data=df_plot, x=x_col, y=y_col, ax=ax)
    ax.set_title(f"{y_col} vs {x_col}")
    st.pyplot(fig)
    plt.close(fig)
