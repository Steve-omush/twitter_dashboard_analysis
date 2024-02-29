import streamlit as st
import pandas as pd
import plotly.express as px

# Sample data
data = {
    'Date': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05'],
    'Value': [10, 15, 13, 17, 20]
}
df = pd.DataFrame(data)

# Create an interactive line graph with Plotly
fig = px.line(df, x='Date', y='Value', title='Interactive Line Graph')
st.plotly_chart(fig)
