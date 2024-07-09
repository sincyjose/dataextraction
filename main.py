import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize, sent_tokenize
import string
import nltk
import re


nltk.download('punkt')

# Function to extract article text from a URL
def extract_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ' '.join([para.get_text() for para in paragraphs])
    return text

# Load the URLs and their corresponding URL_IDs
output_structure_path = "C:\\Users\\Sincy\\OneDrive\\Desktop\\Blackcopper.py\\Output Data Structure.xlsx"
output_structure_df = pd.read_excel(output_structure_path)

data_dir = "C:\\Users\\Sincy\\Downloads\\Data Extraction\\extracted_articles"
os.makedirs(data_dir, exist_ok=True)

# Extract and save articles
for _, row in output_structure_df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    article_text = extract_article_text(url)
    with open(os.path.join(data_dir, f"{url_id}.txt"), 'w', encoding='utf-8') as file:
        file.write(article_text)

# Load stop words
stop_words_dir = "C:\\Users\\Sincy\\Downloads\\Data Extraction\\StopWords"
stop_words = set()
for file_name in os.listdir(stop_words_dir):
    try:
        with open(os.path.join(stop_words_dir, file_name), 'r', encoding='latin1') as file:
            stop_words.update(file.read().splitlines())
    except UnicodeDecodeError:
        print(f"Could not decode {file_name}, skipping.")

# Load master dictionary
master_dict_path = "C:\\Users\\Sincy\\Downloads\\Data Extraction\\MasterDictionary"
positive_words = set()
negative_words = set()

try:
    with open(os.path.join(master_dict_path, 'positive-words.txt'), 'r', encoding='latin1') as file:
        positive_words.update([word for word in file.read().splitlines() if word not in stop_words])
except UnicodeDecodeError:
    print("Could not decode positive-words.txt, skipping.")

try:
    with open(os.path.join(master_dict_path, 'negative-words.txt'), 'r', encoding='latin1') as file:
        negative_words.update([word for word in file.read().splitlines() if word not in stop_words])
except UnicodeDecodeError:
    print("Could not decode negative-words.txt, skipping.")

# Function to calculate the required scores
def calculate_scores(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word not in string.punctuation and word not in stop_words]
    
    positive_score = sum(1 for word in tokens if word in positive_words)
    negative_score = sum(1 for word in tokens if word in negative_words)
    
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(tokens) + 0.000001)
    
    # Round the scores to 4 decimal places
    positive_score = round(positive_score, 4)
    negative_score = round(negative_score, 4)
    polarity_score = round(polarity_score, 4)
    subjectivity_score = round(subjectivity_score, 4)
    
    return positive_score, negative_score, polarity_score, subjectivity_score

# Function to calculate readability scores
def calculate_readability(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    
    num_sentences = len(sentences)
    num_words = len(words)
    
    # Define complex words as words with more than two syllables
    complex_words = [word for word in words if sum([1 for c in word if c in 'aeiou']) > 2]
    num_complex_words = len(complex_words)
    
    avg_sentence_length = num_words / num_sentences if num_sentences else 0
    percent_complex_words = num_complex_words / num_words if num_words else 0
    
    fog_index = 0.4 * (avg_sentence_length + percent_complex_words)
    
    # Round the scores to 4 decimal places
    avg_sentence_length = round(avg_sentence_length, 4)
    percent_complex_words = round(percent_complex_words, 4)
    fog_index = round(fog_index, 4)
    
    return avg_sentence_length, percent_complex_words, fog_index

# Function to calculate additional metrics
def calculate_additional_metrics(text):
    words = word_tokenize(text)
    clean_words = [word for word in words if word not in string.punctuation and word not in stop_words]
    
    # Average Number of Words Per Sentence
    sentences = sent_tokenize(text)
    avg_words_per_sentence = len(clean_words) / len(sentences) if sentences else 0
    
    # Complex Word Count
    complex_words = [word for word in clean_words if sum([1 for c in word if c in 'aeiou']) > 2]
    complex_word_count = len(complex_words)
    
    # Word Count
    word_count = len(clean_words)
    
    # Syllable Count Per Word
    def count_syllables(word):
        word = word.lower()
        count = 0
        vowels = "aeiou"
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith("es") or word.endswith("ed"):
            count -= 1
        if count == 0:
            count += 1
        return count
    
    syllable_count_per_word = {word: count_syllables(word) for word in clean_words}
    syllable_per_word_avg = sum(syllable_count_per_word.values()) / len(syllable_count_per_word) if syllable_count_per_word else 0
    
    # Personal Pronouns
    personal_pronouns = re.findall(r'\b(I|we|my|ours|us)\b', text, re.I)
    personal_pronoun_count = len(personal_pronouns)
    
    # Average Word Length
    avg_word_length = sum(len(word) for word in clean_words) / len(clean_words) if clean_words else 0
    
    # Round the metrics to 4 decimal places
    avg_words_per_sentence = round(avg_words_per_sentence, 4)
    complex_word_count = round(complex_word_count, 4)
    word_count = round(word_count, 4)
    syllable_per_word_avg = round(syllable_per_word_avg, 4)
    personal_pronoun_count = round(personal_pronoun_count, 4)
    avg_word_length = round(avg_word_length, 4)
    
    return avg_words_per_sentence, complex_word_count, word_count, syllable_per_word_avg, personal_pronoun_count, avg_word_length

# Initialize an empty list to hold the data
data = []

# Loop over each file in the directory and calculate scores
for filename in os.listdir(data_dir):
    if filename.endswith(".txt"):
        with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as file:
            text = file.read()
            url_id = filename.split('.')[0] 
            url = output_structure_df[output_structure_df['URL_ID'] == url_id]['URL'].values[0]
            
            # Calculate sentiment scores
            positive_score, negative_score, polarity_score, subjectivity_score = calculate_scores(text)
            
            # Calculate readability scores
            avg_sentence_length, percent_complex_words, fog_index = calculate_readability(text)
            
            # Calculate additional metrics
            (avg_words_per_sentence, complex_word_count, word_count, syllable_per_word_avg, 
             personal_pronoun_count, avg_word_length) = calculate_additional_metrics(text)
            
            data.append([
                url_id, url, positive_score, negative_score, polarity_score, subjectivity_score,
                avg_sentence_length, percent_complex_words, fog_index, avg_words_per_sentence,
                complex_word_count, word_count, syllable_per_word_avg, personal_pronoun_count,
                avg_word_length
            ])

# Create a DataFrame with the collected data
columns = [
    'URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE',
    'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX',
    'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT', 'SYLLABLE PER WORD',
    'PERSONAL PRONOUNS', 'AVG WORD LENGTH'
]
output_df = pd.DataFrame(data, columns=columns)


final_output_df = output_structure_df[['URL_ID', 'URL']].merge(output_df, on=['URL_ID', 'URL'])


final_output_path = "C:\\Users\\Sincy\\OneDrive\\Desktop\\Blackcopper.py\\Output Data Structure.xlsx"
final_output_df.to_excel(final_output_path, index=False)

print(f"Analysis complete. Output saved to {final_output_path}")
