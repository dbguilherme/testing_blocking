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
<<<<<<< HEAD
    def __init__(self,total_num_attr):
=======
    def __init__(self, total_num_attr, encoding_methods, comparison_methods, 
                 min_threshold, min_total_threshold,alac_repetition):
>>>>>>> e2341f7e498a088bb6df57cb79b6c8e931036263
              
        self.alac_repetition=alac_repetition      
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
        
<<<<<<< HEAD
        self.true_positive=0;
        self.false_positive=0;
        self.false_negative=0
        self.true_negative=0
        self.compute=0
        
        self.first_time_active=1
#         self.training_set_final=[]
        self.gabarito=[]
        self.numberOfPairs=0;
=======
        self.true_positive=0.0;
        self.false_positive=0.0;
        self.true_negative=0.0;
        self.false_negative=0.0;
        self.pairs_count=0.0;
>>>>>>> e2341f7e498a088bb6df57cb79b6c8e931036263

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
            if(i > 4):
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
                
            
<<<<<<< HEAD
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
=======
           # print join
        size_gab=0   
        for inv_list in self.inv_index_gab.itervalues():
            if(len(inv_list)>1):
                size_gab+=len(inv_list)-1 
           # print inv_list[0]
        print ' TAMANHO GAB %d' % size_gab
        saida.close()
        return file_out
        
>>>>>>> e2341f7e498a088bb6df57cb79b6c8e931036263

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
       
<<<<<<< HEAD
       ###################################################
       
    def create_data_file(self, ent_id,res_list):
         
        list_of_dict_=[]
        gabarito=[]
        label=[]
        if (res_list != [] and len(res_list)>1):  # Some results were returned
            for i in range(len(res_list)):
               
               #caso sejam iguais                   
                if(ent_id==res_list[i]):
=======
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
       #print months_ordered 
       #for k,v in months_ordered.iteritems():
       #    print "k %s v %i " % (k,v)
       return rec_sorted   
                
                

         
# =============================================================================================== 

    def query(self, rec_id,query_rec):
           #print 'staring query phare\n'
        inv_index = self.inv_index  # Shorthands to make program faster
        min_tot_thres = self.min_tot_thres
        num_attr_without_rec_id = self.num_attr_without_rec_id
        sim_dict = self.sim_dict
        entity_records = self.entity_records
        num_compared_attr = self.num_compared_attr
             
           # Calculate when to switch the accu building phase
        #
        phase_thres = num_compared_attr - min_tot_thres 
       # print ("----------------------------" + str(query_rec) +str (rec_id))
       
                             
        ent_id = rec_id
       
        query_sort= self.resort_record(query_rec)  
        #print "rec_values %s" % query_rec[3]
        
        # Process all attribute values started from 1 since the first
        # attribute is the query record is the entity id 
        
        rec_id_list=[]
        i=0
        for rec_val,v in query_sort.iteritems():     
            if(i > 7):
                break;
            i=i+1
            #print rec_val
            if(rec_val == 'norole' or rec_val == ''  or len(rec_val)<2):
>>>>>>> e2341f7e498a088bb6df57cb79b6c8e931036263
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
                
