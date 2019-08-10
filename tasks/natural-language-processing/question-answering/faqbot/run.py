import os
import spacy

os.system("pip install -r requirements.txt")
spacy.cli.download("en_core_web_sm")
os.system("python manage.py runserver")