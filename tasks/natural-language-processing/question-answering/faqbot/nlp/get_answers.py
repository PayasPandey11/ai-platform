from nlp.faq_tfidf_answers import  get_answers_tfidf
from nlp.faq_vector_answer import get_answer_vectors
import random

import json

def faq_answer(query, user_id,model_type):
    print("Model type",model_type)
    if model_type == "vector":
        response, status = get_answer_vectors(query, user_id)
    elif model_type == "tfidf":
        response, status = get_answers_tfidf(query, user_id)

    else:
        response = "Wrong training type",
        status = 500

    if status == 200:
        response = make_response(response,user_id)

    return response, status


def make_response(answer_ids,user_id):

    file_location = "trained_models/faq/" + user_id + "/questions_file.txt"

    with open(file_location, 'r') as filehandle:
        filecontents = json.load(filehandle)

    answer_id = answer_ids["confidences"][0]["label"]
    confidence = answer_ids["confidences"][0]["confidence"]
    answer_query = next(item for item in filecontents if item["_id"] == str(answer_id))
    answer = random.choice(answer_query["answers"])

    print(answer,answer_ids)

    response = {
        "answer":answer,
        "confidence" : confidence
    }
    return response