<<<<<<< HEAD
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
=======
                
                rec_id_list_temp=inv_index.get(rec_val_ind, [])                 
              
                if(len(rec_id_list)==0):                    
                    rec_id_list=rec_id_list_temp;
                else:
                    for id in rec_id_list_temp:
                
                        if(id not in rec_id_list):
                            rec_id_list.append(id);
             
        #spec_info = ( )
       
        
        return (rec_id_list, 0)
        
        
        
        ###########################################
      
    def remove_query(self, rec_id,query_rec):
    
    
         inv_index = self.inv_index  # Shorthands to make program faster
            
         num_attr_without_rec_id = self.num_attr_without_rec_id
         
         entity_records = self.entity_records
         num_compared_attr = self.num_compared_attr
            
         rec_id_list=[]
         for i in range(0, num_attr_without_rec_id ):     
                
       
               rec_val = query_rec[i]   
                
                
              #  print "     performing att rec_val %s \n" % rec_val
               # if(rec_val == '' or rec_val == 'norole' or len(rec_val)<2):
               if(rec_val == 'norole' or rec_val == ''  or len(rec_val)<3):
                   continue
               # print rec_val
                
               rec_val_ind = '%s' % (rec_val)     # Add attribute type for inverted
                                                        # index values
            
    def create_output_file(self, ent_id,res_list,f):
        
        
        # self.pairs_count=0
         if (res_list != [] and len(res_list)>0):  # Some results were returned
            for i in range(len(res_list)):
                 try:
                    #cado sejam iguais                   
                    if(ent_id==res_list[i]):
                        continue
                    
                    
                    valueA=self.query_records[ent_id]
                    valueB=self.query_records[res_list[i]]
                    sim=[]
                    for j in range(1,len(valueA)):
                       # print ("%s   %s   %f") % (valueA[j],valueB[j], stringcmp.jaro(valueA[j], valueB[j]))
                        f.write(str(self.comp_methods[1](valueA[j], valueB[j])) + ", ")
                       #((stringcmp.jaro(valueA[j], valueB[j])))
                              
                   #false match 
                    if(("dup") not in ent_id and  ("dup") not in res_list[i]):
                    #    print "false match 1"
                        ##query_acc_res.append('FM')
                        f.write("0")
>>>>>>> e2341f7e498a088bb6df57cb79b6c8e931036263
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
<<<<<<< HEAD
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
=======
                            res_clean=res_list[i]                        
                        #if("507-" in ent_id):
                        #        print "chegouuuuuuuuuuuuuuuuuuuuuuuuuuuu %s  %s" % (res_clean, res_list );  
                        if(res_clean==ent_clean):
                            gab_list=self.inv_index_gab.get(res_clean,[])
                           
                            if(dirty in gab_list or res_list[i] in gab_list):                             
                                #gab_list.remove(dirty)
                                #query_acc_res.append('TM')
                                #ind.inv_index_gab[dirty]=gab_list
                                f.write("1")
                                self.pairs_count+=1
                            #else:
                                #print "XXXXXres clean %s %s" % (res_clean,gab_list)
                        else:
                           # print "false match 2"
                            #query_acc_res.append('FM')
                            f.write("0")
                            
                    f.write("\n")
                   
                 except IndexError:
                        print "Oops!  That was no valid number.  Try again... %s %s" % (ent_id,res_list) 
        
        
>>>>>>> e2341f7e498a088bb6df57cb79b6c8e931036263
       
    def header(self,file):
        #file_out="/tmp/final_treina.arff"
        f = open(file, 'w')
        f.write("@relation TrainingInstances\n")
        for i in range(0,5):
            f.write("@attribute att"+str(i) +" numeric\n")
        f.write("@ATTRIBUTE class {0,1}\n @DATA\n")
        f.write("1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.611111111111, 1.0, 1.0, 1.0, 1.0, 0.0, 0.558080808081, 1.0, 1.0, 1.0, 1")
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
           
        
        active = Active_learning(0)
        assemble=EnsembleClassifier(weights=[1,1,1])
        classifier_o= classification(assemble)
        
        print
        print('Testing method: {0}'.format(index_name))
        print('================' + '=' * len(index_name))
        print       
        start_time = time.time() 
        
        
<<<<<<< HEAD
        self.load(file_name,build_percentage)
        load_time = time.time() - start_time
