import streamlit as st
import pandas as pd
from utils import (
    basic_analysis, group_by_analysis, top_n_values,
    plot_bar_chart, plot_line_chart, plot_scatter_chart
)

st.set_page_config(page_title="Data Analyst Chatbot", layout="wide")

st.title("📊 Data Analyst Chatbot")
st.markdown("Upload a CSV file and explore it with built-in analysis and charts.")

# --- Upload CSV ---
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # --- Basic Analysis ---
    if st.checkbox("Show Basic Analysis"):
        st.subheader("Descriptive Statistics")
        st.dataframe(basic_analysis(df))

    # --- Top N values ---
    st.subheader("Top N Values of a Column")
    col = st.selectbox("Select column for top values", df.columns)
    n = st.slider("Select N", min_value=1, max_value=20, value=5)
    st.dataframe(top_n_values(df, col, n))

    # --- Group by Analysis ---
    st.subheader("Group By Sum")
    group_col = st.selectbox("Select column to group by", df.columns)
    value_col = st.selectbox("Select numeric column to sum", df.select_dtypes(include="number").columns)
    st.dataframe(group_by_analysis(df, group_col, value_col))

    # --- Plotting ---
    st.subheader("Charts")
    x_col = st.selectbox("X-axis column", df.columns, key="x_col")
    y_col = st.selectbox("Y-axis column (numeric)", df.select_dtypes(include="number").columns, key="y_col")
    
    chart_type = st.radio("Select chart type", ["Bar Chart", "Line Chart", "Scatter Chart"])
    if chart_type == "Bar Chart":
        plot_bar_chart(df, x_col, y_col)
    elif chart_type == "Line Chart":
        plot_line_chart(df, x_col, y_col)
    elif chart_type == "Scatter Chart":
        plot_scatter_chart(df, x_col, y_col)
else:
    st.info("Please upload a CSV file to get started.")
