import csv
import nltk
from textblob import TextBlob


# TextBlob approach
with open('gsa_sorns.csv') as sorn_csv:
  with open('noun_extracting/TextBlob.csv', 'w') as output:
    reader = csv.DictReader(sorn_csv)
    writer = csv.writer(output)
    for row in reader:
      blob = TextBlob(row['PII'])
      system_name_and_noun_phrases = [row['System Name']] + blob.noun_phrases
      writer.writerow(system_name_and_noun_phrases)


# Simple nlp noun checker
is_noun = lambda pos: pos[:2] == 'NN'
with open('gsa_sorns.csv') as sorn_csv:
  with open('noun_extracting/simple_nlp_nouns.csv', 'w') as output:
    reader = csv.DictReader(sorn_csv)
    writer = csv.writer(output)
    for row in reader:
      tokenized = nltk.word_tokenize(row['PII'])
      nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
      system_name_and_nouns = [row['System Name']] + nouns
      writer.writerow(system_name_and_nouns)


# More complicated nlp phrase checker 
grammar = "NP: {<JJ>*<NN>+<JJ>*<NN>*}"
cp = nltk.RegexpParser(grammar)
with open('gsa_sorns.csv') as sorn_csv:
  with open('noun_extracting/complicated_nlp_phrases.csv', 'w') as output:
    reader = csv.DictReader(sorn_csv)
    writer = csv.writer(output)
    for row in reader:
      sentences = nltk.sent_tokenize(row['PII'])
      sentences = [nltk.word_tokenize(sent) for sent in sentences]
      sentences = [nltk.pos_tag(sent) for sent in sentences]
      phrases = []
      for sentence in sentences:
        result = cp.parse(sentence)
        for chunk in result:
          try:
            phrase = [word for (word, tag) in chunk.leaves()]
            phrase = " ".join(phrase)
            phrases.append(phrase)
          except:
            pass
      system_name_and_phrases = [row['System Name']] + phrases
      writer.writerow(system_name_and_phrases)


    
