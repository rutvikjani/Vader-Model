import nltk
import os
from nltk.corpus import stopwords
import nltk.corpus
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import pandas as pd
import csv
import re

stpwrd = nltk.corpus.stopwords.words('english')


nltk.download('stopwords')

directory = r'D:\python\scrapy\articlescraper\extracted data/'
files = os.listdir(directory)

text_data = []
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

directory = r'D:\python\scrapy\articlescraper\extracted data/'
file_list = os.listdir(directory)
sorted_file_list = sorted(file_list, key=natural_sort_key)

def readingData():
    for filename in sorted_file_list:
        file_path = os.path.join(directory, filename)

        print(file_path)
        extracting_filename = os.path.splitext(os.path.basename(file_path))[0]
        with open(file_path, "r", encoding='utf-8') as my_file:
            text = my_file.read().lower()
            tokenization = word_tokenize(text)
            text_data.extend(tokenization)

        f1 = open(r"D:\python\scrapy\articlescraper\words dictionary\StopWords_Auditor.txt","r")
        auditor_words = f1.read().lower()
        custom_tokenization = word_tokenize(auditor_words)
        extended_stpwrds = stpwrd.extend(custom_tokenization)

        #adding currency stopwords in main stopword file
        f2 = open(r"D:\python\scrapy\articlescraper\words dictionary\StopWords_Currencies.txt","r")
        currency_words = f2.read().lower()
        custom_tokenization = word_tokenize(currency_words)
        extended_stpwrds = stpwrd.extend(custom_tokenization)

        #extending stopwords with date time words
        f3 = open(r"D:\python\scrapy\articlescraper\words dictionary\StopWords_DatesandNumbers.txt","r")
        date_words = f3.read().lower()
        custom_tokenization = word_tokenize(date_words)
        extended_stpwrds = stpwrd.extend(custom_tokenization)

        #extending stopwords with generic words
        f4 = open(r"D:\python\scrapy\articlescraper\words dictionary\StopWords_Generic.txt","r")
        generics_words = f4.read().lower()
        custom_tokenization = word_tokenize(generics_words)
        extended_stpwrds = stpwrd.extend(custom_tokenization)

        #extending stopwords with generic long words
        f5 = open(r"D:\python\scrapy\articlescraper\words dictionary\StopWords_GenericLong.txt","r")
        genericLong_words = f5.read().lower()
        custom_tokenization = word_tokenize(genericLong_words)
        extended_stpwrds = stpwrd.extend(custom_tokenization)

        #extending stopwords with geographic words
        f6 = open(r"D:\python\scrapy\articlescraper\words dictionary\StopWords_Geographic.txt","r")
        geographic_words = f6.read().lower()
        custom_tokenization = word_tokenize(geographic_words)
        extended_stpwrds = stpwrd.extend(custom_tokenization)

        #extending stopwords with name words
        f7 = open(r"D:\python\scrapy\articlescraper\words dictionary\StopWords_Names.txt","r")
        name_words = f7.read().lower()
        custom_tokenization = word_tokenize(name_words)
        extended_stpwrds = stpwrd.extend(custom_tokenization)

        without_stopword = []
        filtered_words = []

        for words in text_data:
            if not words in stpwrd:
                without_stopword.append(words)
                if words.isalpha():
                    filtered_words.append(words)

        p_words = []
        file = open(r"D:\python\scrapy\articlescraper\words dictionary\positive-words.txt", "r", encoding='utf-8')
        positive_words = file.read().lower()
        positiveWordTokenization = word_tokenize(positive_words)

        for words in filtered_words:
            if words in positiveWordTokenization:
                p_words.append(words)

        n_words = []
        file = open(r"D:\python\scrapy\articlescraper\words dictionary\negative-words.txt", "r")
        negative_words = file.read().lower()
        tokenization = word_tokenize(negative_words)

        for words in filtered_words:
            if words in tokenization:
                n_words.append(words)

        polarity_score =  abs((len(p_words) - len(n_words)) / ((len(p_words) + len(n_words)) + 0.000001))

        subjectivity_score = (len(p_words) + len(n_words)) / (len(filtered_words) + 0.000001)

        with open(file_path, "r", encoding='utf-8') as data:
            text = data.read().lower()
            sentences = nltk.sent_tokenize(text)
            total_words = nltk.word_tokenize(text)
            sentence_length = ((len(total_words)) / (len(sentences)))

        two_syllable_word = []
        complex_words = []

        for myword in filtered_words:
            d = {}.fromkeys('aeiou',0)
            haslotsvowels = False
            for x in myword.lower():
                if x in d:
                    d[x] += 1
            for q in d.values():
                if q > 2:
                    haslotsvowels = True
                    complex_words.append(myword)
                    two_syllable_word.append(myword)
            if haslotsvowels:
                complex_words.append(myword)

        avg_complex_words = (len(complex_words) / len(filtered_words))

        fog_index = 0.4 * (sentence_length + avg_complex_words )

        avg_word = (len(filtered_words) / len(sentences))
        
        syllables = 0
        for word in filtered_words:
            vowels = "aeiou"
            if not ( word.endswith("ed") or word.endswith("ing") or word.endswith("es")):
                for chr in word:
                    if chr in vowels:
                        syllables += 1

        syllable_count = (len(filtered_words) / syllables)
        
        pronounce_words = ["I", "we", "my","ours","us", "our", "you", "they", "that", "these", "those"]
        personal_pronounce_words = 0
        for word in text_data:
            if word in pronounce_words:
                personal_pronounce_words += 1


        word_count = 0
        for word in filtered_words:
            for chr in word:
                word_count += 1

        avg_word_length = (word_count / len(filtered_words))

        csv_1 = pd.read_csv(r"D:\python\scrapy\articlescraper\data.csv", encoding='utf-8')
        sorted_df = csv_1.sort_values(by="URL_ID")
        sorted_df.to_excel('Sorted Data Structure.xlsx', index=False)

        data = [[extracting_filename, len(p_words), len(n_words), polarity_score, subjectivity_score, sentence_length, avg_complex_words, fog_index, avg_word, len(complex_words), len(filtered_words), syllable_count, personal_pronounce_words, avg_word_length ]]

        with open("Output Data.csv", mode='a', newline='', encoding='utf-8') as my_file:
            writer = csv.writer(my_file)
            for row in data:
                writer.writerow(row)

        text_data.clear()
readingData()