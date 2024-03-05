import streamlit as st
import plotly.express as px
import pandas as pd
import altair as alt
import pycountry
import plotly.graph_objects as go

st.set_page_config(
    page_title = "User Details Page",
    page_icon=":coffee:",
    layout="wide",
    initial_sidebar_state="expanded")

# load data
sampled_df = pd.read_csv('C:/Users/MACTECH/OneDrive/Desktop/4.2/REAL PROJECT/csv/preprocessed.csv')

# Get the top Users
def select_users_by_followers(df):
    # Sort the dataframe by 'User Followers' column in descending order
    sorted_df = df.sort_values(by='User Followers', ascending=False)
    
    # Get the first n usernames based on the sorted dataframe
    selected_users = sorted_df['Username'].head(5).tolist()
    
    return selected_users

# Example usage
top_users = select_users_by_followers(sampled_df)

# # Display suggested hashtags 
st.sidebar.title('Suggested Users')
selected_user = st.sidebar.selectbox('Choose a User', top_users)

# Columns
col = st.columns((3, 5, 3), gap='medium')

# format the count
def format_follower_count(count):
    if count >= 1_000_000:
        return f"{count/1_000_000:.1f}M"
    elif count >= 1_000:
        return f"{count/1_000:.1f}K"
    else:
        return str(count)

# visualize the follower count
def visualize_follower_count_distribution(selected_user, df):
    user_data = df[df['Username'] == selected_user]
    
    follower_count = user_data['User Followers'].iloc[0]
    formatted_count = format_follower_count(follower_count)

    st.info(f"{selected_user}: {formatted_count}")

# visualize the following count
def visualize_following_count_distribution(selected_user, df):
    user_data = df[df['Username'] == selected_user]
    
    follower_count = user_data['User Following'].iloc[0]
    formatted_count = format_follower_count(follower_count)

    st.info(f"{selected_user}: {formatted_count}")

# Visualize the Location
def map_tweet_locations_to_country(df):
    country_codes = {}
    for country in pycountry.countries:
        country_codes[country.name] = country.alpha_3
    
    df['Country Code'] = df['Tweet Location'].map(country_codes.get)
    df['Country'] = df['Tweet Location']
    return df

def visualize_tweet_location_choropleth(selected_user, df):
    user_data = df[df['Username'] == selected_user]
    user_data = map_tweet_locations_to_country(user_data)
    
    fig = px.choropleth(user_data, 
                        locations='Country Code', 
                        color='Country Code',
                        hover_name='Country',
                        title=f'Tweet Locations for User: {selected_user}')
    
    fig.update_layout(geo=dict(showframe=True, showcoastlines=True,
                                projection_type='equirectangular'),
                      template='plotly_dark',
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      paper_bgcolor='rgba(0, 0, 0, 0)',
                      height = 350)
    
    return fig


# Visualize Tweet Type Distribution
def visualize_tweet_type_distribution(selected_user, df):
    user_tweets = df[df['Username'] == selected_user]
    tweet_types = user_tweets['Tweet Type'].unique()
    
    for tweet_type in tweet_types:
        st.info(f"Tweet Type: {tweet_type}")

# Visualize Total Tweet Type Distribution
def visualize_total_tweet_types(selected_user, df):
    user_tweets = df[df['Username'] == selected_user]
    tweet_counts = user_tweets['Tweet Type'].value_counts()
    
    tweet_info = " ".join([f"{tweet_type}s: {count}" for tweet_type, count in tweet_counts.items()])
    st.info(tweet_info)

# Tweet Language Distribution
def visualize_tweet_language_distribution(selected_user, df):
    user_tweets = df[df['Username'] == selected_user]
    tweet_languages = user_tweets['Tweet Language'].unique()
    
    language_info = ", ".join(tweet_languages)
    st.info(f"Tweet Languages used by {selected_user}: {language_info}")

# Visualize the Account Creation Date
def visualize_account_creation_time(selected_user, df):
    user_data = df[df['Username'] == selected_user]
    account_creation_time = user_data['User Account Creation Date'].iloc[0]
    
    st.info(f"Account Creation Time for {selected_user}: {account_creation_time}")

# Visualize User Engangemenet metrics
def visualize_user_engagement_metrics(selected_user, df):
    user_data = df[df['Username'] == selected_user]
    user_followers = user_data['User Followers']
    user_following = user_data['User Following']
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=user_data.index, y=user_followers, mode='lines', name='User Followers'))
    fig.add_trace(go.Scatter(x=user_data.index, y=user_following, mode='lines', name='User Following'))

    fig.update_layout(title=f'User Engagement Metrics for {selected_user}',
                      xaxis_title='Index',
                      yaxis_title='Count')

    return fig


with col[0]:
    st.markdown('#### User Followers')
    visual_users = visualize_follower_count_distribution(selected_user, sampled_df)
    st.markdown('### User Following')
    following = visualize_following_count_distribution(selected_user, sampled_df)
    st.markdown('### Language')
    language = visualize_tweet_language_distribution(selected_user, sampled_df)

with col[1]:
    st.markdown('### Account Creation')
    visualize_account_creation_time(selected_user, sampled_df)
    st.markdown('### Location')
    location = visualize_tweet_location_choropleth(selected_user, sampled_df)
    st.plotly_chart(location, use_container_width=True)
    st.markdown('### User Engangement Metrics')
    user_engangement = visualize_user_engagement_metrics(selected_user, sampled_df)
    st.plotly_chart(user_engangement, use_container_width=True)


with col[2]:
    st.markdown('### Tweet Type')
    visualize_tweet_type_distribution(selected_user, sampled_df)
    st.markdown('### Total Tweet')
    visualize_total_tweet_types(selected_user, sampled_df)
