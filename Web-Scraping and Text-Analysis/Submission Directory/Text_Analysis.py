# Text Analysis ----> calculated all the variables or column values mentioned in the Text Analysis.docx

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import syllables
import pandas as pd
import re
import numpy as np
import os

df = pd.read_csv("Data/Output Data Structure.xlsx - Sheet1.csv")
df.set_index("URL_ID", inplace=True)
# created a generic function which can fill the col of the dataframe with the values provided.
# other than "sentimental Analysis" i donot need the "cleaned_articles" ---> (articles free from stopWords)....


def add_df_col_values(column: str, function) -> None:
    print(f"############## {function}() ----> is started executing ###############")

    if (
        function == positive_score
        or function == negative_score
        or function == subjectivity_score
    ):
        articles_list = os.listdir(f"Cleaned-Articles/")[1:]
    else:
        articles_list = os.listdir(f"articles_text/")[1:]

    for article in articles_list:
        row = float(article.replace(".txt", ""))

        # opening the article files......
        if (
            function == positive_score
            or function == negative_score
            or function == subjectivity_score
        ):
            with open(f"./Cleaned-Articles/{article}", "r", encoding="utf-8") as file:
                article_tokens = file.readlines()
                article_tokens = [word.strip() for word in article_tokens]
            df.loc[row, column] = function(article_tokens)
        else:
            with open(f"./articles_text/{article}", "r", encoding="utf-8") as file:
                raw_article_text = file.read()
            df.loc[row, column] = function(raw_article_text)
    print(
        f"############## {function}() ----> is executed successfully, moving on to next function ###############"
    )


# 1) POSITIVE SCORE
def positive_score(article_tokens: list) -> int:
    # getting the positive provided in assaignment..
    with open(
        "MasterDictionary-20231016T012001Z-001/MasterDictionary/positive-words.txt", "r"
    ) as file:
        positive_words = file.readlines()
        positive_words = [word.strip() for word in positive_words]

    # calculating the positive score....
    # positive_score...
    positive_tokens = np.array(
        [[word, 1] for word in article_tokens if word in positive_words]
    )
    positive_score = 0
    if positive_tokens.size != 0:
        positive_score = (positive_tokens[:, 1]).astype(int).sum()

    return positive_score


# 2) Negative Score
def negative_score(article_tokens: list) -> int:
    # getting the negative provided in assaignment...
    with open(
        "MasterDictionary-20231016T012001Z-001/MasterDictionary/negative-words.txt", "r"
    ) as file:
        negative_words = file.readlines()
        negative_words = [word.strip() for word in negative_words]

    # calculating the negative score.....
    # negative_score.....
    negative_tokens = np.array(
        [[word, -1] for word in article_tokens if word in negative_words]
    )
    negative_score = 0
    if negative_tokens.size != 0:
        negative_score = (negative_tokens[:, 1]).astype(int).sum() * -1

    return negative_score


# 3) Polarity Score:
# Polarity Score = (Positive Score – Negative Score)/ ((Positive Score + Negative Score) + 0.000001)
# "Polarity Score" can be found easily using pandas dataframe properties....


# 4) Subjectivity Score:
# Subjectivity Score = (Positive Score + Negative Score)/ ((Total Words after cleaning) + 0.000001)
def subjectivity_score(article_tokens: list) -> float:
    pos_score = positive_score(article_tokens)
    neg_score = negative_score(article_tokens)
    score = np.round((pos_score + neg_score) / ((len(article_tokens)) + 0.000001), 2)
    return score


# 5) calcualte the 'Average Sentence Length'
def average_Sentence_Length(article_text):
    sent_tokens = sent_tokenize(article_text)
    word_tokens = word_tokenize(article_text)
    avg_sent_length = len(word_tokens) / len(sent_tokens)
    return int(np.round(avg_sent_length))


# 6) Percentage of Complex words = the number of complex words / the number of words
# all the edge cases for finding the number of syllables in words are being handled in the 'python library syllables'.
def percentage_of_complex_words(article_text):
    word_tokens = word_tokenize(article_text)
    complex_words = [word for word in word_tokens if syllables.estimate(word) > 2]
    percentage_complex_words = (len(complex_words) / len(word_tokens)) * 100
    return np.round(percentage_complex_words, 2)


