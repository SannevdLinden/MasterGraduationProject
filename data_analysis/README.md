## Data analysis

db_connection is the main python file from which the other python files are called. 

The MIMIC-III data set was used:
Johnson, A., Pollard, T., & Mark, R. (2016). MIMIC-III Clinical Database (version 1.4). PhysioNet. https://doi.org/10.13026/C2XW26.
In order to run the python files to get the intended output you need to obtain your own license for MIMIC-III. The data set was saved in a local PostgreSQL database and queried using SQL. 

On line 112 in the db_connection.py file you see the comment that Medtagger and scispacy needs to be run. Running Medtagger can be done by following the instructions of Processing multiple files via this link: http://ec2-184-73-168-219.compute-1.amazonaws.com/index.php/MedTagger_User_Guide. Running scispacy was done by using this tutorial of Wuraola Oyewusi and then running in[9]: display_entities(en_ner_bc5cdr_md,test_doc) with the input as prepared on line 103-111 of the db_connection.py file and saving this output in a json file. See: https://github.com/WuraolaOyewusi/How-to-use-ScispaCy-for-Biomedical-Named-Entity-Recognition-Abbreviation-Resolution-and-link-UMLS/blob/master/Explore_ScispaCy.ipynb 
