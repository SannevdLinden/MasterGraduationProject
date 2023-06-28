## Data analysis

db_connection is the main python file from which the other python files are called. 

The MIMIC-III data set was used:
Johnson, A., Pollard, T., & Mark, R. (2016). MIMIC-III Clinical Database (version 1.4). PhysioNet. https://doi.org/10.13026/C2XW26.
In order to run the python files to get the intended output you need to obtain your own license for MIMIC-III. The data set was saved in a local PostgreSQL database and queried using SQL (psycopg2 library). 

Moreover, the UMLS metathesaurus (ICD-10, CUI codes and TUI codes) was used, in the step4_topic_saliences.py file. In order to run line 14-33 you need to obtain your own UMLS license at https://www.nlm.nih.gov/research/umls/index.html. You need to save your UMLS API key in an authentification.txt file. Also, the instructions of the PyMedTermino2 library (https://owlready2.readthedocs.io/en/latest/pymedtermino2.html) need to be followed to be able to run line 14-26. This takes some time.

On line 112 in the db_connection.py file you see the comment that Medtagger and scispacy needs to be run. Running Medtagger can be done by following the instructions of Processing multiple files via this link: http://ec2-184-73-168-219.compute-1.amazonaws.com/index.php/MedTagger_User_Guide. Running scispacy was done by using this tutorial of Wuraola Oyewusi and then running in[9]: display_entities(en_ner_bc5cdr_md,test_doc) with the input as prepared on line 103-111 of the db_connection.py file and saving this output in a json file. See: https://github.com/WuraolaOyewusi/How-to-use-ScispaCy-for-Biomedical-Named-Entity-Recognition-Abbreviation-Resolution-and-link-UMLS/blob/master/Explore_ScispaCy.ipynb 
