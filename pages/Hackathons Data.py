import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.metric_cards import style_metric_cards

st.title('Hackathons Data Visualization <3')

df = pd.read_csv('data/hackathons.csv')

df1 = dataframe_explorer(df, case=False)
st.dataframe(df1, use_container_width=True,
             column_config={
                 "link": st.column_config.LinkColumn("hackathon_link")
             }, hide_index=True)

st.subheader('Word Cloud of Hackathon Tags')

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

# Filter out rows with currency values equal to "$"
filtered_df = filtered_df[filtered_df['currency'] == '$']

# Draw a scatter plot of 'price' against 'participants'
fig2 = plt.figure(figsize=(8, 6))
plt.scatter(filtered_df['participants'], filtered_df['price'], alpha=0.5, color='#9370DB')
plt.xlabel('Participants')
plt.ylabel('Prize pool')
plt.title('Scatter Plot: Price vs Participants (Currency: $)')
plt.show()

st.pyplot(fig2)


#############################

import pandas as pd

# Calculate the total number of rows in the DataFrame
total_rows = len(df)

# Calculate the number of rows where the location is listed as "online"
online_count = df['location'].str.lower().str.contains('online').sum()

# Calculate the percentage of locations that are listed as "online"
percentage_online = (online_count / total_rows) * 100

col1, col2 = st.columns(2)
col1.metric(label="Percentage of locations listed as 'online'", value=f'{percentage_online:.2f}%', delta="")
style_metric_cards()

#############################

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

#############################

st.subheader('Hackathons through the years')

# Extract the first 3 letters of each period as the month and create a new column 'month'
filtered_df['month'] = filtered_df['period'].str[:3]

custom_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Create a histogram of the extracted months
fig4 = plt.figure(figsize=(8, 6))
filtered_df['month'].value_counts().reindex(custom_order).plot(kind='bar', color='purple')
plt.xlabel('Month')
plt.ylabel('Frequency')
plt.title('Hackathons each month')
plt.xticks(rotation=0)

st.pyplot(fig4)

#############################

# Extract the year from the 'period' column and convert it to an integer column 'year'
filtered_df['year'] = filtered_df['period'].str[-4:].astype(int)

#############################

# Group the DataFrame by 'year' and 'month' and count the occurrences
hackathons_count = filtered_df.groupby(['year', 'month']).size().reset_index(name='count')

# Create a pivot table to rearrange the data for plotting
pivot_table = hackathons_count.pivot(index='month', columns='year', values='count')

# Get the sorted months to display on the x-axis in order
sorted_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Plot the line graph
fig5 = plt.figure(figsize=(10, 6))
for year in pivot_table.columns:
    plt.plot(sorted_months, pivot_table[year], label=str(year))

plt.xlabel('Month')
plt.ylabel('Number of Hackathons')
plt.title('Number of Hackathons Each Month')
plt.legend(title='Year', loc='upper left', bbox_to_anchor=(1, 1))
plt.xticks(rotation=45)
plt.grid(True)

st.pyplot(fig5)

#############################

st.subheader('Major League Hacking Hackathons')

MajorLeagueHacking_df = filtered_df[(filtered_df['organizer'] == 'Major League Hacking')]

df2 = dataframe_explorer(MajorLeagueHacking_df, case=False)
st.dataframe(df2, use_container_width=True,
             column_config={
                 "link": st.column_config.LinkColumn("hackathon_link")
             }, hide_index=True)

#############################

# import nltk
from nltk.probability import FreqDist
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Extract the 'tags' column as text data
text_data_mlh = ",".join(MajorLeagueHacking_df['tags'])

# Tokenize the text data into words
words = text_data_mlh.split(' ')

# Calculate the frequency of each word
word_freq = {}
for word in words:
    word_freq[word] = word_freq.get(word, 0) + 1

# Sort the words based on frequency and get the 10 most frequent words to remove
top_words = sorted(word_freq, key=word_freq.get, reverse=True)[:10]

# Remove the top 10 most frequent words from the list of words
filtered_words = [word for word in words if word not in top_words]

# Join the filtered words back into a single text
filtered_text = " ".join(filtered_words)

# Generate the word cloud from the filtered text
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(filtered_text)

# Plot the word cloud
fig6 = plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('MLH Tags Word Cloud')
plt.show()

st.pyplot(fig6)

# Note as markdown
st.markdown('''
The word cloud above shows the most common tags used by MLH in their hackathons.
''')