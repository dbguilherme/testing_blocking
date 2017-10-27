import string
import sys
import time
import os
from numpy.matlib import rand
from nltk.metrics.association import TOTAL

#from compiler.ast import Assert
sys.path.append("./libsvm/tools/")
sys.path.append("./libsvm/python/")
sys.path.append("./auxiliar/")
import distance
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn import svm

from lib import auxiliary,classifier,blocking, encode,stringcmp
from lib.active_learning import Active_learning
from lib.classifier import classification
from sklearn.svm import SVC
#import Active_learning from active_learning
#import random
from collections import OrderedDict,defaultdict
import collections
import copy
import numpy as np
from timeit import default_timer as timer
from treeinterpreter import treeinterpreter as ti
import pandas as pd
from lib.assemble import EnsembleClassifier

class ActiveOnlineBlocking:
    def __init__(self,total_num_attr):
              
        self.total_num_attr = total_num_attr
        self.enco_methods =  [None, encode.dmetaphone, encode.dmetaphone, 
                        encode.dmetaphone, self.__get_substr__,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,]
        self.comp_methods = [None, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist , stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist]
    
        
        
              
        
        self.rec_dict = {}  # To hold the data set loaded from a file. Keys in
                            # this dictionary are the record identifiers, 
                            # values are the cleaned records(attributes
                            # without the record identifier)
                            
                                    
        self.build_records = {} # A dictionary of the records that are used 
                                # in the build phase, keys are rec-id, and value
                                # is all other attributes
                                # ie: 
                                #{'rec-id': ['ent-id', 'att-1',..., 'att-n']
        
        self.query_records = {} # A dictionary of the records that are used in
                                # the query phase, it has the same structure 
                                # as the buid_records
        
        self.entity_records = {}    # A dictionary of entities, having the 
                                    # entity id as a key and a list of 
                                    # associated records as a value
                                    # i.e. {entity_id: [rec1,rec2,..], ...}
                                    
        
        self.inv_index = {} # (RI)The actual inverted index with record values
                            # as keys and lists of record identifiers. Note
                            # that all values will have a qualifier (1,2,3,..)
                            # added at the end to know a certain value is
                            # for a which attribute  
                            
                                   
        #self.sim_dict = {}  # (SI)The similarity values, with keys being record
                            # values, and values being sets of tuples with
                            # other (similar) record values and their actual
                            # similarity value. Note the values in this
                            # dictionary do not have attribute qualifiers
                            # added, in order to prevent duplication of
                            # similarity calculation and storage.
    
        self.block_dict = {}    # (BI)Keys are the encodings, and values are lists
                                # of record values in this block. Note the
                                # encoding values in this dictionary will have
                                # the attribute qualifier added.
         
        self.inv_index_word_count = {}# store token frequency 
        self.inv_index_gab = {}                                
        
        self.count = 0          # The number of true duplicates in the data set
         
        # Number of attributes in the data set without the rec_id field                            
        self.num_attr_without_rec_id = self.total_num_attr -1   
        
        # Number of actual attributes in the data set 
        # i.e. without the rec-id and ent-id
        self.num_compared_attr = self.total_num_attr - 2  
        
        self.true_positive=0;
        self.false_positive=0;
        self.false_negative=0
        self.true_negative=0
        self.compute=0
        
        self.first_time_active=1
#         self.training_set_final=[]
        self.gabarito=[]
        self.numberOfPairs=0;

# ===============================================================================================        
    
    
   
       
#===========================================================================
    def resort_record(self,query):
        
        inv_index_word_count=self.inv_index_word_count
        num_attr_without_rec_id = self.num_attr_without_rec_id
        rec_values={}
        rec_sorted=[]
        
            
        for i in range(0, num_attr_without_rec_id ):     
            if(query[i] not in inv_index_word_count):
                inv_index_word_count[query[i]]=1
            else: 
                inv_index_word_count[query[i]]=inv_index_word_count[query[i]]+1
            rec_values[query[i]]=(inv_index_word_count[query[i]])
        #sorted(rec_values.items(), key=lambda x: x[1])
        
        rec_sorted = OrderedDict(sorted(rec_values.items(), key=lambda t: t[1]))
        
        #print (rec_sorted)#print months_ordered 
        #for k,v in months_ordered.iteritems():
        #    print "k %s v %i " % (k,v)
        return rec_sorted   
                
                

         
