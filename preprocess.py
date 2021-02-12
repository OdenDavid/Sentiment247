# for text manipulation
import nltk
import string
import re

# importing different libraries for text processing
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize 
from nltk.tag import pos_tag

def CleanMessage(message):
    
    # Removing usernames
    message = re.sub(r'\w*@\w*', '', message)

    # Removing URLs
    message = re.sub(r'(https?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*', '', message, flags=re.MULTILINE)
    
    stop_words = stopwords.words('english')
    tokens = word_tokenize(message)
    
    cleaned_tokens = []
    
    for token, tag in pos_tag(tokens):
        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
            
        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)
        
        if token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token)

    return cleaned_tokens
