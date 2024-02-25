# Importing the necessary Libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns


# Page configuration
st.set_page_config(
    page_title = "Twitter Analysis Dashboard",
    page_icon=":coffee:",
    layout="wide",
    initial_sidebar_state="expanded")
alt.themes.enable("dark")


import streamlit as st
import pandas as pd

# Load data
sampled_df = pd.read_csv('C:/Users/MACTECH/OneDrive/Desktop/4.2/REAL PROJECT/csv/preprocessed.csv')


# Function to get top 5 hashtags
def get_top_hashtags(df):
    # Flatten the hashtags column
    flattened_hashtags = [tag.strip() for sublist in df['Flattened_Hashtags'] for tag in sublist.split(',')]

    # Create a pandas Series from the flattened list of hashtags
    hashtag_counts = pd.Series(flattened_hashtags)

    # Count the occurrences of each hashtag and select the top 5
    top_hashtags = hashtag_counts.value_counts().head(5).index.tolist()
    
    return top_hashtags

# Get top hashtags
top_hashtags = get_top_hashtags(sampled_df)

# Display suggested hashtags
st.sidebar.title('Suggested Hashtags')
selected_hashtag = st.sidebar.selectbox('Choose a hashtag', top_hashtags)
selected_hashtag = selected_hashtag.lower()

# Display a text input for the user to input a hashtag
custom_hashtag = st.sidebar.text_input('Enter a hashtag', '')
st.sidebar.write('Custom Hashtag:', custom_hashtag)
custom_hashtag = custom_hashtag.lower()


# Function to convert the hashtags to lowercase and split them
def format_hashtag(df):
    # Convert hashtags to lowercase and split them
   df['Flattened_Hashtags'] = df['Flattened_Hashtags'].str.lower().str.split(',')
   return df

format_df = format_hashtag(sampled_df)

# split the columns into 2
col1, col2 = st.columns([2, 1])

# Visualization of the hashtags over time
# Visualization for Bar graph
def visualize_hashtag_2(hashtag, df):
    df['Flattened_Hashtags'] = df['Flattened_Hashtags'].astype(str)

    # Filter the dataframe for the given hashtag
    # hashtag_df = df[df['Flattened_Hashtags'].apply(lambda x: True if hashtag.lower() in x else False)]
    hashtag_df = df[df['Flattened_Hashtags'].str.lower().str.contains(hashtag.lower())]

    # Create a bar chart
    # hashtag_counts = hashtag_df['YearMonth of Tweet'].value_counts().reset_index()
    hashtag_counts = hashtag_df.groupby('YearMonth of Tweet').size().reset_index(name='Count')
    hashtag_counts.columns = ['YearMonth of Tweet', 'Count']  # Rename columns
    fig = go.Figure(data=[go.Bar(x=hashtag_counts['YearMonth of Tweet'], y=hashtag_counts['Count'],marker_color='red')]) 
    fig.update_layout(
        title=f'Distribution of Hashtag: {hashtag} Over Time',
        xaxis_title='YearMonth of Tweet',
        yaxis_title='Count',
        xaxis_tickangle=-45,
        showlegend=False
    )
    col1.plotly_chart(fig)

#visualization for line graph
def visualize_hashtag_line(hashtag, df):
    # Convert the 'Flattened_Hashtags' column to string
    df['Flattened_Hashtags'] = df['Flattened_Hashtags'].astype(str)

    # Filter the dataframe for the given hashtag
    hashtag_df = df[df['Flattened_Hashtags'].str.lower().str.contains(hashtag.lower())]

    # Group by YearMonth of Tweet and count the occurrences
    hashtag_counts = hashtag_df.groupby('YearMonth of Tweet').size().reset_index(name='Count')

    # Create an interactive line graph
    fig = go.Figure(data=go.Scatter(x=hashtag_counts['YearMonth of Tweet'], y=hashtag_counts['Count'],
                                    mode='lines+markers', marker_color='salmon'))  # Custom color for line graph
    fig.update_layout(
        title=f'Distribution of Hashtag: {hashtag} Over Time',
        xaxis_title='YearMonth of Tweet',
        yaxis_title='Count'
    )
    col1.plotly_chart(fig)


def visualize_top_users(hashtag, df):
    # Filter the dataframe for the given hashtag
    hashtag_df = df[df['Flattened_Hashtags'].str.lower().str.contains(hashtag.lower())]
    
    # Create a new dataframe with Username and User Followers
    top_users_df = hashtag_df[['Username', 'User Followers']]

    # Sort the dataframe by User Followers descending and get the top 5
    top_users_df = top_users_df.sort_values('User Followers', ascending=False).head(5)
    # Create a doughnut chart
    fig = px.pie(top_users_df, values='User Followers', names='Username', title=f'Top 5 Users by Follower Count for Hashtag: {hashtag}')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    col2.plotly_chart(fig)


if selected_hashtag:  # If a hashtag is selected
    visualize_hashtag_2(selected_hashtag, format_df)
    visualize_hashtag_line(selected_hashtag, format_df)
    visualize_top_users(selected_hashtag, format_df)
else:  # If a custom hashtag is enetered
    hashtag_2 = custom_hashtag
    visualize_hashtag_2(hashtag_2, format_df)
    visualize_hashtag_line(hashtag_2, format_df)
    visualize_top_users(hashtag_2, format_df)