# =============================================================================================== 

    def query(self, rec_id,query_rec):
       
        inv_index = self.inv_index  # Shorthands to make program faster
        rec_id_list=[]
        
        
        if(len(query_rec)==0):
            return (rec_id_list, 0) 
        
               
        query_sort= self.resort_record(query_rec)  
         
        
        i=0
        for rec_val,v in query_sort.items():     
            if(i > 8):
                break;
            i=i+1
            #print rec_val
            if(rec_val == 'norole' or rec_val == ''  or len(rec_val)<2):
                    continue
            
            rec_val_ind = '%s' % (rec_val)     # Add attribute type for inverted
                                                    # index values
            
            if (rec_val_ind not in inv_index):               
             
               
                if(rec_val == 'norole' ):
                    continue  
                #print "             insert att into index"
                self.inv_index=blocking.Insert_value(inv_index,rec_id,rec_val,i)
               
            else:
                             
                # Add the record id into the inverted index
                temp_list = inv_index.get(rec_val_ind, [])
               
                
                #print 'indice len %d %s' % (len(inv_index), rec_val)
                temp_list.append((rec_id))
                
               # if(len(temp_list)>150):
               #     temp_list=[]
                inv_index[rec_val_ind]= temp_list   
                #if(len(inv_index[rec_val_ind])>self.count):
                    #self.count=len(inv_index[rec_val_ind])
                    ##print "xxxxxxx %i %s" % (self.count,rec_val_ind)
                
            
                rec_id_list_temp=inv_index.get(rec_val_ind, [])                 
                if(len(rec_id_list)==0):                    
                    rec_id_list=rec_id_list_temp;
                else:
                    for id in rec_id_list_temp:
                
                        if(id not in rec_id_list):
                            rec_id_list.append(id);
             
        #spec_info = ( )
        #if(("dup") in rec_id ):
        #    print("---" + str(rec_id) +" rec  " + str(rec_id_list))
        return (rec_id_list, 0)
     
     
    def getLineNumber(self, filename):
        ''' Counts the line numbers of a file        it only works on csv '''

        lines = 0
        for line in open(filename):
            lines += 1
        return lines
 
        
    def load(self, file_name, build_percentage):
        """
        Load the data set and store it in memory as a dictionary 
        with record identifiers as keys.
            
        the loaded records are divided into to parts, the (build records) that 
        are used to build the inverted index, and the (query records) that are
        used as queries (i.e 10% build, 90% query).            
        """
        
        # Shorthand to make program faster
        rec_dict = self.rec_dict  
        build_records = self.build_records
        query_records = self.query_records
        entity_records = self.entity_records     
        
        
        print (' Loading data file...')
        
             
        # Get number of lines of the file   
       # num_lines = self.getLineNumber(file_name)-1
         
         
         ##############################################
        file_name=blocking.formatFile(self.inv_index_gab,file_name) 
        
        # Calculate the number of records that should be in the build 
        # dictionary based on the percentage provided by user
        #build_records_count = int(round(num_lines *
         #                                   float(build_percentage)/ 100))
            
            
        in_file = open(file_name)   
        
        
        # Skip over header line
        self.header_line = in_file.readline()  
            
        this_line_num = 0
        for rec in in_file:
            rec = rec.lower().lstrip()
            rec = rec.split(',')
                
            # Clean the record and remove all surrounding white-spaces
           # clean_rec = map(string.strip, rec) 
            clean_rec=[x.strip() for x in rec]
            #print ("xxxxxxxxxxxxxxx %s" % clean_rec)
            #Mmake sure that each record has the same number of attributes
            # which is equal to total_num_attr                    
           # assert len(clean_rec) == total_num_attr, (rec, clean_rec)
            
            # Get the record id of the record
            rec_id = clean_rec[0].lstrip()
            
            # Make sure that all rec_ids in the data set are unique
            assert rec_id not in rec_dict, ('Record ID not unique:', 
                                                rec_id)
            
            # Save the original record without the record identifier
            # in the rec_dict variable
            # i.e.{rec_id:[entity_id, attr-1, ..., attr-n],...}
            rec_dict[rec_id] = clean_rec[1:]
            
                   
            query_records[rec_id] = clean_rec[1:]
            this_line_num += 1
    
        print('\t Loaded file:                {0}'.format(file_name))
        #print (query_records)
        print('\t Total number of records: {0}'.
              format(len(rec_dict)))
        print
        print ('\t ({0}%) of the total records are used to build the index'.
               format(build_percentage))
        print('\t Query records are {0}:'.format(len(query_records)))
        print
        print('\t Number of records in rec_dict is {0}'.
              format(len(rec_dict)))
        print('\t Number of records in build_records is {0}'.
              format(len(build_records)))
        print('\t Number of records in query_records is {0}'.
              format(len(query_records)))
        print('\t Total number of records for build + query is {0}'.
              format(len(build_records)+ len(query_records)))
        print
        print 
        
               
        assert len(rec_dict) == len(build_records)+ len(query_records), 'len(rec_dict) != len(build_records)+ len(query_records '
           
    # ===============================================================================================                         
        
        ###########################################
      
