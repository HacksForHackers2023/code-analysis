import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.metric_cards import style_metric_cards

st.title('Hackathons Data Visualization <3')

df = pd.read_csv('data\hackathons.csv')

df1 = dataframe_explorer(df, case=False)
st.dataframe(df1, use_container_width=True,
             column_config={
                 "link": st.column_config.LinkColumn("link")
             }, hide_index=True)

st.subheader('Word Cloud of Hackathon Tags')

# Assuming you have a DataFrame called 'df' with the 'tags' column
# Filter out NaN values from the 'tags' column
filtered_df = df.dropna(subset=['tags'])

# Extract the 'tags' column as text data
text_data = ",".join(filtered_df['tags'])

# Create a WordCloud object
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)


# Display the generated word cloud using matplotlib
fig1 = plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

st.pyplot(fig1)

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

#############################
st.subheader('Scatter Plot of Prize Pool vs Participants')

# Find all unique values in the 'currency' column
unique_currencies = df['currency'].unique()

# Print the unique values
print(unique_currencies)

# Create a new DataFrame 'df_noNan' by dropping rows with NaN values in any column
df_noNan = df.dropna(how='any')

# Create a copy of the DataFrame
df_noNan2 = df_noNan.copy()

# Assuming you have a DataFrame called 'df' with the 'price', 'participants', and 'currency' columns

# Filter out rows with currency values equal to "$"
filtered_df = filtered_df[filtered_df['currency'] == '$']

# Draw a scatter plot of 'price' against 'participants'
fig2 = plt.figure(figsize=(8, 6))
plt.scatter(filtered_df['participants'], filtered_df['price'], alpha=0.5)
plt.xlabel('Participants')
plt.ylabel('Price')
plt.title('Scatter Plot: Price vs Participants (Currency: $)')
plt.show()

st.pyplot(fig2)


#############################

import pandas as pd

# Assuming you have a DataFrame called 'df' with the 'location' column

# Calculate the total number of rows in the DataFrame
total_rows = len(df)

# Calculate the number of rows where the location is listed as "online"
online_count = df['location'].str.lower().str.contains('online').sum()

# Calculate the percentage of locations that are listed as "online"
percentage_online = (online_count / total_rows) * 100

col1, col2, col3 = st.columns(3)
col1.metric(label="Percentage of locations listed as 'online'", value=f'{percentage_online:.2f}%', delta="")
style_metric_cards()

#############################

# Assuming you have a DataFrame called 'df' with the 'organizer' column
# Filter out rows with NaN values in the 'organizer' column
filtered_df = filtered_df.dropna(subset=['organizer'])

# Extract the 'organizer' column as text data
text_data_organizer = ",".join(filtered_df['organizer'])

# Create a WordCloud object
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data_organizer)

# Display the generated word cloud using matplotlib
fig3 = plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

st.pyplot(fig3)
