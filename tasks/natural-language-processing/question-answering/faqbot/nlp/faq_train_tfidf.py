import os
from sklearn.feature_extraction.text import TfidfVectorizer
import string
from .faq_utils import stemming_tokenizer,lemmatizer_tokenizer,word_pos


def train_tfidf(questions,user_id):
    try:
        all_questions = list()
        uid_list = list()
        for idx, question in enumerate(questions):
            if len(question["question"])>1:
                all_questions.append(question["question"])
                uid_list.append(question["_id"])
            for alias in question["aliases"]:
                if len(alias) > 1:
                    all_questions.append(alias)
                    uid_list.append(question["_id"])

        X = word_pos(all_questions)
        tfidf_vectorizer = TfidfVectorizer(tokenizer=stemming_tokenizer, lowercase=True,
                                           stop_words=list(string.punctuation))
        tfidf_matrix = tfidf_vectorizer.fit_transform(X)

        response = persist_faq(tfidf_vectorizer,tfidf_matrix,uid_list,user_id)
        return response

    except ValueError:

        print("VAlueerror")
        status = False

    return status


def persist_faq(tfidf_vectorizer,tfidf_matrix,uid_list,user_id):
    import pickle
    try:
        user_modelfile_location = "trained_models/faq/" + user_id
        vect_file = user_modelfile_location + "/vect.p"
        matrix_file = user_modelfile_location + "/matrix.p"
        uid_file = user_modelfile_location + "/uid_list.p"

        if not os.path.exists(user_modelfile_location):
            os.makedirs(user_modelfile_location)

        pickle.dump(uid_list, open(uid_file, "wb"))
        pickle.dump(tfidf_vectorizer, open(vect_file, "wb"))
        pickle.dump(tfidf_matrix, open(matrix_file, "wb"))
        status =  True
    except NotADirectoryError:
        print("not a directory")
        status = False

    return status
