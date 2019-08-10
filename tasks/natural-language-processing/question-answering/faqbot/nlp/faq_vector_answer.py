from faqnlu.settings import spacy_nlp as nlp

import pickle
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
from nlp.faq_utils import  JsonEncoder




def get_answer_vectors(query,user_id):
    try:
        label, dist = sentence_sim(query, user_id)
        status = 200

    except FileNotFoundError as e:
        print("Error---", e)
        status = 500
        response = dict(success=False, message="Model not present for the user,please train a FAQ model first")
        return response, status

    try:
       response = get_answer_index(label, dist)
       status = 200

    except ValueError:
        response = dict(success=False, message="Some Error in getting answer please try again")
        status = 500

    return response,status


def sentence_sim(sentence, user_id):
    user_modelfile_location = "trained_models/faq/" + user_id
    matrix_file = user_modelfile_location + "/matrix.p"
    label_file_location = user_modelfile_location + "/uid_list.p"

    vcmatrix = open(matrix_file, 'rb')
    vector_matrix = pickle.load(vcmatrix)

    label_file = open(label_file_location, 'rb')
    labels = pickle.load(label_file)

    doc = nlp(sentence)
    dist_vectors = cosine_similarity(doc.vector.reshape(1, 96), vector_matrix)
    confidence_score_vectors = sorted(dist_vectors[0])[-1] * 100
    closest_vectors = np.argsort(
        dist_vectors)  # sort by closest index, in accending order(last element will be the closest one)
    closest_idx_vectors = closest_vectors[0][-1]  # get index of closest sentence
    print("\n Vectors Detected question id ---->", closest_idx_vectors)
    print("\n Vectors Confidence score----->", confidence_score_vectors)
    print(labels[closest_idx_vectors])

    return labels,dist_vectors


def get_answer_index(label, dist):

    sorted_dist = list(reversed(sorted(dist[0])))

    closest = np.argsort(dist)  # sort by closest index, in accending order(last element will be the closest one)
    closest_idx = closest[0][-1]  # get index of closest sentence
    closest_idx = label[closest_idx]

    labelIndex = list(reversed(closest[0]))
    labelIndex = [int(x) for x in labelIndex]


    confidences = list()
    for idx, _dist in enumerate(sorted_dist):
        _confidence = dict()
        _confidence["confidence"] = _dist
        _confidence["label"] = label[labelIndex[idx]]
        confidences.append(_confidence)

    if len(confidences) > 10:
        confidences = confidences[:10]

    response = {
        "confidences": json.loads(json.dumps(confidences, cls=JsonEncoder)),
        "success": True
    }
    return response


def sentence_to_vector(sentence):
    doc = nlp(sentence)
    return doc.vector


