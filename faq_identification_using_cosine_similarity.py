# Match the FAQ based on user input and return appropriate answers
# based on the FAQs found on websites.
# Currently using the FAQs found on https://www.vitality.co.uk/rewards/partners/
# Compare the input question with the list of FAQs using Cosine similarity

import re, math
import pandas as pd
import nltk
from collections import Counter

WORD = re.compile(r'\w+')

stopwords = nltk.corpus.stopwords.words('english')

# Method to remove Englist Stop words
def remove_stopwords(text1):
    new_text1 = ''
    tokens = nltk.word_tokenize(text1)
    for token in tokens:
        if token not in stopwords:
            new_text1 += token + ' '

    return new_text1

# Conpute Cosine similarity
def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

# Convert Text to vector
def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)

# For questions that do not contain any context(brand names, plans etc),
# identify the context by finding the providers name in the question.
def check_context(row, question):
    question = remove_stopwords(question)
    in_context = False

    # Currently just checking the presence of the whole text
    if (row[1] in question) or (row[2] in question):
        in_context = True

    return in_context

# Compare the input question with the list of FAQs in faq.csv
# Return a list of answers sorted based on the score
# Currently score is computer as
# if question does not contain context words, score = cosine_score
# if question contains context words, score = cosine_score + 1
# Return 10 answers based on the score
def get_answer(question, number_of_answers = 10):

    df = pd.read_csv("faqs.csv")
    score_dictionary = {}
    faq_array = []
    answer_list = []
    count = 0
    vector1 = text_to_vector(question)

    for index, row in df.iterrows():
        vector2 = text_to_vector(row[3])
        cosine_score = get_cosine(vector1, vector2)

        # Check providers and category for context
        if check_context(row, question):
            score_dictionary[index] = cosine_score + 1
        else:
            score_dictionary[index] = cosine_score

        faq_array.append(''.join(str(row[1]) + "\t" + str(row[2]) + "\t" + str(row[3]) + "\t" + str(row[4]) + "\t" + str(score_dictionary[index])))

    sorted_by_value = sorted(score_dictionary.items(), key=lambda k: k[1], reverse=True)

    for key, value in sorted_by_value:
        # print(faq_array[key])
        answer_list.append(faq_array[key])
        count += 1
        if count == number_of_answers:
            break

    return answer_list

if __name__ == "__main__":
    # Get text to find corresponding answer.
    question = 'Do I need a vitality plan to get the starbucks offer?'
    answer_list = get_answer(question)

    print("\n",question)
    for answer in answer_list:
        print(answer)