# 7) To calculate ----> Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)
# but we donot need to create the fog_index function to calculate it because pandas can take care of it much easily....


# 8) Average Number of Words Per Sentence
# when calculated for the same text, the values for average sentence length and average number of words per sentence will be
# the same. These two metrics provide different insights into the text, but because they are derived from the same data
# (the text's words and sentences), they will yield identical numerical results.
def average_num_words_per_sentence(article_text):
    return average_Sentence_Length(article_text)


# 9) Complex Word Count
def complex_word_count(article_text):
    word_tokens = word_tokenize(article_text)
    complex_words = [word for word in word_tokens if syllables.estimate(word) > 2]
    return len(complex_words)


# 10) Word Count
# We count the total cleaned words present in the text by.....
# i) removing the stop words (using stopwords class of nltk package).
# ii) removing any punctuations like ? ! , . from the word before counting.
def word_count(article_text):
    word_tokens = word_tokenize(article_text)
    # removing the stopwords...
    word_tokens = [
        word for word in word_tokens if word not in stopwords.words("english")
    ]
    # removing the punctuations.....
    word_tokens = [word for word in word_tokens if word not in string.punctuation]
    return len(word_tokens)


# 11) Syllable Count Per Word
def syllable_count_per_word(article_text):
    word_tokens = word_tokenize(article_text)
    syllables_per_word = np.array([syllables.estimate(word) for word in word_tokens])
    return np.round(syllables_per_word.mean())


# 12) Personal Pronouns
#  “I,” “we,” “my,” “ours,” and “us” and beware of US as it is not personal pronoun.
# "re.I" means check string in a case insensitive manner
# and (?-i:us) ----> inline modifier group where matching is CASE SENSITIVE, and this only matches 'us' (not 'US')
def count_personal_pronouns(article_text):
    word_tokens = word_tokenize(article_text)
    regex = re.compile(r"\b(I|we|my|ours|(?-i:us))\b", re.I)
    personal_pronouns = [word for word in word_tokens if regex.findall(word)]
    return len(personal_pronouns)


# 13) Average Word Length
# Sum of the total number of characters in each word/Total number of words
def average_word_length(article_text):
    word_tokens = word_tokenize(article_text)
    # removing the punctuations.....
    word_tokens = [word for word in word_tokens if word not in string.punctuation]
    avg_word_len = np.array([len(word) for word in word_tokens])
    return np.round(avg_word_len.mean())


if __name__ == "__main__":
    try:
        add_df_col_values("POSITIVE SCORE", positive_score)
        add_df_col_values("NEGATIVE SCORE", negative_score)
        df["POLARITY SCORE"] = np.round(
            (df["POSITIVE SCORE"] - df["NEGATIVE SCORE"])
            / ((df["POSITIVE SCORE"] + df["NEGATIVE SCORE"]) + 0.000001),
            2,
        )
        add_df_col_values("SUBJECTIVITY SCORE", subjectivity_score)
        add_df_col_values("AVG SENTENCE LENGTH", average_Sentence_Length)
        add_df_col_values("PERCENTAGE OF COMPLEX WORDS", percentage_of_complex_words)
        df["FOG INDEX"] = np.round(
            0.4 * (df["AVG SENTENCE LENGTH"] + df["PERCENTAGE OF COMPLEX WORDS"]), 2
        )
        add_df_col_values(
            "AVG NUMBER OF WORDS PER SENTENCE", average_num_words_per_sentence
        )
        add_df_col_values("COMPLEX WORD COUNT", complex_word_count)
        add_df_col_values("WORD COUNT", word_count)
        add_df_col_values("SYLLABLE PER WORD", syllable_count_per_word)
        add_df_col_values("PERSONAL PRONOUNS", count_personal_pronouns)
        add_df_col_values("AVG WORD LENGTH", average_word_length)

        # reseting the integer range(0,113) as the index with following command....
        df.reset_index(drop=False, inplace=True)

        # updating the 'Output Data Structure.xlsx'
        df.to_csv("Data/Output Data Structure.xlsx - Sheet1.csv")

        print()
        print("#####################################################")
        print("Everything happend seemlessly, be ruthless and you can do it🥷❤️")

    except Exception as e:
        print(f"Exception: {e}")
