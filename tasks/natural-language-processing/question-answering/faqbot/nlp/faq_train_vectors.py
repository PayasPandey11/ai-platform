from faqnlu.settings import spacy_nlp as nlp
import pickle
import os


def train_faq(questions,user_id):
    """
    Create dataset in required format and sends it to get vector matrix

    :param questions: question with alias and labels
    :param user_id: unique indentifier
    :return:status
    """
    print(questions)
    all_questions = list()
    uid_list = list()
    try:
        for idx, question in enumerate(questions):
            if len(question["question"]) > 1:
                all_questions.append(question["question"])
                uid_list.append(question["_id"])
            for alias in question["aliases"]:
                print(alias)
                if len(alias) > 1:
                    all_questions.append(alias)
                    uid_list.append(question["_id"])

        print(all_questions, uid_list)
        # Get vector matrix
        X_train_vector = list(map(sentence_to_vector, all_questions))
        # Save model to disk


    except ValueError:
        print("VAlue error")
        status = False
    status = persist_faq(user_id, X_train_vector, uid_list)

    return status


def persist_faq(user_id,X_train_vector,uid_list):
    """

    :param user_id: unique indentifier for model file
    :param X_train_vector: Vector Matrix
    :param uid_list: labels list associated with question
    :return: status
    """

    try:
        user_modelfile_location = "trained_models/faq/" + str(user_id)
        matrix_file = user_modelfile_location + "/matrix.p"
        uid_file = user_modelfile_location + "/uid_list.p"

        if not os.path.exists(user_modelfile_location):
            os.makedirs(user_modelfile_location)

        pickle.dump(uid_list, open(uid_file, "wb"))
        pickle.dump(X_train_vector, open(matrix_file, "wb"))
        status = True
    except NotADirectoryError:
        print("not a directory")
        status = False

    return status


def sentence_to_vector(sentence):
    doc = nlp(sentence)
    return doc.vector
