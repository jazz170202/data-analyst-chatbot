import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="whitegrid")  # Optional styling

# --- Data analysis functions ---

def basic_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Returns descriptive statistics of numeric columns."""
    if df.empty:
        st.warning("The dataset is empty.")
        return pd.DataFrame()
    return df.describe()

def group_by_analysis(df: pd.DataFrame, group_col: str, value_col: str) -> pd.DataFrame:
    """Groups by column and sums numeric values."""
    if group_col not in df.columns or value_col not in df.columns:
        st.warning(f"Columns {group_col} or {value_col} not found in the dataset.")
        return pd.DataFrame()
    grouped_df = df.groupby(group_col)[value_col].sum().reset_index()
    if grouped_df.empty:
        st.warning("No data to group. Check your columns.")
        return pd.DataFrame()
    return grouped_df.sort_values(by=value_col, ascending=False)

def top_n_values(df: pd.DataFrame, column: str, n: int = 5) -> pd.DataFrame:
    """Returns top n values of a column."""
    if column not in df.columns:
        st.warning(f"{column} is not in the dataframe.")
        return pd.DataFrame()
    
    result = df[column].value_counts().head(n).reset_index()
    
    # Safe renaming to avoid duplicates
    result.columns = [column, f"{column}_count"]
    return result


# --- Plotting functions ---

def plot_bar_chart(df: pd.DataFrame, x_col: str, y_col: str):
    if x_col not in df.columns or y_col not in df.columns:
        st.warning(f"Columns {x_col} or {y_col} not found in dataset.")
        return
    df_plot = df[[x_col, y_col]].dropna()
    if df_plot.empty:
        st.warning("No valid data to plot.")
        return
    if not pd.api.types.is_numeric_dtype(df_plot[y_col]):
        st.warning(f"Column {y_col} is not numeric.")
        return
    fig, ax = plt.subplots()
    sns.barplot(data=df_plot, x=x_col, y=y_col, ax=ax)
    ax.set_title(f"{y_col} by {x_col}")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    plt.close(fig)

def plot_line_chart(df: pd.DataFrame, x_col: str, y_col: str):
    if x_col not in df.columns or y_col not in df.columns:
        st.warning(f"Columns {x_col} or {y_col} not found in dataset.")
        return
    df_plot = df[[x_col, y_col]].dropna()
    if df_plot.empty:
        st.warning("No valid data to plot.")
        return
    if not pd.api.types.is_numeric_dtype(df_plot[y_col]):
        st.warning(f"Column {y_col} is not numeric.")
        return
    fig, ax = plt.subplots()
    sns.lineplot(data=df_plot, x=x_col, y=y_col, ax=ax, marker="o")
    ax.set_title(f"{y_col} over {x_col}")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    plt.close(fig)

def plot_scatter_chart(df: pd.DataFrame, x_col: str, y_col: str):
    if x_col not in df.columns or y_col not in df.columns:
        st.warning(f"Columns {x_col} or {y_col} not found in dataset.")
        return
    df_plot = df[[x_col, y_col]].dropna()
    if df_plot.empty:
        st.warning("No valid data to plot.")
        return
    if not pd.api.types.is_numeric_dtype(df_plot[y_col]):
        st.warning(f"Column {y_col} is not numeric.")
        return
    fig, ax = plt.subplots()
    sns.scatterplot(data=df_plot, x=x_col, y=y_col, ax=ax)
    ax.set_title(f"{y_col} vs {x_col}")
    st.pyplot(fig)
    plt.close(fig)
