# -*- coding: utf-8 -*-
"""
Created on Fri May  1 09:32:15 2020

@author: s146523

Based upon the blog 'How to Create a Simple Frontend, API, and Model with Python + Vue.js' from James Salvatore retrieved 04-11-2020 from:
https://medium.com/uptake-tech/how-to-create-a-simple-frontend-api-and-model-with-python-vue-js-a51841c66f8a
"""

from owlready2 import *
import nltk
import os
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import numpy as np
#  set up only 
# from owlready2.pymedtermino2 import *
# from owlready2.pymedtermino2.umls import *

# only do this once
# def set_up():    
#     default_world.set_backend(filename = "pym.sqlite3")
#     import_umls("umls-2019AB-metathesaurus.zip", terminologies = ["ICD10", "CUI"])
#     default_world.save()

app = Flask(__name__)
CORS(app)
api = Api(app)

# Require a parser to parse our POST request.
parser = reqparse.RequestParser()
parser.add_argument("search")
first_run = True
UMLS = None

class Search(Resource):
    def post(self):
        args = parser.parse_args()        
        word = str(args['search']) 
        #split search terms, lower case them and stem them        
        tokens = word.split()
        stemmer = nltk.stem.porter.PorterStemmer()
        tokens = [word.lower() for word in tokens]
        tokens = [stemmer.stem(t) for t in tokens]
        word = ''
        #concatenate word again
        for token in tokens:
            word += (token + '* ') 
        #needed to make pym.sqlite backend work
        global first_run
        global UMLS
        if(first_run):
            default_world.set_backend(filename = "pym.sqlite3")
            PYM = get_ontology("http://PYM/").load()
            UMLS = PYM["CUI"]
            first_run = False
        #search for synonyms of the searched term
        search_word = UMLS.search(word)
        if (len(search_word) > 0):
            result = []
            for concept in search_word:
                result.append(concept.label.first())
        else:
            result = "no results"
# print(result)

        return {'search_result': result}
        

api.add_resource(Search, "/")

if __name__ == "__main__":
   app.run(debug=True)

    #initial set-up
    # set_up()
