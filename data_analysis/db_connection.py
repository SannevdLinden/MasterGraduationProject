# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 10:14:03 2020

@author: s146523
"""

import pandas as pd 
from doc_clustering_manual import clustering
from step4_topic_saliences import topic_saliences
from sql_con import db_conn
import codecs
import re
import numpy as np
import json

if __name__ == "__main__":
    subject_id = '' #patient id from mimic data set 
    #set them True one by one, and the others should be False
    first_run_this = True #make the input files for medtagger
    second_run_this = False #make concept extraction files
    finally_run_this = False # get word summaries and save data 
    #get data from local mimic data base
    query = "SELECT subject_id, hadm_id, chartdate, charttime, storetime, category, description, text FROM mimiciii.noteevents \
         WHERE subject_id =" + subject_id + " ORDER BY chartdate ASC, charttime ASC LIMIT 500;"
    data = db_conn(query)
   
    #step: remove redundancy
    #remove redundancy (optional), can be done in number of ways based on your preference.
    #for example split text up in sentences based on . (exclude it if it is used for number, e.g. 3.99)
    #based on levensthein distance or DTW check the similairty between string of different notes.
    # delete the sentences above a certain similarity threshold. Keep the oldest instance  
    #get if duplicated text is above 15% of all text otherwise do not mark redundancy
      
    #reset dates to 1980 and remove [** **] to make text more readable
    for index, row in data.iterrows():
        text = row['text']
        for date in re.finditer(r'\[\*\*\d\d\d\d-\d\d-\d\d\*\*\]', text):        
            year = int(text[date.start() + 3:date.end()-9]) -130
            text = text[:(date.start() + 3)] + str(year) + text[(date.end() - 9):]
        for date in re.finditer(r'\[\*\*\d\d\d\d-\d\d-\d\*\*\]', text):        
            year = int(text[date.start() + 3:date.end()-8]) -130
            text = text[:(date.start() + 3)] + str(year) + text[(date.end() - 8):]
        text = re.sub(r'\[\*\*', '', text)
        text = re.sub(r'\*\*\]', '', text)
        data.at[index, 'text'] = text
    print(data)

#######################################################################

    #step: document clustering
    #get information about admission for admission clusters
    query_clustering = "SELECT subject_id, hadm_id, admittime, dischtime, admission_type, admission_location, \
            discharge_location, diagnosis FROM mimiciii.admissions \
         WHERE subject_id = " + subject_id
    info_clustering = db_conn(query_clustering)
    data = clustering(info_clustering, data, len(info_clustering.index))
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    print(data['cluster'])
    
    # prepare input doc for next step, concatenate data of all notes belonging to same cluster
    clusters = []
    for cluster, group in data.groupby('cluster'):
        if(cluster != 'empty'):
            clusters.append(cluster) 
            if(first_run_this):
                f = open('./Medtagger_output/input/patient_'+subject_id +'/' + cluster + '_' + subject_id + '.in',"w+")
                for index, row in group.iterrows():
                    f.write(row['text'])
                f.close()
    # RUN MEDTAGGER AND SCISPACY
                 
####################################################################################
    #step: salience and topic extraction  
    if (first_run_this):
        #extract the most salient words to form the word summaries for each cluster
        concept_extration = second_run_this
        #make data frame with the needed info per cluster
        cluster_data = pd.DataFrame (columns = ['name', 'title', 'department', 'date_start', 
            'date_stop', 'disease_words', 'drugs_words', 'procedure_words', 'bookmark'])
        for cluster in clusters:
            #open medtagger file and extract term and the category
            fileTags = codecs.open('./Medtagger_output/output/patient_'+ subject_id + '/' + cluster + '_' + subject_id + '.in.ann', 'r')
            fileTags = fileTags.read()
            fileTags = fileTags.splitlines()
            for i in range(len(fileTags)):
                fileTags[i] = fileTags[i].split('\t')
            
            fileTags_set = set() #tags from medtagger from disease, drug, procedure or chemical category
            for element in fileTags:
                if ('DISO' in element[8] or 'DRUG' in element[8]
                    or 'PROC' in element[8] or 'CHEM' in element[8]):
                    fileTags_set.add((element[1], element[8]))
            fileTagsMed = [[], []] # index 0 is diseases and index 1 is treatment
            #fill fileTagsMed
            for x in list(fileTags_set):
                if 'DISO' in x[1]:
                    fileTagsMed[0].append([x[0], x[1]]) 
                if 'DRUG' in x[1] or 'PROC' in x[1] or 'CHEM' in x[1]:
                    fileTagsMed[1].append([x[0], x[1]])
            
            with open('./patient_data/tags_sci_' + cluster + '_' + subject_id + '.json') as f:
                fileTagsSci = json.load(f) #tags from scispacy lib
            # print(fileTagsSci)

            mergedTags = [] # term with tags that overlap in both
            #add term with disease tag in scispacy and medtagger
            for tagMed in fileTagsMed[0]:
                tagMed[0] = tagMed[0].replace('"', "")       
                for tagSci in fileTagsSci:
                    if 'DISEASE' in tagSci[1] and tagSci[0] == tagMed[0]:
                        mergedTags.append(tagSci)
            #add term with procedure or drug tag in medtagger and add term with chemical tag in medtagger and scispacy
            for tagMed in fileTagsMed[1]:
                tagMed[0] = tagMed[0].replace('"', "")  
                tagMed[1] = tagMed[1].replace('"', "")  
                if 'PROC' in tagMed[1] or 'DRUG' in tagMed[1]:
                    mergedTags.append([tagMed[0], tagMed[1]])           
                for tagSci in fileTagsSci:
                    if 'CHEMICAL' in tagSci[1] and tagSci[0] == tagMed[0]:
                        mergedTags.append(tagSci)
            
            # first extract the TUI and CUI from all terms
            if (concept_extration):
                topic_saliences(mergedTags, cluster, concept_extration, subject_id) #True > matched to UMLS, false > uses teh UMLS codes as well
            else: #then make extract the 5 most salient words for the word summaries per cluster per disease, drugs, treatment category
                words_result = topic_saliences(mergedTags, cluster, concept_extration, subject_id)
                if('check' in cluster):
                    title = 'Check-ups'
                else:
                    title = 'Admission'
                cluster_data = cluster_data.append({'name': cluster, 'title' : title, 
                    'department' : None, 'date_start': None , 'date_stop': None, 
                    'disease_words': words_result[0], 'drugs_words': words_result[1], 
                    'procedure_words': words_result[2], 'bookmark': False}, ignore_index = True)

#write to json files for site   
    if(finally_run_this):        
        for cluster, group in data.groupby('cluster'):
            cluster = cluster
            first_instance = True
            department = set()
            for index, row in group.iterrows():
                #format start and stop date of cluster differently 
                if (first_instance):
                    start_date = str(row['chartdate'])
                    start_date = start_date[:10]
                    first_instance = False
                stop_date = str(row['chartdate'])
                department.add(row['category'])
            stop_date = stop_date[:10]
            stop_date = stop_date.split('-')
            stop_date = stop_date[2] + '-' + stop_date[1] + "-" + str(int(stop_date[0])-130)
            # find all departments of all notes of one cluster 
            department = list(department)
            dep_string = ''
            for j in range(len(department)):
                if(j < len(department) -1):
                    dep_string += department[j] + ";"
                else:
                    dep_string += department[j] 
            department = dep_string
            ind_cluster = cluster_data.index[cluster_data['name'] == cluster].tolist()
            if(ind_cluster):
                cluster_data.at[ind_cluster, 'department'] = department
                cluster_data.at[ind_cluster, 'date_start'] = start_date
                cluster_data.at[ind_cluster, 'date_stop'] = stop_date
        pd.set_option("display.max_rows", None)   
        print(cluster_data) 

        cluster_array = [] 
        cluster_data['date_start'] = pd.to_datetime(cluster_data.date_start)  
        cluster_data = cluster_data.sort_values(by='date_start')
        cluster_data.reset_index(drop=True, inplace=True)     
        for index, row in cluster_data.iterrows():
            date_start = str(row['date_start'])[:10]
            date_start = date_start.split('-')
            date_start = date_start[2] + '-' + date_start[1] + '-' + str(int(date_start[0])-130)
            dict_cluster = {
                'id' : index, 
                'name': row['name'],
                'title': row['title'],
                'department': row['department'].split(';'),
                'date_start': date_start,
                'date_stop': row['date_stop'],
                'disease_words': row['disease_words'], 
                'drugs_words': row['drugs_words'], 
                'procedure_words': row['procedure_words'], 
                'bookmark': row['bookmark']
            } 
            cluster_array.append(dict_cluster)

        cluster_to_json = {'clusters': cluster_array}
        with open('./patient_data/clusters_' + subject_id +  ".json", 'w') as f:
            json.dump(cluster_to_json, f)

        notes_array = []
        for index, row in data.iterrows():
            #format date
            date = str(row['chartdate'])
            date = date[:10]
            date = date.split('-')                    
            date = date[2] + '-' + date[1] + "-" + str(int(date[0])-130)
            text = row['text']
            #remove some characters from text for readability 
            text = re.sub('_+', ' ', text)
            text = re.sub('\*+', '', text)
            text = re.sub('\\n\\n+|\\n \\n', '<br><br>', text)
            text= re.sub('\\n', '', text)
            
            dict_note = {
                'id' : index, 
                'date_start': date,
                'cluster': row['cluster'],
                'title': row['category'],
                'department': [row['category']],
                'bookmark': False,
                'text': text
            } 
            notes_array.append(dict_note)

        notes_to_json = {'Notes': notes_array}
        with open('./patient_data/Notes_' + subject_id +  ".json", 'w') as f:
            json.dump(notes_to_json, f)



                    