from owlready2 import *
from PyUMLS.pyumls import api
import codecs
import numpy as np
import pandas as pd
import json
from anytree import Node, RenderTree, search
from anytree.exporter import DotExporter
from doc_clustering import stem_token_stop
from sql_con import db_conn
from sklearn.feature_extraction.text import TfidfVectorizer

#needed for owlready setup
# from owlready2.pymedtermino2 import *
# from owlready2.pymedtermino2.umls import *

# def setupOwlready():
#     default_world.set_backend(filename = "pym.sqlite3")
#     import_umls("umls-2019AB-metathesaurus.zip", terminologies = ["ICD10", "CUI"])
#     default_world.save()

default_world.set_backend(filename = "pym.sqlite3")
PYM = get_ontology("http://PYM/").load()
UMLS = PYM["CUI"]
ICD10 = PYM["ICD10"]

# need a license for UMLS: https://www.nlm.nih.gov/databases/umls.html to get an API key
# open API key of UMLS 
apiUMLS = codecs.open('authentification.txt', 'r')
apiUMLS = apiUMLS.read()
apiUMLS = { 'apiUMLS' : apiUMLS.split(':')[1]}

#get CUI of a term from UMLS using owlready2/PyMedTermino2
def getCUI(term):    
    print("term:" + term)   
    CUI = UMLS.search(term) 
    if (CUI):
        print(CUI[0])
        return(CUI[0])
    else:
        print('concept not recognized')
        return False

#Get TUI of term using UMLS API from PyUMLS.pyumls
def getSemanticType(CUI):
    result = api.getByCUI(CUI, apikey = apiUMLS['apiUMLS'])
    return result['semanticTypes'][0]['name']

#make json file with array filled with [term, tags from medtagger or scispacy, CUI, TUI]
def concept_extraction(data, cluster, subject_id):
    #UMLS API does not like these characters
    for x in data:
        if(re.search('-|:|\/|\\|\.|,|\(|\)|;|\'|\*|\[|\]|%|&', x[0])): 
            x[0] = re.sub('-|:|\/|\\|\.|,|\(|\)|;|\'|\*|\[|\]|%|&', ' ', x[0])             
        
        CUI = getCUI(x[0]) 
        if (CUI != False):
            TUI = getSemanticType(CUI.name)
            x.append(CUI.name)
            x.append(TUI)
        else :
            print('Entity not recognized')
    
    data = filter(lambda x : len(x) > 2, data) #filter out all concepts that were not recognized 
    data = list(data)
    with open('./patient_data/' + cluster + '_' + subject_id +  ".json", 'w') as f:
        json.dump(data, f)

#make tree with terms based on ICD-10 codes of terms
#CUIset  all CUI from all terms, ICD10_bool if yes make tree based on ICD-10 codes
def makeTree(CUIset, ICD10_bool):
    #make a tree structure of all the CUI concepts and their ancestors 
    root = Node('root', leafCount = 0, occurence = 0, indexArray = None, idNode='root')
    for x in CUIset: 
        conceptSet = UMLS[x[2]] >> ICD10 #convert CUI to ICD10 to get hierarchical structure      
        ancestors = [concept.ancestor_concepts() for concept in conceptSet] #contains [[ICD10, ancestor1, ancestor2...]]        
        if(len(ancestors) > 0): #sometimes concepts not recognized 
            x.append(placeholder_name) #the ICD-10 names are not saved in the tree but some placeholder, suchs as 'A' and then its child is 'A.1'. 
            #You need to temporarily store which icd-10 concept translate to which placeholder to check if a leaf already exists or if paths partly overlap. 
            #But that is not included in this code and should be added by you. 
            leafExists = search.find_by_attr(root, placeholder_name) #search if leaf is new
            for index, ancestor in reversed(list(enumerate(ancestors[0]))): #first the highest ancestor to walk down path of this term
                name = placeholder_name #search for placeholder again 
                searchNode = search.find_by_attr(root, name) # search if current node already exists  
                if (searchNode): #node already exist
                    searchNode.occurence += 1
                    if (not leafExists): # if there is a new leaf then add leaf count
                        searchNode.leafCount += 1
                else: #new leaf
                    if (index == len(ancestors[0]) -1 ): #last element in array, child of root
                        parentNode = root                        
                        vars()[name] = Node(name, parent = parentNode, leafCount = 1, occurence = 1, indexArray = None, idNode=name)
                    else:
                        parentNode = ancestor_placeholder_name
                        if(index == 0): #if it is a leaf add the index in de original array
                            vars()[name] = Node(name, parent = vars()[parentNode], leafCount = 1, occurence = 1, indexArray = x[0], idNode=name)
                        else: 
                            vars()[name] = Node(name, parent = vars()[parentNode], leafCount = 1, occurence = 1, indexArray = None, idNode=name)
    return(root, CUIset)
    
