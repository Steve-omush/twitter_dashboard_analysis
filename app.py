import streamlit as st
import plotly.express as px
import pandas as pd
import altair as alt
import pycountry
import plotly.graph_objects as go
from pathlib import Path
import streamlit_authenticator as stauth
import pickle


st.set_page_config(
    page_title = "User Details Page",
    page_icon=":coffee:",
    layout="wide",
    initial_sidebar_state="expanded")



st.header("First Page of Analysis")



# USER AUTHENTICATOR
names = ["Steve Omush", "Rebecca Jackson"]
usernames = ["somush", "rjackson"]

# Load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)


authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "twitter_dashboard", "abcdef", cookie_expiry_days=10)

names, authentication_status, username = authenticator.login("Login", "main")

