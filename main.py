import streamlit as st
import pandas as pd
import numpy as np
import validators
from util import code_analysis, auth
from streamlit_extras.dataframe_explorer import dataframe_explorer

# page title
st.title('Code Analysis')

user_input = st.text_input(
    "Input your own GitHub Repo Link (e.g. https://github.com/hua-lun/agent_bucky)")


if not user_input or not validators.url(user_input):
    user_input = 'https://github.com/PrideHacks-2023/mapper'


@st.cache_data
def load_data(url):
    d1, d2 = code_analysis.stats(url)
    return d1, d2


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data1, data2 = load_data(user_input)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache_data)")

# table
#if st.checkbox('Show table with raw data'):
st.subheader('Lines of Code Table')
df1 = dataframe_explorer(data1, case=False)
st.dataframe(df1, use_container_width=True)
st.subheader('Cyclomatic Complexity Table')
df2 = dataframe_explorer(data2, case=False)
st.dataframe(df2, use_container_width=True)