#detect 5 most salient terms of the tree
def salience_tree(tree):
    result = [] #top 5 salient terms
    percentages = [] #percentages of the children of the root, based upon how many leaf each subtree with
    # a child of the root as parent has
    total_leaf = 0
    children_root = list(tree.children)
    print(children_root)
    # get total leaf count
    for node in children_root:
        total_leaf += node.leafCount
    if (total_leaf <= 5): #if there are only 5 leaves or less just take them all
        for leaf in tree.leaf:
            result.append(leaf.indexArray)
        return result
    else: 
        counter = 0
        # calculate percentages of children root
        for child in children_root:
            percentage = (child.leafCount * 100 ) / total_leaf
            percentages.append(percentage)
        print(percentages)
        while counter < 5: #as long as their have not been chosen 5 salient terms
            #child with highest percentage
            max_index = percentages.index(max(percentages)) 
            node = children_root[max_index]
            while not node.is_leaf:
                #traverse down the tree with the child of the root with the highest percentage as root
                #on every level pick child with highest leaf count
                children = np.array(node.children)
                #if multiple children have the same leaf count a random one will be chosen
                np.random.shuffle(children) 
                max_value = 0
                for child in children:
                    if child.leafCount > max_value:
                        node = child
                        max_value = child.leafCount            
            result.append(node.indexArray)
            #get all ancestors of chosen leaf
            ancestors = node.ancestors
            #decrease count so same leaf are not chosen again
            for ancestor in reversed(ancestors):
                if (ancestor != tree.root):
                    ancestor.leafCount -= 1 
            if len(ancestors) > 1: #decrease percentage of the child of the root's subtree
                ind = children_root.index(ancestors[1])
                percentages[ind] = percentages[ind] - 20
            else: # the node is a child of the root
                ind = children_root.index(node)
                percentages[ind] = percentages[ind] - 20
            counter += 1
            print(node)
            print(result)
        return result

# I wanted more control to test certain things with stemming, therefore, this is needed to override the TfidfVectorizer
def needed_tfidf(doc):
    return doc

#get synonyms of a CUI code
def get_synonyms(CUI):
    concept = UMLS[CUI]
    return concept.synonyms

#get the 5 most salient terms based upon salient detection, data are all the terms 
# and make_df is a bool if the reference frame needs to be made
def salience_TFIDF(data, make_df):
    categories = ['ECG', 'Echo', 'Nursing', 'Radiology', 'Discharge summary'] #all note categories
    result = []
    percentage = [40, 13.333333, -100, 46.6666666, -100] #percetages of notes in each category, nursing and discharge excluded
    if(make_df): #make a reference dataframe with tf-idf of all words occuring in 500,000 notes for each note category,
        #only need to do this once
        doc_collection = []
        doc_collection_tokens = []
        #for each category take 100,000 random notes from the MIMIC database
        for cat in categories:
            query = "SELECT category, text FROM mimiciii.noteevents \
            WHERE category = '"+ cat +"' ORDER BY RANDOM() LIMIT 100000"
            docs = db_conn(query)
            text = ''
            #add notes in one category together to form one doc
            for index, row in docs.iterrows():
                text += row['text']
            doc_collection.append(text)
        #stem, tokenize and remove stopwords from docs  
        for doc in doc_collection:
            doc = stem_token_stop(doc)
            doc_collection_tokens.append(doc)
        #vectorize sentences 
        vectorizer = TfidfVectorizer(
            analyzer = 'word',
            tokenizer = needed_tfidf,
            preprocessor = needed_tfidf,
            token_pattern = None)  
        #transform using TFIDF vectorizer
        vectors = vectorizer.fit_transform(doc_collection_tokens)
        feature_names = vectorizer.get_feature_names()
        dense = vectors.todense()
        denselist = dense.tolist()
        df_tfidf = pd.DataFrame(denselist, columns=feature_names)
        print('tf-idf Matrix:')
        print(df_tfidf)
        df_tfidf.to_csv(r'D:\Documents\Master\Graduation project\semester 2\code\patient_data\tfidf_notes.csv')
    else:
        #load reference frame
        df_tfidf = pd.read_csv(r'D:\Documents\Master\Graduation project\semester 2\code\patient_data\tfidf_notes.csv') 
        print('tf-idf Matrix:')
        print(df_tfidf)

    tmp = categories.insert(0, 'term')
    final_tfidf = pd.DataFrame(columns = tmp) #dataframe with all the term in data as rows and all categories as columns
    data = np.array(data)
    np.random.shuffle(data)
    # for all terms check how often they and their synonyms occur in different note types of reference frame
    for term in data:
        #get synonyms
        synonyms = list(get_synonyms(term[2]))
        synonyms.insert(0, term[0])
        for i in range(len(synonyms)):
            #stem, tokenize and remove stop words synonyms
            synonyms[i] = stem_token_stop(synonyms[i])      
        tfidf_val = [] # data to fill row belonging to one row in final_tfidf
        for synonym in synonyms: #all tokens of all synonyms and the original term 
            if len(tfidf_val) < 1: #fill row with 0's if empty
                for i in range(len(categories)-1): 
                    tfidf_val.append(0)        
            #for every word in synonyms get the tf_idf of each category for that word 
            # and add it to the current tf_idf values in tfidf_val
            #for multiple synonyms 
            if len(synonym) > 1:
                for word in synonym:                    
                    in_df = word in df_tfidf
                    if in_df:                    
                        for index, row in df_tfidf.iterrows():
                            tfidf_val[index] += row[word]
            else: #for one synonym 
                in_df = synonym[0] in df_tfidf           
                if in_df:
                    for index, row in df_tfidf.iterrows():
                            tfidf_val[index] += row[synonym[0]]
        dict_data = {'term' : term[0]}
        #for each category add the normalized tf_idf of that term to final_tfidf
        for i in range(len(categories) -1):
            dict_data[categories[i+1]] = (tfidf_val[i] / len(synonyms)) #normalize total tf_idf value
        final_tfidf = final_tfidf.append(dict_data, ignore_index=True)
    # pick the note category with highest percentage and then the term with highest tf-idf score 
    for i in range(5): 
        idx = percentage.index(max(percentage)) + 1 #due to inserting term
        col = categories[idx]
        col = final_tfidf[col]
        max_val_id = col.idxmax()
        result.append(final_tfidf['term'][max_val_id])
        final_tfidf.loc[max_val_id] = -100 #make sure term is not chosen again
        percentage[idx - 1] = percentage[idx - 1] - 20 #reduce percentage of that note category
    return result
    
    
