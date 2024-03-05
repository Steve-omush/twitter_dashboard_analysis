# Importing the necessary Libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit.components.v1 as components
import networkx as nx

# Page configuration
st.set_page_config(
    page_title = "Twitter Analysis Dashboard",
    page_icon=":coffee:",
    layout="wide",
    initial_sidebar_state="expanded")

import streamlit as st
import pandas as pd

# Load data
sampled_df = pd.read_csv('C:/Users/MACTECH/OneDrive/Desktop/4.2/REAL PROJECT/csv/preprocessed.csv')


st.markdown("<h1 style='text-align: center;'>Hashtag Analysis</h1>", unsafe_allow_html=True)
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

# # Display suggested hashtags 
st.sidebar.title('Suggested Hashtags')
selected_hashtag = st.sidebar.selectbox('Choose a hashtag', top_hashtags)
selected_hashtag = selected_hashtag.lower()

# # Display a text input for the user to input a hashtag
# custom_hashtag = st.sidebar.text_input('Enter a hashtag', '')
# st.sidebar.write('Custom Hashtag:', custom_hashtag)
# custom_hashtag = custom_hashtag.lower()


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

# Pie chart to show top users of a hashtag
def visualize_top_users(hashtag, df):
    # Filter the dataframe for the given hashtag
    hashtag_df = df[df['Flattened_Hashtags'].str.lower().str.contains(hashtag.lower())]
    
    # Create a new dataframe with Username and User Followers
    top_users_df = hashtag_df[['Username', 'User Followers', 'Tweet Location']]

    # Sort the dataframe by User Followers descending and get the top 5
    top_users_df = top_users_df.sort_values('User Followers', ascending=False).head(5)

    # Create a new column for label including Username and Tweet Location
    top_users_df['label'] = top_users_df['Username'] + ' - ' + top_users_df['Tweet Location']

    # Create a doughnut chart
    fig = px.pie(top_users_df, values='User Followers', names='label', title=f'Top 5 Users by Follower Count for Hashtag: {hashtag}')

    fig.update_traces(textposition='inside', textinfo='percent+label')
    col2.plotly_chart(fig)

# Function to visualize client distribution for a hashtag
def visualize_client_distribution(hashtag, df):
    # Filter the dataframe for the given hashtag
    hashtag_df = df[df['Flattened_Hashtags'].str.lower().str.contains(hashtag.lower())]

    # Count the occurrences of each client type
    client_counts = hashtag_df['Client'].value_counts().head(5).reset_index()
    client_counts.columns = ['Client', 'Count']

    # Calculate the percentage of each client type
    total_clients = client_counts['Count'].sum()
    client_counts['Percentage'] = (client_counts['Count'] / total_clients) * 100

    # Create a pie chart
    fig = px.pie(client_counts, values='Percentage', names='Client', title=f'Percentage of Clients for Hashtag: {hashtag}')
    col2.plotly_chart(fig)



# Function to visualize User Engagement Metrics
def visualize_user_engagement(hashtag, df):
    # Filter dataframe for the selected hashtag
    hashtag_df = df[df['Flattened_Hashtags'].str.lower().str.contains(hashtag.lower())]

    engagement_metrics = hashtag_df.groupby('YearMonth of Tweet').agg({
        'Likes Received': 'sum',
        'Retweets Received': 'sum'
    }).reset_index()
    # Plot line graphs for each metric
    # fig = px.line(grouped_df, x='YearMonth of Tweet', y=['Retweets Received', 'Likes Received'],title=f'User Engagement Metrics for Hashtag: {hashtag}')
    fig = px.line(engagement_metrics, x='YearMonth of Tweet', y=['Likes Received', 'Retweets Received'],
                  title=f'User Engagement Metrics for Hashtag: {hashtag}',
                  labels={'value': 'Count', 'YearMonth of Tweet': 'Year-Month'})
    
    # Update x-axis and y-axis labels
    fig.update_xaxes(title_text='Month')
    fig.update_yaxes(title_text='Count')

    # Display the line graphs
    col1.plotly_chart(fig)

