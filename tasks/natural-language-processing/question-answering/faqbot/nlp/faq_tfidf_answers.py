from sklearn.metrics.pairwise import cosine_similarity
from .faq_utils import word_pos
import numpy as np
import pickle
import json
from nlp.faq_utils import JsonEncoder


def get_answers_tfidf(query,user_id):
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


def sentence_sim(query, user_id):
    user_modelfile_location = "trained_models/faq/" + user_id
    vect_file = user_modelfile_location + "/vect.p"
    matrix_file = user_modelfile_location + "/matrix.p"
    uid_file = user_modelfile_location + "/uid_list.p"

    tfmatrix = open(matrix_file, 'rb')
    tfidf_matrix = pickle.load(tfmatrix)

    tffile = open(vect_file, 'rb')
    tfvector = pickle.load(tffile)

    uid_list = open(uid_file, 'rb')
    labels = pickle.load(uid_list)
    query = word_pos([query])
    query = ' '.join(query)

    tfidf_sentence = tfvector.transform([query])

    # get similarity
    dist_vector = cosine_similarity(tfidf_sentence, tfidf_matrix)
    print(dist_vector,tfidf_sentence,tfidf_matrix)

    confidence_score_vectors = sorted(dist_vector[0])[-1] * 100
    closest_vectors = np.argsort(
        dist_vector)  # sort by closest index, in accending order(last element will be the closest one)
    closest_idx_vectors = closest_vectors[0][-1]  # get index of closest sentence
    print("\n Vectors Detected question id ---->", closest_idx_vectors)
    print("\n Vectors Confidence score----->", confidence_score_vectors)
    print(labels[closest_idx_vectors])

    return labels,dist_vector


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