#     def remove_query(self, rec_id,query_rec):
#     
#     
#          inv_index = self.inv_index  # Shorthands to make program faster
#             
#          num_attr_without_rec_id = self.num_attr_without_rec_id
#          
#          entity_records = self.entity_records
#          num_compared_attr = self.num_compared_attr
#             
#          rec_id_list=[]
#          for i in range(0, num_attr_without_rec_id ):     
#        
#                rec_val = query_rec[i]   
#               #  print "     performing att rec_val %s \n" % rec_val
#                # if(rec_val == '' or rec_val == 'norole' or len(rec_val)<2):
#                if(rec_val == 'norole' or rec_val == ''  or len(rec_val)<2):
#                    continue
#                # print rec_val
#                 
#                rec_val_ind = '%s' % (rec_val)     # Add attribute type for inverted
#                                                         # index values
       
       ###################################################
       
    def create_data_file(self, ent_id,res_list):
         
        list_of_dict_=[]
        gabarito=[]
        label=[]
        if (res_list != [] and len(res_list)>1):  # Some results were returned
            for i in range(len(res_list)):
               
               #caso sejam iguais                   
                if(ent_id==res_list[i]):
                    continue
                #if(("dup") in ent_id and  ("dup") in res_list[i]):
                #    continue
                
                
                valueA=self.query_records[ent_id]
                valueB=self.query_records[res_list[i]]
                dictionary={}
                for j in range(self.total_num_attr):
                    temp=self.comp_methods[1](valueA[j], valueB[j])
                    dictionary[j]=temp
                    #f.write(str(temp) + ", ")
                list_of_dict_.append(dictionary)  
                
                if(("dup") not in ent_id and  ("dup") not in res_list[i]):
                #    print "false match 1"
                    #query_acc_res.append('FM')
                   # f.write("0")
                    gabarito.append(0);
                    label.append(-1)
                else:
                    if(("dup") in ent_id):
                        ent_clean=ent_id.split("-")[0]
                        dirty=ent_id
                    else:
                        ent_clean=ent_id  
                        
                    if(("dup") in res_list[i]):
                        res_clean=res_list[i].split("-")[0]
                        dirty=res_list[i]
                    else:
                        res_clean=res_list[i] 
                            
                    if(res_clean==ent_clean):
                        gab_list=self.inv_index_gab.get(res_clean,[])
                        
                        if(dirty in gab_list or res_list[i] in gab_list):                             
                            if(("dup") not in ent_id):
                                label.append(res_list[i])                            
                            else:
                                label.append(dirty)                            
                            gabarito.append(1) 
                        else:
                            if(("dup") not in ent_id):
                                label.append(res_list[i])                            
                            else:
                                label.append(dirty)                            
                            gabarito.append(0) 
                    else:
                        label.append(-1)
                       # self.query_acc_res.append('FM')
                     #   f.write("0")
                        gabarito.append(0);
                           
        index=range(self.numberOfPairs,len(list_of_dict_)+self.numberOfPairs)
        dt=pd.DataFrame(list_of_dict_, index=index)
        self.numberOfPairs+=len(list_of_dict_)
        
        if(len(dt)>0):
            dt[100]=gabarito
            dt[1001]=label
            #print( "size -->>>")
            #print (dt)
        #          print (gabarito)      
        #          print (label)    
        assert (len(dt)==len(label)), "problem %s %s %s %s" %(ent_id,res_list, gabarito, label)   
        
        