=======
    ##############encontrar bug aqui!!!!!!!!!!!!!!!!!!!!!!!!!
    def allac (self, file, flag):
        self.count+=1000;
        if(flag==1):
            os.system("cd ssarp &&  rm train-B16-* ")
            os.system("cd ssarp &&  ./gera_bins_TUBE.sh "+ file +"  16")
            os.system("cd ssarp && ./discretize_TUBE.pl train-B16 "+file+ "  16 lac_train_TUBEfinal.txt 1")
            os.system("cd ssarp && ./updateRows.pl lac_train_TUBEfinal.txt lac_train_TUBEfinal_rows.txt " + str(self.count))
            os.system("cd ssarp && rm alac_lac_train_TUBEfinal_rows.txt")
            os.system("cd ssarp && ./run_alac_repeated.sh lac_train_TUBEfinal_rows.txt 1 " +str(self.alac_repetition))
            os.system("cd ssarp && ./desUpdateRows.pl alac_lac_train_TUBEfinal_rows.txt alac_lac_train_TUBEfinal.txt " + str(self.count))
            os.system("cd ssarp && cat alac_lac_train_TUBEfinal.txt | awk '{ print $1 }'  | while read instance; do  sed  -n  \"$instance\"p  " + file+"; done >> /tmp/final_treina.arff;")
           
            #sys.stdin.read(1)
        else:
            #os.system("cd ssarp &&  rm train-B16-* && ./gera_bins_TUBE.sh "+ file +"  16")
            os.system("cd ssarp && ./discretize_TUBE.pl train-B16 "+file+ "  16 lac_train_TUBEfinal.txt 1")
            
            os.system("cd ssarp && ./updateRows.pl lac_train_TUBEfinal.txt  lac_train_TUBEfinal_rows.txt  " + str(self.count))
            os.system("cd ssarp && cat alac_lac_train_TUBEfinal_rows.txt >> lac_train_TUBEfinal_rows.txt") 
            os.system("cd ssarp && ./run_alac_repeated.sh lac_train_TUBEfinal_rows.txt 1 "+str(self.alac_repetition))
            os.system("cd ssarp && ./desUpdateRows.pl alac_lac_train_TUBEfinal_rows.txt_2 alac_lac_train_TUBEfinal.txt " + str(self.count))
            os.system("cd ssarp && cat alac_lac_train_TUBEfinal.txt | awk '{ print $1 }'  | while read instance; do  sed  -n  \"$instance\"p  " + file+"; done >> /tmp/final_treina.arff;")
            #os.system("cd ssarp && cat alac_lac_train_TUBEfinal.txt >> lac_train_TUBEfinal.txt")
           # sys.stdin.read(1)
            #os.system("cd ssarp && wc -l alac_lac_train_TUBEfinal.txt")  
           # print ("erro ")
        #os.system("cd ssarp && cat "+file+" > /tmp/temp " )
        
        
        
    def arfftoSVM(self, inputfilename,outfile):
        print "gerando arquivo svm"
        fin = open(inputfilename,'r')
        lines = fin.readlines()
        #fin.close()
        outputfilename = outfile
        fout = open(outputfilename,'w')
        
        beginToRead = False
        for line in lines:
            flag=0    
            
               # print("entrou leitura das linhas...............................")
               
            if len([pos for pos, char in enumerate(line) if char == ','])>5:
                if len(line) > 1:# not an empty line
                    #read this line
                    dataList = line.split(',')
                    resultLine =''
                    resultLine += dataList[-1].strip()
                    if (flag==0):
                        resultLine += ' '
                        flag=1
                        
                    for i in range(1,len(dataList)-1):
                        resultLine += str(i)
                        resultLine += (":"+dataList[i].strip()+" ")
                    #print(resultLine)
                    fout.write(resultLine+"\n")
            

        fout.flush()
        fout.close()
>>>>>>> e2341f7e498a088bb6df57cb79b6c8e931036263
        
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
       
        
        
        rf = SVC(kernel='rbf', C=1.0) #ExtraTreesClassifier(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
        query_time_res = []  # Collect results for each of query record
        class_time = []
        process_time = []
        
        df=pd.DataFrame()
        df_train=pd.DataFrame()
        flag_active=1;
        first_time_active=1
        
<<<<<<< HEAD
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
                        
               
            if(len(df)>500 or flag_active==0):
                 
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
=======
        rate, param = find_parameters(svm_file, '-out mull -resume -log2c -1,1,1 -log2g -1,1,1 -gnuplot null')
        #print "xxxxxxxxxxxxxxxxxx %s %s" % (param.get('c'),(param.get('g')))
        
        p='-q '+ '-c '+ str(param.get('c')) +' -g ' + str(param.get('g')) 
        m = svm_train(y, x, p) 
        return m 
         
         
    def test_svm(self, model, file_full):  
        Y, x = svm_read_problem(file_full)
        
       # x0, max_idx = gen_svm_nodearray({1:1, 3:1})
        _labs, p_acc, p_vals = svm_predict(Y, x, model)
      
        
        #for i in xrange(len(y)):
            #if(y[i] != _labs[i]):
                #self.false_positive+=1;
            #else:
                #self.true_positive+=1;
       # print (Y)        
        t=0
        for i in Y:
            if i==1.0:
                t+=1
        print ("valor do t \n" + str(t))
        for i in range(len(x)):
