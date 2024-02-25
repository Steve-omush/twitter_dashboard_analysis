import streamlit as st

import requests
from bs4 import BeautifulSoup

#data
import json
import pandas as pd

#plotting
import plotly.express as px
import seaborn as sns

st.title("Trying an app")

def get_count(tag):
    url = f"https://www.instagram.com/explore/tags"
    s = requests.get(url)
    soup = BeautifulSoup(s.content)
    return int(soup.find_all("meta")[6]["content"].split)