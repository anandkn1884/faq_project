# faq_project
Match the FAQ based on user input and return appropriate answers based on the FAQs found on websites.
Currently using the FAQs found on https://www.vitality.co.uk/rewards/partners/

Compare the input question with the list of FAQs using Cosine similarity


Compare the input question with the list of FAQs in faq.csv
Return a list of answers sorted based on the score
Currently score is computer as

if question does not contain context words, 
    _score = cosine_score_

if question contains context words, 
    _score = cosine_score + 1_

Return 10 answers based on the score