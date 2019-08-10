**FAQ Bot - Turn your FAQ into automatic responces**

This is a plug and play Django project which uses sentence similarity to create automate response for frequently asked 
questions. 

This project currently supports two algorithms  
Tfidf and Word vectors(Contact developer for a project with 6 algorithms including neural networks)

Steps to run project -
 
    1. If running for the first time
      a. Go to project directory 
      b. In terminal type "python run.py"
    
    2. If already installed
      a. Go to project directory 
      b. In terminal type "python manage.py runserver"


Payload to Train FAQ -
    
    Type:Post
    Url: http://127.0.0.1:8000/nlpapi/faq/train
    Payload : {
	"qArray":[
	{
	    "question": "hi",
	    "aliases": ["hey", "hi", "hello"],
	    "answers":["Hello,what can i do for you","Hey whats up"],
	    "_id":"1"}, 
	{
        "question": "bye",
        "aliases": ["bye", "baaye", "goodbye"],
        "answers":["it was nice talking to you","see you soon"],
        "_id":"2"
    }],
        "workspace_id":"1",
        "model_type":"vector"/"tfidf"
    }
    

Payload to Test FAQ -

    Type:Post
    Url: http://127.0.0.1:8000/nlpapi/faq/ask
    Payload: {"query":"bye","workspace_id":"1"}
    


*--------Note---------*

  This is a demo project, ideally the project would use node.js/mongodb/redis to handle request/save data/create response.
  Sine this is a demo, the project saves data locally and exposes main nlp layer. This is not recommended.
  
*--------Note----------*


**Developer: Payas Pandey** 

**Email Id : rpayaspandey@gmail.com**

