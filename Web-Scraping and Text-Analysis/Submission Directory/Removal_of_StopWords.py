# creating fucntions to do stopwords cleaning....

# import all the modules required here....
from nltk.tokenize import word_tokenize
import os


# now we need to remove all the stop words from article_text
def clean_article_text(article_file_path: str) -> list:
    print(f"{article_file_path} ---> this is the article we are cleaning right now...😎")
    article_text = get_article_text(article_file_path)

    tokenized_text_words = tokenize_article_text(article_text)
    print(
        f"{len(tokenized_text_words)} ---> this is no. of tokens we have from the article....."
    )

    # here removing stopwords from all the stopwords_files given.....
    list_of_stopwords_file = os.listdir("./StopWords-20231016T011953Z-001/StopWords/")

    for stopwords_file in list_of_stopwords_file:
        stopwords = get_stopwords(
            f"./StopWords-20231016T011953Z-001/StopWords/{stopwords_file}"
        )
        tokenized_text_words = [
            word for word in tokenized_text_words if word.lower() not in stopwords
        ]

    # Removing the puntuations from the tokens we created....
    tokenized_text_words = [
        word for word in tokenized_text_words if word not in "\"#$&'(),-./:;[\\]^_`{|}~"
    ]
    cleaned_tokens = tokenized_text_words
    print(len(cleaned_tokens), "---> this is the no. of tokens after cleaning")

    # we cannot store the cleaned tokens in files here in this function because this will repeatedly overwrite these files
    # everytime this function run...
    return cleaned_tokens


# creating function to get text of articles for stopwords cleaning
def get_article_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        article_text = file.read()
    return article_text


# tokenize the text we get from article.....
def tokenize_article_text(article_text: str) -> list:
    tokenized_words = word_tokenize(article_text)
    return tokenized_words


# removing all the stopwords(provided in Stopwords directory) from the tokenized_words created using  article....
# getting stop words from files
def get_stopwords(path: str) -> list:
    with open(path, "rb") as file:
        file = file.readlines()

    # removing the byte 'b' from the words
    n = 0
    for word in file:
        file[n] = word.decode("iso-8859-1")
        n += 1

    # removing the | and '\n' char from the word.
    file = [word.split("|")[0].rstrip().lower() for word in file]

    return file


# store these refined tokens of articles in files, name equal to those file
def store_tokenized_clean_article(path: str, cleaned_article_tokens: list) -> None:
    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(word for word in cleaned_article_tokens))
    print(f"The cleaned tokens of articles has been written in file----{path}✌️❤️")


# executing the above functions to clean the article text.....
if __name__ == "__main__":
    list_of_articles = os.listdir("./articles_text/")[1:]
    list_of_stopwords_file = os.listdir("./StopWords-20231016T011953Z-001/StopWords/")

    # implementing....
    try:
        for article_file in list_of_articles:
            # creating file path to store cleaned tokens of article....
            clean_token_file_path = f"./Cleaned-Articles/{article_file}"

            # calling function to clean the article text
            cleaned_tokens = clean_article_text(
                article_file_path=f"./articles_text/{article_file}"
            )

            # storing the cleaned tokens
            store_tokenized_clean_article(clean_token_file_path, cleaned_tokens)
        print()
        print("Happy!Happy!Happy, everything happened seemlessly.......🙃😊🤪")

    except Exception as e:
        print(f"Exception: {e}")
