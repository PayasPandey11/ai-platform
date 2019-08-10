import json

from django.http import JsonResponse
from nlp.faq_train_vectors import train_faq
from nlp.faq_train_tfidf import train_tfidf
from nlp.get_answers import faq_answer
from nlp.faq_utils import save_questions


def train(request):
    ''' Trains the Spacy vectors and dumps the model files to disk in trained_models/userId

    Args:
        request,
        userId:the function takes userID from validate decorator present in woohoonlu/decorator.py
    Return:
        Jsonresponse "model trained"
    '''

    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')

            body = json.loads(body_unicode)
            questions = body["qArray"]
            user_id = body["workspace_id"]
            model_type = body["model_type"]

        except ValueError:
            response = {
                "success": False,
                "message": "Wrong Json format,Please check documentation for right api format"
            }

            return JsonResponse(response)
        if model_type == "vector":
            train_status = train_faq(questions,user_id)
        elif model_type == "tfidf":
            train_status = train_tfidf(questions, user_id)
        else:
            response = {
                "success": False,
                "message": "Unknown training type"
            }

            return JsonResponse(response)

        request.session['model_type'] = model_type
        question_save_status  = save_questions(questions,user_id)



        if train_status:
            response = {
                "success": True,
                "message": "Model trained!"
            }
        else:
            response = {
                "success": False,
                "message": "There was some error while training"
            }

        return JsonResponse(response)
    else:
        response = {
            "success": False,
            "message": "Wrong Request Type"
        }

        return JsonResponse(response)




def ask(request):
    '''Generates the response(the label associated) to any query

    Args:
        request,
        userId:the function takes userID from validate decorator present in woohoonlu/decorator.py
    Returns:
        Success true with label if confidence score is greater than Upper threshold,
        False with no label for other two condition
    '''

    import json
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        query = body["query"]
        print(query)

        user_id = body["workspace_id"]
        model_type = request.session.get('model_type', None)

        response,status = faq_answer(query, user_id,model_type)

        return JsonResponse(response,status=status,safe=False)

