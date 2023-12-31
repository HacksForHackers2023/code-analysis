import streamlit as st
import pandas as pd
import numpy as np
import validators
from util import code_analysis
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.metric_cards import style_metric_cards
import altair as alt

# page title
st.title('Code Analysis')


with st.form("my_form"):
    user_input = st.text_input(
        "Input your own GitHub Repo Link (e.g. https://github.com/HacksForHackers2023/code-analysis)")
    submitted = st.form_submit_button("Submit")
    if not user_input or not validators.url(user_input):
        user_input = 'https://github.com/HacksForHackers2023/code-analysis'


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
st.balloons()

col1, col2, col3 = st.columns(3)
col1.metric(label="Lines of Code", value=data1['loc'].sum())
col2.metric(label="Logical Lines of Code", value=data1['lloc'].sum())
col3.metric(label="Source Lines of Code", value=data1['sloc'].sum())
style_metric_cards()

# table
# if st.checkbox('Show table with raw data'):
st.subheader('Lines of Code Table')
df1 = dataframe_explorer(data1, case=False)
st.dataframe(df1, use_container_width=True,
             column_config={
                 "link": st.column_config.LinkColumn("link")
             }, hide_index=True)

st.subheader('Cyclomatic Complexity Table')
df2 = dataframe_explorer(data2, case=False)
st.dataframe(df2, use_container_width=True,
             column_config={
                 "link": st.column_config.LinkColumn("link")
             }, hide_index=True)

st.subheader('An area chart made from the data')
if st.checkbox('Check the box to view'):
    st.markdown("Abstract art 🎨\n. It looks cool and that's about it for now")
    st.area_chart(df2)
