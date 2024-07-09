# dataextraction
it perform text extraction, processing, and  analysis on article fetched from provided URLS.It calculates various sentiment, readability, and text complexity metrics, and saves the results to an Excel file. The workflow involves web scraping, text tokenization, and statistical analysis to derive meaningful insights from the content.

Prerequisites

pip install pandas requests beautifulsoup4 nltk
nltk.download('punkt')

Extracting Text from Articles
Read Excel File:
Use pandas to read the Excel file into a DataFrame named output_structure_df.

Extract Text from URL:

Loop through each URL in the DataFrame.
Use requests to perform an HTTP GET request for each URL.
Parse the HTML content using BeautifulSoup.
Extract text from all <p> tags and combine them into a single string.
Save the extracted text as a .txt file named after the url_id

Loading Stopwords and Master Dictionary

Initialize empty sets for stop words, positive words, and negative words.
Read the stop words file and update the stop words set.
Read the positive words file and update the positive words set.
Read the negative words file and update the negative words set.

 Calculating Sentiment Scores
 
Tokenize the text into words (lowercase).
Calculate positive_score by counting tokens in the positive words set.
Calculate negative_score by counting tokens in the negative words set.

Calculate Polarity Score:
                      Polarity Score = positive_score−negative_score/(positive_score+negative_score)+0.000001
​
Calculate Subjectivity Score:
                     Subjectivity Score =positive_score+negative_score/(number of tokens)+0.000001
                     
Calculate avg_sentence_length:
                     avg_sentence_length=num_words/num_sentences
​
Calculate percent_complex_words:
                            percent_complex_words=number of complex words/num_words

Calculate fog_index:
                  fog_index=0.4×(avg_sentence_length+percent_complex_words)
                 
Writing Output to Excel File
Loop through each .txt file in the data_dir.
If the url_id matches an entry in output_structure_df, calculate all metrics and append the data to a list.
Create columns for url_id, url, positive_score, negative_score, polarity_score, subjectivity_score, avg_sentence_length, percent_complex_words, fog_index, avg_words_per_sentence, complex_word_count, word_count, syllable_per_word_avg, personal_pronoun_count, and avg_word_length.
Save the results to output_structure.xlsx using pandas DataFrame.













     






















