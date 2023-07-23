import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import ast
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.metric_cards import style_metric_cards

st.title('Projects Data Visualization 🫰')

df = pd.read_csv('data\projects.csv')


# Use boolean indexing to filter out rows where the 'win' column contains {} or the substring '[]'
filtered_df = df[~(df['win'] == '{}') & ~df['win'].str.contains('\[\]')]

# Reset the index of the DataFrame
filtered_df.reset_index(drop=True, inplace=True)

st.subheader('Word Cloud of Prize Names')

# Define a function to extract the 'prizeNames' from the 'win' column
def extract_prize_names(win_data):
    try:
        win_dict = ast.literal_eval(win_data)
        return win_dict[list(win_dict.keys())[0]][0]
    except:
        return None

# Apply the function to create a new column 'prizeNames' in 'filtered_df'
filtered_df['prizeNames'] = filtered_df['win'].apply(extract_prize_names)

# Assuming you have a DataFrame called 'df' with the 'tags' column
# Filter out NaN values from the 'tags' column
filtered_df = filtered_df.dropna(subset=['prizeNames'])

df1 = dataframe_explorer(filtered_df, case=False)
st.dataframe(df1, use_container_width=True,
             column_config={
                 "link": st.column_config.LinkColumn("link")
             }, hide_index=True)

# Extract the 'tags' column as text data
text_data = ",".join(filtered_df['prizeNames'])

# Create a WordCloud object
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)

# Display the generated word cloud using matplotlib
fig = plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

st.pyplot(fig)


# Process the text data to get word frequencies as a dictionary
word_freq = wordcloud.process_text(text_data)

# Sort the word frequencies dictionary by frequency in descending order
sorted_word_freq = {k: v for k, v in sorted(word_freq.items(), key=lambda item: item[1], reverse=True)}

# Extract the words and frequencies in descending order
words = list(sorted_word_freq.keys())
frequencies = list(sorted_word_freq.values())

# Print the words and frequencies in descending order
print("Word Frequencies (Descending Order):")
i = 0
for word, freq in sorted_word_freq.items():
    i += 1
    if i > 15: break
    print(f"{word}: {freq}")