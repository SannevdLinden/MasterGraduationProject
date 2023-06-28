from doc_clustering import doc_clustering
import pandas as pd

def clustering(info, data, number_admissions):
    for index, row in data.iterrows():
        #remove <br> from redundancy step
        tmp = row['text'].replace('<br>','')
        data.at[index, 'text'] = tmp
    #initiate new column with header cluster and none entries for all rows
    data.insert(1, 'cluster', None)
        
    for index, row in data.iterrows():
        # no ER without admission or small interventions cluster types in this dataset  
        # cluster all the hospital admission
        for i in range(number_admissions):
            if (row['hadm_id'] == info['hadm_id'][i]):
              data.at[index, 'cluster'] = 'hop_admis_' + str(i)       
          
    
    none_entries = []
    non_admission_groups = [] #indexes of check-up notes in between admissions clusters
    non_admissions = data     
    non_admissions.insert(0, 'id', -1)   
    temp = []
    #add all notes that do not have a cluster yet to a group (all notes between two 
    # admission, the start and the first admission or the stop and the last admission) 
    for index, row in non_admissions.iterrows():
        if(row['cluster'] == None):
            non_admissions.at[index, 'id'] = index           
            if(index != 0 and data['cluster'][index - 1] != None):
                non_admission_groups.append(temp)
                temp = []
            if(index == (len(non_admissions) -1)):
                non_admission_groups.append(temp)
            temp.append(index)                
    non_admissions = non_admissions[non_admissions['id'] != -1]
    
    print("GROUPS")
    print(non_admission_groups)

    for index, row in data.iterrows():
        if(row['cluster'] == None):
            none_entries.append(index)
    
    #if there are no check-up notes than program is done
    if (len(none_entries) == 0):
        return data
    #if there is only one check-up note is has its own cluster
    elif (len(none_entries) == 1):
        data.at[none_entries[0], 'cluster'] = 'check_up_' + str(number_admissions)
        return data
    # if there are multiple check-up notes they need to be clustered based on the HDBSCAN algo and date
    else:
        #cluster docs with HDBSCAN
        dbscan = doc_clustering(non_admissions)
        #check-up cluster count 
        checkup_count = 0
        db_offset = 0 #start index to get a substring of the cluster labels corresponding to that group
        for i in range(len(non_admission_groups)): #for all groups 
            dbscan_part = dbscan[db_offset: (db_offset + len(non_admission_groups[i]))] #part of the dbscan labels for this group
            indices_date = [] #per admission group an array containing the indexes of the docs on the same day [[day 1], [day 2]]
            temp_date = [] 
            for j in range(len(non_admission_groups[i])):
                #find all indexes with same chart date in this group to fill indices_date 
                if(j != 0 and data['chartdate'][non_admission_groups[i][0] + j - 1] != data['chartdate'][non_admission_groups[i][0] +j]):
                    indices_date.append(temp_date)
                    temp_date = []
                if(j == (len(non_admission_groups[i]) -1)):
                    indices_date.append(temp_date)
                temp_date.append(j) 
            
            for day in indices_date: #for each day in this group
                vals = [] #all cluster number values of this day
                if(data['cluster'][non_admission_groups[i][0] + day[0]] == None):
                    #all docs on the same day get assigned to the same cluster
                    for notes_ind in day:
                        data.at[non_admission_groups[i][0] + notes_ind, 'cluster'] = 'check_up_' + str(checkup_count)
                        vals.append(dbscan_part[notes_ind]) #append all cluster number of the docs of this day

                    vals_done = [] #cluster values that are already checked                    
                    # different days are merged together if they have an overlapping cluster value
                    while len(vals) > 0: #while there are still values to be checked do this                    
                        if (vals[0] != -1): #cluster number value is not an outlier
                            for day2 in indices_date: #check all other day groups
                                day_dbscan_vals = [] #all cluster number values of that day
                                for notes_ind2 in day2:
                                    day_dbscan_vals.append(dbscan_part[notes_ind2])                              
                                if(vals[0] in day_dbscan_vals): #if that day contains val then this day also in same cluster
                                    for z in day_dbscan_vals: #add all new cluster val to vals to be checked
                                        if(z != vals[0] and z not in vals_done):
                                            vals.append(z)    
                                    for notes_ind2 in day2: #give this day the same cluster name
                                        data.at[non_admission_groups[i][0] + notes_ind2, 'cluster'] = 'check_up_' + str(checkup_count)
                            vals_done.append(vals[0]) #add cluster number value to checked
                            del vals[0] #delete the checked cluster number value
                        else:
                           vals_done.append(vals[0]) #add cluster number value to checked
                           del vals[0] #delete the checked cluster number value
                    checkup_count += 1           
            db_offset += len(non_admission_groups[i])        
        return data
   