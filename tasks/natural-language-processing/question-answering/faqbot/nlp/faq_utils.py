import json
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize



def stemming_tokenizer(text):

    """Convert text to their stemmed version
    example game,gaming,games,gamed get changed to "game"
    Used in train function as a parameter to tfidf vectorizer

    Args:
      text:list of sentences
    Returns:
      list of tokenized and stemmed sentences
    """

    stemmer = PorterStemmer()
    return [stemmer.stem(w) for w in word_tokenize(text)]


def lemmatizer_tokenizer(text):

    """Convert text to their lemmantized version
    example game,gaming,games,gamed get changed to "game"
    Can you used instead of "stemming_tokenizer" in train function as a parameter to tfidf vectorizer

    Args:
      text:list of sentences
    Returns:
      list of tokenized and lemmantized sentences
    """

    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(w) for w in word_tokenize(text)]


def word_pos(data):
    """Converts sentences into list of string with words represented as Word_POS (POS->part of speech)

    Args:
        data:list of sentences.example pandas series
    Returns:
        list of sentences where word is replaced with word_pos.
    """

    final = list()
    for question in data:
        pos_tags = nltk.pos_tag(word_tokenize(question))
        tags = list()
        for i in pos_tags:
            new_word = i[0] + '_' + i[1]
            tags.append(''.join(new_word))
        str1 = ' '.join(tags)
        final.append(str1)
    return final


def save_questions(questions,user_id):
    import pickle
    file_location = "trained_models/faq/" + user_id +"/questions_file.txt"
    try:
        with open(file_location, 'w') as f:
            json.dump(questions, f)
        status = True
    except FileNotFoundError:
        status = False
    return status


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(JsonEncoder, self).default(obj)