# 				if(avg[i][0]>0.2 and avg[i][0]<0.8):
# 					print ("instavel ...."+ str(X.iloc[i].name)+"  " +str(avg[i]))
			if( _labs[i]==1 and Y[i]==1):
				
				self.true_positive+=1;
				
				#print ("------------------------------------------------------------true positive pair ")				
				#remove do gabarito as tags reais 
				
			#false positive
			if(_labs[i]==1 and Y[i]==0):
				self.false_positive+=1;
				#print( " false positive " + str(i) + "  "+  "  "+str(avg)  )
			#false negative 
			if(_labs[i] ==0 and Y[i]==1):
				
				
				#print(df_train.to_string())
				#if(len(df_train)>0):
				
				
				#print (x[i])
				self.false_negative +=1;
			if(_labs[i] ==0 and Y[i]==0):
				self.true_negative +=1;	
>>>>>>> e2341f7e498a088bb6df57cb79b6c8e931036263
        
        
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

<<<<<<< HEAD
       
    
=======
def run(sys):
    
    total_num_attr = 15  # Total number of attribute 
                        # including rec-id, and ent-id
    alac_repetition = int(sys.argv[1])          # Minimal similarity threshold
    min_threshold = float(sys.argv[2])          # Minimal similarity threshold
    min_total_threshold = float(sys.argv[3])    # Minimal total threshold
    build_percentage = float(sys.argv[4])       # Percentage of records used to
                                                # build the index
    file_name = sys.argv[5]             # optimization flag
    arff_file="/tmp/final_treina.arff"
    svm_file="/tmp/final_treina.svm"
    svm_file_full="/tmp/svm_full.svm"
    file_input="/tmp/arff_out"
    index_name = 'Active Online Blocking'
    # Define encoding and comparison methods to be used for attributes
    # Note: first element in the list should always be None. 
    enco_methods = [None, encode.dmetaphone, encode.dmetaphone, 
                    encode.dmetaphone, __get_substr__,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,]
    comp_methods = [None, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro , stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro]
    
    ind = ActiveOnlineBlocking(total_num_attr,enco_methods, comp_methods, 
                  min_threshold, min_total_threshold,alac_repetition)
     
    
    print
    print('Testing method: {0}'.format(index_name))
    print('================' + '=' * len(index_name))
    print       
    
    start_time = time.time()  # Load data set from file(s)
    ind.load(file_name,build_percentage)
    load_time = time.time() - start_time
    
    print(' Loading time: %.1f sec' % (load_time))
    
    # Getting memory usage does not work in windows
    load_memo_str = auxiliary.get_memory_usage()
    print '    ', load_memo_str
    print  
    ##
   
   
   
    # Match query records - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    query_time_res = []  # Collect results for each of query record
    query_acc_res = []
    num_comp_res = []
    
    query_cnt = 1
    num_rec = 0
    print ' Processing Query records ...'
   
    # Go through query records and try to find a match for each query 
    tuples_count=0
    count = 0 # count of true duplicates 
    flag=1;
    first_time=1
    f = open(file_input, 'w',100)
    #print(ind.query_records)
    
    #for attribute, value in ind.query_records.iteritems(): 
        #print('{} : {}'.format(attribute, value))
    ind.header(arff_file)
    for rec_id, clean_rec in ind.query_records.iteritems():
       
        if  rec_id =="":
            continue
        ent_id = rec_id
        #print 'PERFOMING RECORD %s \n\n' %   ((rec_id))
        start_time = time.time()
        res_list, num_comp = ind.query(rec_id,clean_rec)
        query_time = time.time() - start_time
        #print ind.count
        
        num_rec += 1
        if (num_rec % 100 == 0):
            print '\t Processed %d records in the query phase' % (num_rec)
            #print "inverted inde size %i" % ((ind.count))
            
        query_time_res.append(query_time)
        num_comp_res.append(num_comp)
            
            
        
        tuples_count+=len(res_list);
        #print("xxx " +str(ind.pairs_count))    
        #gera arquivo de saida para avaliacao da tupla
        ind.create_output_file(ent_id, res_list,f)
        
        
        if(first_time==1):
            f.write("1.0, 1.0, 1.0, 1.0, 1.0, 1., 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1\n");
            first_time=0
        
       
            
        if(tuples_count>200):             
            f.flush()    
        #     if(flag==1):
            ind.allac(file_input, flag)
            flag=0;
                    #########################treinamento do SVM
                
            ind.arfftoSVM(arff_file, svm_file);
            model= ind.train_svm(svm_file)  
                
                
                    #flag=0;   
                ## if(flag==0):
            tuples_count=0                      
        
           
        
        
       
            
            #print("file size %s" % len(res_list))

            ind.arfftoSVM(file_input, svm_file_full);
            ind.test_svm(model,svm_file_full); 
           # sys.stdin.read(1)
            f.close            
            open(file_input, 'w').close()
            f = open(file_input, 'w',100)
            open(svm_file_full, 'w').close()
            
            
    #if((len(res_list))>0):
       #ind.arfftoSVM(file_input, svm_file_full);
       #ind.test_svm(model,svm_file_full);       
     #############################################################     
       

        
   # query_memo_str = auxiliary.get_memory_usage()
   # print "COUNTTTTT %s" % count;  
    
    print "false positive %i" % ind.false_positive
    print "true positive %i" % ind.true_positive
    print "false negative %i" % ind.false_negative
    print "true negative %i" % ind.true_negative
    
    try:
        p =  ind.true_positive /(ind.true_positive+ind.false_positive)
        r=  ind.true_positive /(ind.true_positive + ind.false_negative)
        print ("p %s %s " % (p,r))
       # print ("GABARITO " + str(ind.pairs_count))
        print ("tamanho do garito")
        print (os.system("wc /tmp/final_treina.svm"))
    except Exception:
        print "Oops!  Precision or recall equal to zero  Try again... "  
        
    
    
    #if (1==1):
        #exit()
    
    #####################
    #f.close()
    
      
    #size_gab=0   
    #print (ind.inv_index_gab)
    #for inv_list in ind.inv_index_gab.itervalues():
        #if(len(inv_list)>1  ):
            #size_gab+=len(inv_list)-1
            ##print "%s %d " % (inv_list,len(inv_list))
            ##for i in inv_list:
                ##print ("gab %s \n\n" % inv_list[i])
    #print (' TAMANHO GAB %d' % size_gab)

   # values.sort()
    #print ind.inv_index
    
    # Summarise query results - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    #num_tm = query_acc_res.count('TM')
    #num_fm = query_acc_res.count('FM')
    ##assert num_tm + num_fm == len(ind.query_records)
    #print
    #print ' Query summary results for index: %s' % (index_name)
    #print '-' * (33 + len(index_name))
    
    #print '  minimum threshold: %.2f;' % \
              #( min_threshold) + ' minimum total threshold: %.2f' % \
              #(min_total_threshold)
    ##if ind.count > 0:
        ##print '  Matching accuracy: %d/%d true matches (%.2f%%)' % \
              ##(num_tm, ind.count, 100.0 * num_tm / ind.count) 
    ##else:
        ##print' No duplicates where found' 
    #if num_tm>0 :    
        #print ' precisao %f  revo %f' %  ((100.0*num_tm/(num_tm+num_fm)),(100.0*num_tm/(size_gab+num_tm)))
        #print ' true pos %d  false posit %d' %  (num_tm, num_fm)
    #else:
        #print 'true matching equal zero'
        
   
  
if __name__ == '__main__':
    run(sys)


    
>>>>>>> e2341f7e498a088bb6df57cb79b6c8e931036263
