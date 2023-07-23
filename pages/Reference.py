import streamlit as st
import pandas as pd

st.title('Reference')

st.markdown("Used **Radon** Python library to compute code metrics. [Click here to learn more!]("
            "https://radon.readthedocs.io/en/latest/intro.html)")

st.subheader('Abbreviations Explained')
legend = [
    {"Name": "loc", "Description": "Lines of Code", "Detail": "Total lines of code written in the file"},
    {"Name": "lloc", "Description": "Logical Lines of Code", "Detail": "Line of Code that be executable / a statement"},
    {"Name": "sloc", "Description": "Source Lines of Code", "Detail": "Size of program, based on lines of code"}
]
df1 = pd.DataFrame(legend)
st.dataframe(df1, hide_index=True)

st.subheader('Cyclomatic Complexity Explained')
st.markdown("Extracted from [Radon Documentation]("
            "https://radon.readthedocs.io/en/latest/api.html#module-radon.complexity)")

table = [
    {"Rank": "1 - 5", "Score": "A (low risk - simple block)"},
    {"Rank": "6 - 10", "Score": "B (low risk - well structured and stable block)"},
    {"Rank": "11 - 20", "Score": "C (moderate risk - slightly complex block)"},
    {"Rank": "21 - 30", "Score": "D (more than moderate risk - more complex block)"},
    {"Rank": "31 - 40", "Score": "E (high risk - complex block, alarming)"},
    {"Rank": "41 and above", "Score": "F (very high risk - error-prone, unstable block)"},
]

df2 = pd.DataFrame(table)
st.dataframe(df2, hide_index=True)


