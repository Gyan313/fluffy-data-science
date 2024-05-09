# Importing all the modules needed for DataExtraction......
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

# getting the dataframe....
df = pd.read_csv("Data/Output Data Structure.xlsx - Sheet1.csv")


def get_article_text(link: str) -> list:
    r = requests.get(link)
    # we used "lxml" parser rather than html.parser cause it is fast,lenient and has more features....
    soup = BeautifulSoup(r.text, "lxml")

    # Extracting the article's title.
    title = soup.find("title")
    title = title.get_text()
    title = title.replace(" - Blackcoffer Insights", "")

    # Extracting content of the article.
    # attribute ---> the div that contain the class "td-post-content tagdiv-type" and this class
    # contains the text of all the articles....
    attribute = re.findall(r".*td-post-content tagdiv-type", str(soup))
    if attribute:
        for i in attribute:
            attr = i.split('="')[1]
    else:
        return None
    usefull_text = soup.find("div", attrs={"class": attr})
    article_text = usefull_text.get_text()
    article_text = re.sub(r"Blackcoffer Insights.*|\xa0.*", "", article_text)
    return [title, article_text]


def store_article_text(all_text: list, file_name: str) -> None:
    if all_text == None:
        raise Exception("No text found in the file😊")
    path = f"./articles_text/{file_name}"
    title = all_text[0]
    article_text = all_text[1]
    with open(path, "w", encoding="utf-8") as file:
        file.write(title)
        file.write(article_text)
    print("Text has been written in file.✌️")


if __name__ == "__main__":
    # Extracting text from articles and storing them in files.
    for i in range(len(df)):
        content_article = get_article_text(df["URL"][i])
        file_name = str(df["URL_ID"][i]) + ".txt"
        print(f"##### {i} #####")
        try:
            store_article_text(content_article, file_name)
        except Exception as e:
            print("Exception:", e)

    # "24th" and "37th" row in "df" URL has no article_text present because "url" doesnt have no content.