#main function, data are all the terms and their category from medtagger and scispacy
# cluster is cluster name, conceptextraction is bool to check if concepts (CUI and TUI) still need to be extracted from UMLS
# subject_id is the patient id from MIMIC data set
def topic_saliences(data, cluster, conceptExtraction, subject_id):   
    if (conceptExtraction):
        concept_extraction(data, cluster, subject_id)
    else:
        with open('./patient_data/' + cluster + '_' + subject_id + ".json") as f:
            data = json.load(f)
            
        disease = []
        drugs = []
        procedure = []

        #semantic types (TUI) per word summary category 
        diseaseCat = {'Anatomical Abnormality', 'Congenital Abnormality', 'Acquired Abnormality',
                        'Hazardous or Poisonous Substance',  'Laboratory or Test Result', 
                        'Sign or Symptom', 'Disease or Syndrome', 'Mental or Behavioral Dysfunction'
                        'Neoplastic Process', 'Cell or Molecular Dysfunction', 'Injury or Poisoning'} #'Finding',
        drugsCat = {'Clinical Drug', 'Chemical', 'Pharmacologic Substance', 'Antibiotic', 
                        'Biologically Active Substance', 'Hormone', 'Enzyme', 'Vitamin', 
                        'Immunologic Factor', 'Receptor'}
        procedureCat = {'Laboratory Procedure', 'Diagnostic Procedure', 'Therapeutic or Preventive Procedure'}
 
        unique_cui = set()
        #check if the category from medtagger and scispacy overlaps with the categories defined above
        for x in data:
            if len(x) > 1:
                if (x[3] in diseaseCat and 'DISEASE' in x[1] and x[2] not in unique_cui):
                    disease.append(x)
                    unique_cui.add(x[2])
                elif(x[3] in drugsCat and ('DRUG' in x[1] or 'CHEMICAL' in x[1]) 
                    and x[2] not in unique_cui):
                    drugs.append(x)
                    unique_cui.add(x[2])
                elif(x[3] in procedureCat and 'PROC' in x[1] 
                    and x[2] not in unique_cui):
                    procedure.append(x)
                    unique_cui.add(x[2])
        
        #for the disease category make the tree and extract terms from tree
        if(len(disease) > 5):
            root, disease = makeTree(disease, True)
            # tree = RenderTree(root)
            # print(tree)        
            disease_words = salience_tree(root)
            # print(disease_words)
        else: 
            disease_words = []
            for word in disease:
                disease_words.append(word[0]) 

        #for drugs and procedure category use salience detection to get most salient terms
        if (len(drugs) > 5):
            drugs_words = salience_TFIDF(drugs, False) 
        else: 
            drugs_words = []
            for word in drugs:
                drugs_words.append(word[0])
        
        if (len(procedure) > 5):
            procedure_words = salience_TFIDF(procedure, False) 
        else: 
            procedure_words = []
            for word in procedure:
                procedure_words.append(word[0])
    
        return [disease_words, drugs_words, procedure_words]
    return []       
