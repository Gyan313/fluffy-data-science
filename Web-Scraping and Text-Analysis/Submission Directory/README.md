## Instructions

> _Must visit `objective.docx` file to know the flow of the program from Data_Extraction to Data_Analysis and instructions to do every step of this Assaignment....
> In this file you will get know about all the files used in this Assaignment...._

**Aim** - The objective of this assignment is to extract textual data articles from the given URL and perform text analysis to compute variables that are explained thoroughly in `Text Analysis.docx` file.

`Output Data Structure.xlsx` ------- contain the all the URL's and the variable we need to find in order to do Text Analysis.......
And it is located inside the _Data directory_....

-------- Lets go through each step of this assaignment one by one ----------

1.  **Data Extraction**

    - Program for "Data Extraction" is in file **Data_Extraction.py**
    - This program uses _BeautifulSoup_ module to get text from the article.
    - So ,I made two functions `get_article_text` and `store_article_text` and there purpose is pretty clear by there names.
    - `get_article_text` --- this function uses the _BeautifulSoup_ module to get the title and text of article.This function returns a list containing the _title_ and _text of article_.
    - `store_article_text` ---- this function stores the title and text we got from the `get_article_text` in a folder _article_text_ with file names as _URL_ID_ given in `Output Data Structure.xlsx`.
    - At last we traverse through all the URL's from the column URL of `Output Data Structure.xlsx` and get title and text of all the articles and stored them in _article_text_ directory.
    - We only get the text from 112 articles and 2 articles ( 11668.0.txt and 11668.0.txt ) both doesnt contain any text.

                        **----------------------- Data Extraction Ends Here --------------------------**


2.  **Data Analysis**

> Data Analysis is divided into 2 parts in my program files....

        2.1) Removal of StopWords from Article Text
        2.2) Text Analysis


2.1. **Removal of StopWords from Article Text**

- Program for Removal of StopWords is in file `Removal_of_StopWords.py`
- start going through this program from `get_article_text`. This function returns the text of article from `article_text` directory.
- Then we tokenize this text we get from `get_article_text` using `tokenize_article_text` function.
- After this we need stopWords provided in the Assaignment in the `StopWords` directory.We get this stopwords using the function `get_stopwords`.
- Now , we have everything to remove stopwords from the article_text.Thus, this is performed by `clean_article_text` function.This function cleans all the 112 articles text from the stopwords provided to us.
- In the last lines of program, we called all the above functions to actually implement stopwords Removal from all the articles texts.

                  **----------------------- Removal of StopWords Ends Here --------------------------**


2.2. **Text Analysis**

- Program for Text Analysis is written in file `Text_Analysis`.
- Go to file `Text Analysis.docx`, this file contain all the steps to be followed to do text analysis on a text.
- created a pandas dataframe for file `data/Output Data Structure.xlsx - Sheet1.csv` named `df`.
- Now , we need to calculate variables provided in `Text Analysis.docx` and fill these values in columns of `df`.
- Thats why i created a function named `add_df_col_values` , this function takes the name of column to be filled and name of the function that is going to fill this column.
- Now, look every other function (other than `add_df_col_values`) is for calculating a certain variable, and the variable it is calculating is suggested in the name of the function itself.
- At last we called these functions on all the articles iteratively and after filling the `df` , I updated this `data/Output Data Structure.xlsx - Sheet1.csv`.

                **----------------------- Text Analysis Ends Here --------------------------**

**The End✌️🥷**
