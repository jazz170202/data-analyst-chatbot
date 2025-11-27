import pandas as pd
import streamlit as st
from utils import basic_analysis, group_by_analysis, top_n_values, plot_bar_chart, plot_line_chart, plot_scatter_chart

# Streamlit page config
st.set_page_config(page_title="Data Analyst Chatbot", layout="wide")
st.title("💻 Data Analyst Chatbot - Menu Version (Matplotlib/Seaborn)")

# Upload CSV
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.subheader("Data Preview")
    st.dataframe(df.head())

    st.subheader("Choose Analysis")
    menu = [
        "Basic Statistics",
        "Top N Values",
        "Group-by Sum",
        "Bar Chart",
        "Line Chart",
        "Scatter Plot"
    ]
    choice = st.selectbox("Select an action", menu)

    if choice == "Basic Statistics":
        st.subheader("Basic Statistics")
        st.dataframe(basic_analysis(df))

    elif choice == "Top N Values":
        cat_cols = df.select_dtypes(include='object').columns.tolist()
        if cat_cols:
            col = st.selectbox("Select a categorical column", cat_cols)
            n = st.number_input("How many top values?", min_value=1, max_value=20, value=5)
            st.dataframe(top_n_values(df, col, n))
        else:
            st.warning("No categorical columns found.")

    elif choice == "Group-by Sum":
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        if numeric_cols:
            group_col = st.selectbox("Group by column", df.columns, key="group")
            value_col = st.selectbox("Sum numeric column", numeric_cols, key="sum")
            result = group_by_analysis(df, group_col, value_col)
            st.write(result)
        else:
            st.warning("No numeric columns to aggregate.")

    elif choice in ["Bar Chart", "Line Chart", "Scatter Plot"]:
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        if numeric_cols:
            x_col = st.selectbox("X-axis column", df.columns, key="x")
            y_col = st.selectbox("Y-axis column", numeric_cols, key="y")
            if choice == "Bar Chart":
                plot_bar_chart(df, x_col, y_col)
            elif choice == "Line Chart":
                plot_line_chart(df, x_col, y_col)
            else:
                plot_scatter_chart(df, x_col, y_col)
        else:
            st.warning("No numeric columns available for plotting.")