#         size_gab=0   
#         for inv_list in ind.inv_index_gab.values():
#             if(len(inv_list)>1  ):
#                 size_gab+=len(inv_list)-1
#             #print ("%s %d " % (inv_list[0],len(inv_list)))
#             #for i in range(len(inv_list)):
#             #    print ("\n\ngab %s" % inv_list[i])
#         print (' TAMANHO GAB %d' % size_gab)                
        #print ("problem %s %s %s %i %s" % (ent_id,res_list, gabarito, len(list_of_dict_), label))
        return (dt)
       
    def header(self,file):
        #file_out="/tmp/final_treina.arff"
        f = open(file, 'w')
        f.write("@relation TrainingInstances\n")
        for i in range(0,5):
            f.write("@attribute att"+str(i) +" numeric\n")
        f.write("@ATTRIBUTE class {0,1}\n @DATA\n")
        f.flush();
        f.close();
      
         
 
    # Define special functions for post code encoding and comparison
    # Any other function can be used 
    def __get_substr__(self,s):  
        # Function used for post code blocking
        # Returns last three digits of post code
        return s[1:]  
            
    
    def __postcode_cmp__(self,s1, s2): 
        # Function for post code comparison: count
        # different digits. this function assumes that 
        # compared post cods are of the same length
        
        pc_length = len(s1)  # length of post code
        e = 0                # Number of equal digits found
        
        if len(s1) == len(s1):    
            for i in range(pc_length):  # Loop over positions in strings
                    if (s1[i] == s2[i]):
                        e += 1
        return e / float(pc_length)
    
    def run(self,file):
        print("starting active learning")
        total_num_attr = self.total_num_attr # Total number of attribute 
                            # including rec-id, and ent-id
       
        build_percentage = 0      # Percentage of records used to
                                                    # build the index
        file_name = file
#         arff_file="/tmp/final_treina.arff"
#         svm_file="/tmp/final_treina.svm"
#         svm_file_full="/tmp/svm_full.svm"
        
        index_name = 'Active Online Blocking'
#         line_number=0
        # Define encoding and comparison methods to be used for attributes
        # Note: first element in the list should always be None. 
           
        rf = SVC() #ExtraTreesClassifier(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
        active = Active_learning(0)
       # assemble=EnsembleClassifier(weights=[1,1,1])
        classifier_o= classification(rf)
        
        print
        print('Testing method: {0}'.format(index_name))
        print('================' + '=' * len(index_name))
        print       
        start_time = time.time() 
        
        
        self.load(file_name,build_percentage)
        load_time = time.time() - start_time
        
        build_time = time.time() - start_time
        print('  Finished loading the index.')    
        print ('  Loading time: %.1f sec' % (build_time))
        # Match query records - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #
#         query_time_res = []  # Collect results for each of query record
#         query_acc_res = []
#         num_comp_res = []
#         
#         query_cnt = 1
        num_rec = 0
        print (' Processing Query records ...')
       
        # Go through query records and try to find a match for each query 
        tuples_count=0
        count = 0 # count of true duplicates 
       
        
        
       
        query_time_res = []  # Collect results for each of query record
        class_time = []
        process_time = []
        
        df=pd.DataFrame()
        df_train=pd.DataFrame()
        flag_active=1;
        first_time_active=1
        
        for rec_id, clean_rec in self.query_records.items():        
           
            #print("RECORD ID " +str(rec_id) )
            ent_id = rec_id
            start_time = time.time()
            res_list, num_comp = self.query(rec_id,clean_rec)
            
           # print "query %s pairs %s" % (rec_id, res_list)
            query_time = time.time() - start_time
            query_time_res.append(query_time)
            num_rec += 1
            if (num_rec % 100 == 0):
                
               
                print ('\t Processed %d records in the query phase' % (num_rec))
                #print "inverted inde size %i" % ((ind.count))
        
            start_time = time.time()
            df =df.append(self.create_data_file(ent_id, res_list))
            timecreate = time.time() - start_time
            process_time.append(timecreate)
            
            if(len(df)==0):
                continue;
                        
               
            if(len(df)>40):
                 
                count = 0 
                 # print ("numero de pares a serem processados %i" % (len(set_list_of_pairs)))
    #            
                 # f.flush()
                if(flag_active==1):             
                    # print ("\n ############################starting active  \n\n")             
                    df_train ,flag =(active.active_learning(df,df_train,1,total_num_attr))
                    first_time_active=0
                    flag_active=0
                    model = classifier_o.train(df_train,total_num_attr)
                    
                start_time = time.time()    
                df_train =classifier_o.test_svm_online(rf, df,df_train,model,self,total_num_attr, active,flag_active) 
                timeclass = time.time() - start_time
                class_time.append(timeclass)
         
                df=pd.DataFrame()
                
        if(len(df)>0):     
            df_train =classifier_o.test_svm_online(rf, df,df_train,model,self,total_num_attr, active,flag_active)
        print ("####################")
        print ("false positive %i" % self.false_positive)
        print ("true positive %i" % self.true_positive)
        print ("false_negative %i" % self.false_negative)
        print ("true_negative %i" % self.true_negative)
        print ("full size %i" % self.compute)
        
        pos=neg=0
        print ("TREINING SIZE " + str(len(df_train)))
        for i in range(len(df_train)):
            if(df_train.iloc[i,total_num_attr]==1):
                pos+=1
            else:
                neg+=1
                
        print ("True labels " + str(pos) +"  false labels  " +str(neg))
        
        
        print ('  Query timing %.3f sec' %             (sum(query_time_res))) 
        print ('  class_time timing %.3f sec' %             (sum(class_time) ))
        print ('  process_time timing %.3f sec' %            ( sum(process_time)))
         
         
           
        size_gab=0   
        for inv_list in self.inv_index_gab.values():
            if(len(inv_list)>1  ):
                size_gab+=len(inv_list)-1
                print ("%s %d " % (inv_list[0],len(inv_list)))
              #  for i in range(len(inv_list)):
              #      print ("\n\ngab %s" % inv_list[i])
        print (' TAMANHO GAB %d' % size_gab)
        pre=(100.0*self.true_positive/(self.true_positive+self.false_positive))
        recall=(100.0*self.true_positive/(self.false_negative+self.true_positive+size_gab))
        print (' precisao %f  revo %f' % (pre,recall))  
        # Summarise query results - - - - - - - - - - - - - - - - - - - - - - - - -
        #
#         num_tm = query_acc_res.count('TM')
#         num_fm = query_acc_res.count('FM')
#         #assert num_tm + num_fm == len(ind.query_records)
#         print
#         print (' Query summary results for index: %s' % (index_name))
#         print ('-' * (33 + len(index_name)))
    #=============================================================================
    
        print("XXXPREC %i , %i " %( pre,recall))

       
    