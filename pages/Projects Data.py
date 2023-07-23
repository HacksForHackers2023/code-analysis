import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import ast
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.metric_cards import style_metric_cards

st.title('Projects Data Visualization 🫰')

df = pd.read_csv('data/projects.csv')

# Use boolean indexing to filter out rows where the 'win' column contains {} or the substring '[]'
filtered_df = df[~(df['win'] == '{}') & ~df['win'].str.contains('\[\]')]

# Reset the index of the DataFrame
filtered_df.reset_index(drop=True, inplace=True)

# Define a function to extract the 'prizeNames' from the 'win' column
def extract_prize_names(win_data):
    try:
        win_dict = ast.literal_eval(win_data)
        return win_dict[list(win_dict.keys())[0]][0]
    except:
        return None

# Apply the function to create a new column 'prizeNames' in 'filtered_df'
filtered_df['prizeNames'] = filtered_df['win'].apply(extract_prize_names)

# Filter out NaN values from the 'tags' column
filtered_df = filtered_df.dropna(subset=['prizeNames'])

df1 = dataframe_explorer(filtered_df, case=False)
st.dataframe(df1, use_container_width=True,
             column_config={
                 "link": st.column_config.LinkColumn("url")
             }, hide_index=True)

# Extract the 'tags' column as text data
text_data = ",".join(filtered_df['prizeNames'])

# Create a WordCloud object
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)


st.subheader('Word Cloud of Prize Names')

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


#######################

st.subheader('Histogram of Prize wins')

shades_of_purple = ['#9370DB', '#8A2BE2', '#8B008B', '#800080', '#6A5ACD']

# Filter rows with values containing the phrases "Place" or "Runner Up" in the 'prizeNames' column
filtered_df3 = filtered_df[filtered_df['prizeNames'].str.contains('Place|Runner Up', na=False)]

# Create a mapping dictionary to replace variations of prize names
prize_name_mapping = {
    '1st': 'first',
    'First': 'first',
    'first': 'first',
    '2nd': 'second',
    'Second': 'second',
    'second': 'second',
    '3rd': 'third',
    'Third': 'third',
    'third': 'third',
    'Runner Up': 'runner-up',
    'Runner-Up': 'runner-up',
    'runner up': 'runner-up',
    'first runner up': 'second',
    'First Runner Up': 'second',
    'second runner up': 'third',
    'Second Runner Up': 'third',
    # Add other variations and their replacements as needed
}

# Function to apply mapping and reduce prize names
def reduce_prize_names(prize_name):
    prize_name = prize_name.lower()
    for key, value in prize_name_mapping.items():
        if key in prize_name:
            return value
    return 'other'

filtered_df3['prizesReduced'] = filtered_df3['prizeNames'].apply(reduce_prize_names)

# Create a histogram of the values in the 'prize names reduced' column
value_counts = filtered_df3['prizesReduced'].value_counts()

# Plot the histogram
fig2 = plt.figure(figsize=(8, 6))
plt.bar(value_counts.index, value_counts.values, color=shades_of_purple)
plt.xlabel('Prize Names')
plt.ylabel('Frequency')
plt.title('Histogram of Prize types')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

st.pyplot(fig2)

#######################

# Function to count the number of words in a description
def count_words(description):
    words = description.split()
    return len(words)

# Create the new column 'description length' by applying the count_words function
filtered_df3['description length'] = filtered_df3['description'].apply(count_words)

# Function to calculate the average description length for a given prize name
def average_description_length(prize_name, filtered_df3):
    filtered_df3 = filtered_df3[filtered_df3['prizesReduced'] == prize_name]
    return filtered_df3['description'].apply(len).mean()

# List of prize names to analyze
prize_names = ['first', 'second', 'third']

# Compute the average description length for each prize name
average_lengths = [average_description_length(prize_name, filtered_df3) for prize_name in prize_names]

# Plot the results
fig3 = plt.figure(figsize=(8, 6))
plt.bar(prize_names, average_lengths, color=shades_of_purple)
plt.xlabel('Prize Names')
plt.ylabel('Average Description Length')
plt.title('Average Description Length for Different Prizes')
plt.show()

st.pyplot(fig3)

#######################
st.subheader('Number of Authors')

# Function to count the number of authors in the 'authors' column
def count_authors(authors):
    return len(authors)

# Create the new column 'num_authors' by applying the count_authors function
filtered_df3['num_authors'] = filtered_df3['authors'].apply(lambda x: count_authors(eval(x)))

# Define shades of purple
shades_of_purple = ['#9370DB', '#8A2BE2', '#8B008B']

# Filter the DataFrame to include only the top 3 prizes (first, second, third)
top_prizes = ['first', 'second', 'third']
filtered_df4 = filtered_df3[filtered_df3['prizesReduced'].isin(top_prizes)]

# Create subplots for each prize category
fig4, axs = plt.subplots(len(top_prizes), figsize=(8, 6), sharex=True)

# Plot frequency of number of authors for each prize category with separate shades of purple
for i, (prize, shade) in enumerate(zip(top_prizes, shades_of_purple)):
    prize_df = filtered_df4[filtered_df4['prizesReduced'] == prize]
    author_counts = prize_df['num_authors'].value_counts().sort_index()
    axs[i].bar(author_counts.index, author_counts.values, color=shade)
    axs[i].set_xlabel('Number of Authors')
    axs[i].set_ylabel('Frequency')
    axs[i].set_title(f'Frequency for "{prize}" Prize')
    axs[i].set_xticks(author_counts.index)

plt.tight_layout()
plt.show()

st.pyplot(fig4)
