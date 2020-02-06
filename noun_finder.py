import csv
import nltk
from textblob import TextBlob


# with open('gsa_sorns.csv') as sorn_csv:
#   reader = csv.DictReader(sorn_csv)
#   for row in reader:
#     blob = TextBlob(row['PII'])
#     print(blob.noun_phrases)


# # function to test if something is a noun
# is_noun = lambda pos: pos[:2] == 'NN'
# # do the nlp stuff
# with open('gsa_sorns.csv') as sorn_csv:
#   reader = csv.DictReader(sorn_csv)
#   for row in reader:
#     tokenized = nltk.word_tokenize(row['PII'])
#     nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
#     print(nouns)



# grammar = "NP: {<JJ>*<NN>+<JJ>*<NN>*}"
# cp = nltk.RegexpParser(grammar)

# # do the nlp stuff
# with open('gsa_sorns.csv') as sorn_csv:
#   reader = csv.DictReader(sorn_csv)
#   for row in reader:
#     sentences = nltk.sent_tokenize(row['PII'])
#     sentences = [nltk.word_tokenize(sent) for sent in sentences]
#     sentences = [nltk.pos_tag(sent) for sent in sentences]
#     for sentence in sentences:
#       result = cp.parse(sentence)
#       for chunk in result:
#         try:
#           print(" ".join([word for (word, tag) in chunk.leaves()]))
#         except:
#           pass


    
