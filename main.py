import streamlit as st
import re
import nltk
nltk.download('stopwords')
nltk.download('vader_lexicon')
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer

def most_used_words(text):

    pattern = re.compile("[a-zA-Z]+")
    words = re.findall(pattern, text.lower())

    no_of_words = len(set(words))

    word_count = {}

    for word in words:
        if word not in word_count.keys():
            word_count[word] = 1
        else:
            word_count[word] += 1

    sorted_word_count = sorted([(value, keyword) for (keyword, value) in word_count.items()], reverse=True)



    english_stopwords = stopwords.words("english")
    filtered_sorted_word_count = []

    for count, word in sorted_word_count:
        if word not in english_stopwords:
            filtered_sorted_word_count.append((count, word))

    return filtered_sorted_word_count, sorted_word_count, words, no_of_words

def see_tone(text):
    analyzer = SentimentIntensityAnalyzer()

    return analyzer.polarity_scores(text)


st.header("Natural Language Proccessing")
st.write("Natural language processing (NLP) is a subfield of computer science and artificial intelligence (AI) that uses machine learning to enable computers to understand and communicate with human language.")

st.subheader("Enter text and select the functions to do on the text")

text = st.text_area("Type Text and press Ctr + Enter")

text_function = st.selectbox("Select a function", ("See the most used words", "See if the text is positive/negative"))

if text_function == "See the most used words":
    include_stopwords = st.checkbox("Include Stop Words?", help="Stop words are common words in a language, like 'the', 'a', 'is', 'and', that are typically removed during text processing tasks like natural language processing and search engine indexing")

    if include_stopwords == False:
        no_of_words = len(most_used_words(text)[0])
    else:
        no_of_words = len(most_used_words(text)[1])


if text != "":
    if text_function == "See the most used words":
        if no_of_words <= 5:
            no_of_top_words = st.slider("Select the number of top words you want", min_value=1, max_value=no_of_words, value=no_of_words)
        else:
            no_of_top_words = st.slider("Select the number of top words you want", min_value=1, max_value=no_of_words, value=5)
            
        st.subheader(f"The Top {no_of_top_words} Words in your string were:")
        
        col1, col2, col3 = st.columns([2, 5, 3])

        col1.markdown("**Word Rank**")
        col2.markdown("**Top Words**")
        col3.markdown("**Occurance**")


        if include_stopwords == False:
            for i in range(no_of_top_words):
                if most_used_words(text)[0][i][0] > 1:
                    col1.write(f"{i+1} ")
                    col2.markdown(f"The word **{most_used_words(text)[0][i][1]}** occured")
                    col3.markdown(f"**{most_used_words(text)[0][i][0]}** times.")
                else:
                    col1.write(f"{i+1}")
                    col2.write(f"The word **{most_used_words(text)[0][i][1]}** occured")
                    col3.markdown(f"**{most_used_words(text)[0][i][0]}** time.")
        else:
            for i in range(no_of_top_words):
                if most_used_words(text)[1][i][0] > 1:
                    col1.write(f"{i+1} ")
                    col2.markdown(f"The word **{most_used_words(text)[1][i][1]}** occured")
                    col3.markdown(f"**{most_used_words(text)[1][i][0]}** times.")
                else:
                    col1.write(f"{i+1}")
                    col2.markdown(f"The word **{most_used_words(text)[1][i][1]}** occured")
                    col3.markdown(f"**{most_used_words(text)[1][i][0]}** time.")


    elif text_function == "See if the text is positive/negative":

        st.subheader("Tone Score of the Entered Text")

        st.write(f"Positive Score: {see_tone(text)['pos'] * 10}/10")
        st.write(f"Neutral Score: {see_tone(text)['neu'] * 10}/10")
        st.write(f"Negative Score: {see_tone(text)['neg'] * 10}/10")

        st.markdown(f"**Overall Score: {see_tone(text)['compound'] * 10}**")
        st.write("(The score can be between -10 to +10, where -10 to 0 represents negative tone and 0 to 10 represents positive tone)")
