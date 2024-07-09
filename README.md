# dataextraction
it perform text extraction, processing, and  analysis on article fetched from provided URLS.It calculates various sentiment, readability, and text complexity metrics, and saves the results to an Excel file. The workflow involves web scraping, text tokenization, and statistical analysis to derive meaningful insights from the content.

#Prerequisite
Install these libraries using pip:  
pip install pandas requests beautifulsoup4 nltk
nltk.download('punkt')

Description
Extract the text from the article
The pandas to read the Excel file into a DataFrame named output_structure_df..
The loop calls the function as text_article =  extract_article_text(url)  takes the urls and url_id from the excel file.
The HTTP GET requests the provided URL and stores the response.
The html content of the response is parsed by using beautifulsoup .  
Find the paragraph in the response using the (<p>) tags and combine into single string
Save the extracted text as url_ids as name of the txt files.

Loading the Stopwords and Master Dictionary
Stop words are common words that do not contribute to the sentiment of the text.
Eg: is,a,the,are etc…. By removing the stop words,we have filtered out less significant words and retained the words that are more likely to carry important information.
Master dictionary contain positive and negative words which contribute to the sentiment of the text.
Give the path of Stop words and Master dictionary and initialize an empty set to store the stop words,positive words and negative words.
Open and read each file and update the sets of stop words , positive words and negative words.

Function to Calculating Score
Define a function  calculate_scores(text) to take a text string as input and calculate various sentiment-related scores.
tokens = word_tokenize(text.lower()) - convert the text to lowercase and tokenize it into words.
positive_score: Counts the number of tokens that are in the positive_words set.
negative_score: Counts the number of tokens that are in the negative_words set.
Polarity Score: Measures the overall sentiment direction
Formula: (positive_score−negative_score)/((positive_score+negative_score)+0.000001)

               Positive values indicate a positive sentiment.
               Negative values indicate a negative sentiment.
               Values close to zero indicate a neutral sentiment
Subjectivity Score: Measures how subjective the text is, indicating the proportion of words that carry sentiment (either positive or negative).
   Formula: (positive_score+negative_score)/(number of tokens+0.000001)
               Values close to 1 indicate highly subjective text.
                Values close to 0 indicate more objective text.

Function to Calculating Readability Score
Define a function calculate_readability(text) to compute readability metrics for a given text, including the average sentence length, percentage of complex words, and the Gunning Fog Index. 
sentences = sent_tokenize(text) - split the text into sentences. Then find out the following
num_sentences: The total number of sentences in the text.
num_words: The total number of words in the text.
Complex Words: Defined as words with more than two syllables
avg_sentence_length: Average number of words per sentence.
Calculated as the total number of words divided by the total number of sentences.
percent_complex_words: Proportion of complex words to the total number of words.
Calculated as the total number of complex words divided by the total number of words.
fog_index: A readability test that estimates the years of formal education needed to understand the text on the first reading.
Formula: 0.4×(avg_sentence_length+percent_complex_words)
Round the values to 4 decimal points and return the value.

Function to Calculating Additional Metrics
Define a function calculate_additional_metric(text) to compute various readability and linguistic metrics from a given text. 
sentences = word_tokenize(text) - split the text into  words.
clean_words= remove the punctuation and stop words from the words.
Finding the average number of words per sentence by tokenizing the text into sentences and average calculation is done by the total number of cleaned words divided by the number of sentences.
Word_count = total number of cleaned words.
To find out syllable Count per word create a function  and start the count with zero and it increments count for vowels at the start of the word and for each vowel not preceded by another vowel.
Adjusts count for common word endings like "es" and "ed."
Average Syllables per Word: The total syllable count divided by the number of words.

 Write output to Excel file
Rounds each calculated metric to four decimal places and return the values.
Initialize an empty list to hold the data and started a loop to read the all files in the data_dir and if url_id in the output_structure_df  and url_id of txt files matches it calls the above mentioned functions and  append the data to the  empty list.
Create columns for url_id, url, positive_score, negative_score, polarity_score, subjectivity_score,                avg_sentence_length, percent_complex_words, fog_index, avg_words_per_sentence,   complex_word_count, word_count, syllable_per_word_avg, personal_pronoun_count,                avg_word_length.
Save the file to the output_structure.xlsx using pandas dataframe.



.











     






