# Location Distribution of Tweets
def visualize_geographical_distribution(hashtag, df):
    # Filter the dataframe for the given hashtag
    hashtag_df = df[df['Flattened_Hashtags'].str.lower().str.contains(hashtag.lower())]

    # Group by 'Tweet Location' and count the number of tweets for each location
    location_counts = hashtag_df['Tweet Location'].value_counts().reset_index()
    location_counts.columns = ['Tweet Location', 'Tweet Count']

    fig = px.choropleth(location_counts, locations='Tweet Location',
                        locationmode='country names',
                        color='Tweet Count',
                        color_continuous_scale='Viridis',
                        title=f'Geographical Distribution of Hashtag: {hashtag}',
                        labels={'Count': 'Tweet Count'})
    fig.update_layout(geo=dict(showframe=True, showcoastlines=True,
                                projection_type='equirectangular'),
                                template='plotly_dark',
                                plot_bgcolor='rgba(0, 0, 0, 0)',
                                paper_bgcolor='rgba(0, 0, 0, 0)')
    col2.plotly_chart(fig)

# Visualize Sentiments of the Hashtag
def visualize_sentiments(hashtag, df):
    # Filter the dataframe for the given hashtag
    hashtag_df = df[df['Flattened_Hashtags'].str.lower().str.contains(hashtag.lower())]

    # Count the occurrences of each sentiment
    sentiment_counts = hashtag_df['Sentiments'].value_counts().head(10).reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']

    # Create a bar chart for sentiment distribution
    fig = px.bar(sentiment_counts, x='Sentiment', y='Count', 
                 title=f'Sentiment Distribution for Hashtag: {hashtag}',
                 labels={'Sentiment': 'Sentiment', 'Count': 'Number of Tweets'},
                 color='Sentiment', color_discrete_map={'Positive': 'green', 'Neutral': 'gray', 'Negative': 'red'})
    fig.update_xaxes(type='category')  # Ensure x-axis treats sentiments as categories
    col1.plotly_chart(fig)

# Trying to Get Follower Details
def visualize_follower_details_by_hashtag(hashtag, df):
    filtered_df = df[df['Flattened_Hashtags'].str.lower().str.contains(hashtag.lower())]
    follower_details = filtered_df[['Tweet Location', 'Username', 'User Followers']].drop_duplicates()
    fig = px.bar(follower_details, x='Tweet Location', y='User Followers', hover_data=['Username'],
                 title=f'Follower Details for #{hashtag}', labels={'User Followers': 'User Followers'})
    col2.plotly_chart(fig)

# Visualize Language Details
def visualize_language_details_by_hashtag(hashtag, df):
    language_distribution = df['Tweet Language'].value_counts().head(7).reset_index()
    language_distribution.columns = ['Language', 'Count']
    
    fig = px.bar(language_distribution, x='Language', y='Count',
                 title='Language Distribution in Tweets', labels={'Count': 'Number of Tweets'})
    col1.plotly_chart(fig)


if selected_hashtag:  # If a hashtag is selected
    visualize_hashtag_2(selected_hashtag, format_df)
    visualize_hashtag_line(selected_hashtag, format_df)
    visualize_top_users(selected_hashtag, format_df)
    visualize_client_distribution(selected_hashtag, format_df)
    visualize_user_engagement(selected_hashtag, format_df)
    visualize_geographical_distribution(selected_hashtag, format_df)
    visualize_sentiments(selected_hashtag, format_df)
    visualize_follower_details_by_hashtag(selected_hashtag, format_df)
    visualize_language_details_by_hashtag(selected_hashtag, format_df)
    # generate_wordcloud(selected_hashtag, format_df) 


# else:  # If a custom hashtag is enetered
#     hashtag_2 = custom_hashtag
#     visualize_hashtag_2(hashtag_2, format_df)
#     visualize_hashtag_line(hashtag_2, format_df)
#     visualize_top_users(hashtag_2, format_df)
