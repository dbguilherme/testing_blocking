import string
import sys
import time
import os
from numpy.matlib import rand
#from compiler.ast import Assert
sys.path.append("./libsvm/tools/")
sys.path.append("./libsvm/python/")
sys.path.append("./auxiliar/")
import distance


import auxiliary
import encode
import stringcmp
import random
from collections import OrderedDict,defaultdict
from svmutil import *
from grid import *
import collections
import copy
import numpy as np
from timeit import default_timer as timer


class ActiveOnlineBlocking:
    def __init__(self, total_num_attr, encoding_methods, comparison_methods, 
                 min_threshold, min_total_threshold):
              
        self.total_num_attr = total_num_attr
        self.enco_methods = encoding_methods
        self.comp_methods = comparison_methods
        self.min_thres = min_threshold
        self.min_tot_thres = min_total_threshold
        
        
        self.rec_dict = {}  # To hold the data set loaded from a file. Keys in
                            # this dictionary are the record identifiers, 
                            # values are the cleaned records(attributes
                            # without the record identifier)
                            
        self.top_x_rec = {} # A Dictionary of lists that holds the top X 
                            # percent Of all attributes most frequent values  
                            
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
                            
                                   
        self.sim_dict = {}  # (SI)The similarity values, with keys being record
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
        self.training_set_final=[]
        self.gabarito_set_final=[]

# ===============================================================================================        
    
    
    def getLineNumber(self, filename):
        ''' Counts the line numbers of a file
            it only works on csv '''

        lines = 0
        for line in open(filename):
            lines += 1
        return lines


    def formatFile(self, filename):
        
        inv_index_gab = self.inv_index_gab  
        count = 0
        #for line in open(filename):
            
        #return lines
        #file_out="/tmp/teste"+str(random.randint(0, 100))
        file_out="/tmp/teste"
        saida=open(file_out, 'w')
        with open(filename) as books:
            lines = books.readlines()   
        
        for rec in lines:
            rec = rec.lower().strip()
            rec = rec.split(',')
            rec[0]= rec[0].replace('rec-','').replace('-org','')
            #.replace('-dup-0','')
            #rec[0]=rec[0].replace('-dup-1','').replace('-dup-2','').replace('-dup-3','').replace('-dup-4','').replace('-dup-5','')
#             if (count == 0):
#                 saida.write('id')
#             else:    
#                 saida.write(str(count))
#             
#             saida.write(',')
            
            #self.inv_index_gab[count]= rec[0];   
            rec_id_list = inv_index_gab.get(rec[0].split('-')[0], [])
            
            if len(rec_id_list)>0:
                #print rec[0].split('-')[0]
                rec_id_list.append(rec[0])
                inv_index_gab[rec[0].split('-')[0]] = rec_id_list
                #print 'xxxx '
            else:
                
               # print rec[0].split('-')[0]
                rec_id_list.append(rec[0])
                inv_index_gab[rec[0].split('-')[0]] = rec_id_list
            
            saida.write(",".join(rec))
           # join=rec[0]+", "+rec[6]+", "+rec[7]+", "+rec[8]+", "+rec[9]+", "+rec[14]
           # saida.write(join)
            saida.write('\n')
            count+=1
            
            
            
           # print join
        size_gab=0   
        for inv_list in ind.inv_index_gab.items():
            if(len(inv_list)>1):
                size_gab+=len(inv_list)-1 
           # print inv_list[0]
        print (' TAMANHO GAB %d' % size_gab)
        saida.close()
        return file_out
        

# ===============================================================================================        
        
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
        
        #if (file_name.lower().endswith('.csv')):
            #pass  
        #else:
            #print '\t Only (csv) file format is supported' 
            #sys.exit()
    
      
        # Get number of lines of the file   
        num_lines = self.getLineNumber(file_name)-1
         
         
         ##############################################
        file_name=self.formatFile(file_name) 
        
        # Calculate the number of records that should be in the build 
        # dictionary based on the percentage provided by user
        build_records_count = int(round(num_lines *
                                            float(build_percentage)/ 100))
            
            
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
                    
                   
            # Break the data into build records, and query records
            # based on the previously calculated number of build_records 
            if this_line_num < build_records_count:
                    
                # Add the record to build dictionary 
                build_records[rec_id] = clean_rec[1:]
                    
                # Group the records that have the same entity_id when 
                # loading records from the dataset file and save them 
                # in the variable named 'entity_records. 
                # i.e {'ent-id':[rec_id_1,rec_id_2,...]}. 
                # this variable is used for the purpose of calculating 
                # accuracy. 
                ent_id = clean_rec[1]
                ent_rec_list = entity_records.get(ent_id, [])
                ent_rec_list.append(rec_id)
                entity_records[ent_id] = ent_rec_list

            else:
                # add the record to the query dict
                query_records[rec_id] = clean_rec[1:]
            this_line_num += 1

        print('\t Loaded file:                {0}'.format(file_name))
       
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
        
    def Insert_value(self,rec_id,rec_val,i):
        ''' Inserts a record value to the inverted indexes RI, SI, and BI
        '''
        # Shorthands to make program faster
        inv_index = self.inv_index  
        sim_dict = self.sim_dict
        block_dict = self.block_dict
        min_thres = self.min_thres
        enco_methods = self.enco_methods
        comp_methods = self.comp_methods
        
        rec_val_ind = '%s' % (rec_val)     # Add attribute qualifier for the
                                                # inverted index values
    
        # Insert the record value with qualifier into the inverted index
        
        rec_id_list = inv_index.get(rec_val_ind, [])
        this_rec_id = (rec_id)    # this is a set of -->(rec id, entity id)
        rec_id_list.append(this_rec_id)
        
        inv_index[rec_val_ind] = rec_id_list
        
       
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
        
                             
        ent_id = rec_id
       
        query_sort= self.resort_record(query_rec)  
        #print "rec_values %s" % query_rec[3]
        
        # Process all attribute values started from 1 since the first
        # attribute is the query record is the entity id 
        
        rec_id_list=[]
        i=0
        for rec_val,v in query_sort.items():     
#             if(i > num_compared_attr/2):
#                break;
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
                self.Insert_value(rec_id,rec_val,i)
               
            else:
                             
                # Add the record id into the inverted index
                temp_list = inv_index.get(rec_val_ind, [])
               
                
                #print 'indice len %d %s' % (len(inv_index), rec_val)
                temp_list.append((rec_id))
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
       
       ###################################################
       
    def create_output_file(self, ent_id,res_list,f):
         
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
                   
                   
                    valueA=ind.query_records[ent_id]
                    valueB=ind.query_records[res_list[i]]
                    dictionary={}
                    sum=0.0
                    for j in range(self.total_num_attr):
                        temp=ind.comp_methods[1](valueA[j], valueB[j])
                        dictionary[j]=temp
                        #f.write(str(temp) + ", ")
                        sum=temp+sum
                       #((stringcmp.editdist(valueA[j], valueB[j])))
                    #if(sum/len(valueA)>0.1):
                    list_of_dict_.append(dictionary)          
                    #else:
                    #    continue    
                   
                   # print ("ent -> %s %s " % (ent_id,res_list[i]))
                   
                    if(("dup") not in ent_id and  ("dup") not in res_list[i]):
                    #    print "false match 1"
                        query_acc_res.append('FM')
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
                            gab_list=ind.inv_index_gab.get(res_clean,[])
                            
                            if(dirty in gab_list or res_list[i] in gab_list):                             
                                if(("dup") not in ent_id):
                                    label.append(res_list[i])                            
                                else:
                                    label.append(dirty)                            
                                #gab_list.remove(dirty)
                                #query_acc_res.append('TM')
                                #ind.inv_index_gab[dirty]=gab_list
                        #        f.write("1")
                                gabarito.append(1) 
                            else:
                                if(("dup") not in ent_id):
                                    label.append(res_list[i])                            
                                else:
                                    label.append(dirty)                            
                                gabarito.append(0) 
                        else:
                            label.append(-1)
                            query_acc_res.append('FM')
                         #   f.write("0")
                            gabarito.append(0);
                            
                    #f.write("\n")
                   
         assert (len(gabarito)==len(label)), "problem %s %s %s %s" %(ent_id,res_list, gabarito, label)                   
         #print ("problem %s %s %s %i %s" % (ent_id,res_list, gabarito, len(list_of_dict_), label))
         return (gabarito, list_of_dict_,label)
       
    def header(self,file):
        #file_out="/tmp/final_treina.arff"
        f = open(file, 'w')
        f.write("@relation TrainingInstances\n")
        for i in range(0,5):
            f.write("@attribute att"+str(i) +" numeric\n")
        f.write("@ATTRIBUTE class {0,1}\n @DATA\n")
        f.flush();
        f.close();
        
        
        
        
    ##############encontrar bug aqui!!!!!!!!!!!!!!!!!!!!!!!!!
    def allac (self, file, flag):
        self.count+=100;
        if(flag==1):
            os.system("cd ssarp &&  rm train-B5-* ")
            os.system("cd ssarp &&  ./gera_bins_TUBE.sh "+ file +"  5")
            os.system("cd ssarp && ./discretize_TUBE.pl train-B5 "+file+ "  5 lac_train_TUBEfinal.txt 1")
#             os.system("cd ssarp && ./updateRows.pl lac_train_TUBEfinal.txt lac_train_TUBEfinal_rows.txt " + str(self.count))
#             os.system("cd ssarp && rm alac_lac_train_TUBEfinal_rows.txt")
#             os.system("cd ssarp && ./run_alac_repeated.sh lac_train_TUBEfinal_rows.txt 1")
#             os.system("cd ssarp && ./desUpdateRows.pl alac_lac_train_TUBEfinal_rows.txt alac_lac_train_TUBEfinal.txt " + str(self.count))
#             os.system("cd ssarp && cat alac_lac_train_TUBEfinal.txt | awk '{ print $1 }'  | while read instance; do  sed  -n  \"$instance\"p  " + file+"; done >> /tmp/final_treina.arff;")
        else:
            #os.system("cd ssarp &&  rm train-B16-* && ./gera_bins_TUBE.sh "+ file +"  16")
            #os.system("cd ssarp && ./discretize_TUBE.pl train-B16 "+file+ "  16 lac_train_TUBEfinal.txt 1")
            #os.system("cd ssarp && ./updateRows.pl lac_train_TUBEfinal.txt  lac_train_TUBEfinal_rows.txt  " + str(self.count))
            
            #os.system("cd ssarp && ./run_alac_repeated.sh lac_train_TUBEfinal_rows.txt 1")
            #os.system("cd ssarp && ./desUpdateRows.pl alac_lac_train_TUBEfinal_rows.txt alac_lac_train_TUBEfinal.txt " + str(self.count))
            #os.system("cd ssarp && cat alac_lac_train_TUBEfinal.txt | awk '{ print $1 }'  | while read instance; do  sed  -n  \"$instance\"p  " + file+"; done >> /tmp/final_treina.arff;")
            #os.system("cd ssarp && wc -l alac_lac_train_TUBEfinal.txt")  
            print ("erro ")
        #os.system("cd ssarp && cat "+file+" > /tmp/temp " )
        
        
        
    def arfftoSVM(self, inputfilename,outfile):
        print ("gerando arquivo svm")
        fin = open(inputfilename,'r')
        lines = fin.readlines()
        #fin.close()
        outputfilename = outfile
        fout = open(outputfilename,'w')
        
        beginToRead = False
        for line in lines:
            flag =0
            if beginToRead == True:
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
                   # print(resultLine)
                    fout.write(resultLine+"\n")

            if line[0:6] == ' @DATA' or len([pos for pos, char in enumerate(line) if char == ','])>5:
                beginToRead = True

        fout.close()
        
        
        
        
    def train_svm(self,svm_file, pairs, gabarito):
  
        #os.system("export PYTHONPATH=//home/guilherme/git/testing_blocking/libsvm/tools/:$PYTHONPATH")
        #y, x = svm_read_problem(svm_file)
        
        #rate, param = find_parameters(svm_file, '-log2c -1,1,1 -log2g -1,1,1 -gnuplot null')
        #print ("xxxxxxxxxxxxxxxxxx %s %s" % (param.get('c'),(param.get('g'))))
        #p='-c '+ str(param.get('c')) +' -g ' + str(param.get('g'))
        gabarito=[float(i) for i in gabarito]
        print ("treinamento  %i " % ( len(pairs)))
        print ("gabarito  %i" % (len(gabarito)))
       
        m = svm_train(gabarito, pairs, '-c 4') 
        return m         
         
    def test_svm(self, model, file_full):  
        y, x = svm_read_problem(file_full)
        
       # x0, max_idx = gen_svm_nodearray({1:1, 3:1})
        _labs, p_acc, p_vals = svm_predict(y, x, model)
      
        
        for i in range(len(y)):
            if(y[i] != _labs[i]):
                self.false_positive+=1;
            else:
                self.true_positive+=1;
        
    def test_svm_online(self, model, y, x, gabarito ):  
        #y, x = svm_read_problem(file_full)
        print ("labellll-> " +str(y))
       # x0, max_idx = gen_svm_nodearray({1:1, 3:1})
        _labs, p_acc, p_vals = svm_predict(y, x, model )
        #print _labs
        for i in range(len(y)):
            self.compute+=1;
            #true positive
            if( _labs[i]==1 and y[i]==1):
                self.true_positive+=1;
                print ("------------------------------------------------------------true positive pair " +str(x))                
                #remove do gabarito as tags reais 
                for x in (gabarito):
                    if(x!=-1):
                        try:
                            res_clean=x.split("-")[0]  
                            
                            gab_list=ind.inv_index_gab.get(res_clean,[])
                            #print "gab_list %s" % gab_list
                            #print "remove  %s" % x
                            gab_list.remove(x)
                            ind.inv_index_gab[res_clean]=gab_list
                            #print "gab_list %s" % gab_list
                        except ValueError:
                            print ("element not exists")
            #false positive
            if(_labs[i] ==1 and y[i]==0):
                self.false_positive+=1;
            #false negative 
            if(_labs[i] ==0 and y[i]==1):
                self.false_negative +=1;
            if(_labs[i] ==0 and y[i]==0):
                self.true_negative +=1;    
    
    
    def load_struct_active(self,list_of_pairs,gabarito):
        
        
        global line_number;
        
        
        
        
        #save dict to file arff
                     
        ###load discretized file
        list_of_pairs_discrete=[]
        gabarito_d=[]
        id=[]
        for line in list_of_pairs:
            dict ={}
            for k,v in line.items():
                  dict[k]=str(int(v*10))
                  if(v==1.0):
                      dict[k]='k'
            list_of_pairs_discrete.append(dict);
#         for ele in gabarito:
#             gabarito_d.append(str(ele))
#             line_number+=1
#             id.append(line_number)
              
#         os.system("cd ssarp && ./discretize_TUBE.pl train-B5 /tmp/arff_out  5 lac_train_TUBEfinal.txt 1")
#         
#         lines=0
#         f = open("ssarp/lac_train_TUBEfinal.txt", 'r',100)
#         list_of_pairs_discrete=[]
#         gabarito=[]
#         id=[]
#         for line in f:
#             splitted=line.strip().split(" ")
#             dict={}
#             
#             for i in range(len(splitted)-2):
#                  if(i==1):
#                      gabarito.append(splitted[i].split("=")[1])
#                      id.append(splitted[0])
#                  dict[i]= (splitted[i+2].split("="))[1]
#                     
#             list_of_pairs_discrete.append(dict)
#             lines+=1
#         print ("lista of pairs %i %i", (len(list_of_pairs), len(list_of_pairs_discrete)))
        #assert (len(list_of_pairs_discrete)==lines),"problema com tamanho da struct"
        
        
        #print list_of_pairs
       # print gabarito   
        return list_of_pairs_discrete,id 
    
    def active_select_first_pair(self,list_of_pairs, list_of_pairs_discrete,gabarito, collumn_frequency,training_set,training_gabarito,training_set_gabarito):
        
            matrix = np.zeros((len(list_of_pairs_discrete),len(list_of_pairs_discrete[0])))   #[[0 for x in range(len(list_of_pairs))] for y in range(59)]
            
            for i in range(len(list_of_pairs_discrete)):
                for j in range(len(list_of_pairs_discrete[i])):
                    matrix[i][j] = collumn_frequency[j][list_of_pairs_discrete[i][j]]
            value = []        
            for i in range(len(list_of_pairs_discrete)):
                value.append(sum(matrix[i]));
    
            print ("total de valores por linha %s" % value)
            
            
            count_value = [0] * len(list_of_pairs_discrete)
           # top_values= sorted(range(len(value)), key=lambda i: value[i], reverse=True)[:2] #get the top values positions
            top_values = sorted(enumerate(value), key=lambda x: x[1], reverse=True)                       
            print ("top  valores %s " % top_values)
            
            memory = top_values[0];
            for tuple in top_values:
                if(memory[1] == tuple[1]):
                    memory = tuple
            print ("tuple final %s" % memory[0])
            print (list_of_pairs_discrete)
    
            end = time.time()        
           # print("time to select first element %f " % (end - start))
        
            stored_ids.append(memory[0])
            training_set = []        
            training_set.append (list_of_pairs_discrete[memory[0]])                      
            training_set_gabarito.append(gabarito[memory[0]])           
            
            self.training_set_final.append(list_of_pairs[memory[0]])
            self.gabarito_set_final.append(gabarito[memory[0]])
            training_gabarito.append(gabarito[memory[0]])
            # add a positive pair
            self.first_time_active = 0
            
            # add a  positive pair 
            temp_ele = {}
            temp_ele_d = {}
            for i in range (len(list_of_pairs[memory[0]])):
                temp_ele[i] = 0.9
                temp_ele_d[i] = "9"
            self.training_set_final.append(temp_ele)
            self.gabarito_set_final.append(1)
            
            training_set.append(temp_ele_d)
            training_set_gabarito.append('1')
            training_gabarito.append("1")
            stored_ids.append("-1")

            return training_set, training_gabarito ,stored_ids 
    
    
    def active_learning(self, list_of_pairs, gabarito,training_set,training_gabarito,stored_ids):
        
        global n_rule
        #e preciso mapear o atributos continuos para valores discreto 
        #   list_of_pairs--> list_of_pairs_discreto
        #
        
        list_of_pairs_discrete,  id= self.load_struct_active(list_of_pairs,gabarito)
        
        
        print("pares a serem processador %i %i " % (len(list_of_pairs), len(list_of_pairs_discrete)))
        
            
            
            
#         if(self.first_time_active==0):      
#             stored_ids=[]
#             for i in range(len(training_set)):
#                 stored_ids.append(str(i))
        
        
        
       
        #encontrar a primeira linha
        collumn_frequency=[]; 
        training_set_gabarito=[]   
        temp=collections.Counter()
       # max_value=[]
        for j in range(len(list_of_pairs_discrete[0])): # para cada coluna fazer a varedura
            for i in range(len(list_of_pairs_discrete)): # varrear as linhas 
                temp[list_of_pairs_discrete[i][j]]+=1
            collumn_frequency.append(temp)            
            temp= collections.Counter()    
       
        if(self.first_time_active==1):      
           training_set, training_gabarito ,stored_ids =self.active_select_first_pair(list_of_pairs,list_of_pairs_discrete,gabarito, collumn_frequency,training_set,training_gabarito,training_set_gabarito)
           self.first_time_active=0
           
       # print "top value %s "% sorted(range(len(count_value)), key=lambda i: count_value[i], reverse=True)[:1]
        
        #encontra o resto 
        
        while(1):
            contador=0
            start = time.time()   
            lowest_rule=sys.maxsize
            lowest_id=0
            for j in range(len(list_of_pairs_discrete)):
                join_pairs=' '.join('{}'.format(value) for key, value in list_of_pairs_discrete[j].items())
                teste_soma=0                
                for i in range(len(training_set)):
                    join_gab=' '.join('{}'.format(value) for key,value in training_set[i].items())
                   # print ((sum(1 for a, b in zip(join_pairs, join_gab) if a == b)))
                    teste_soma+=(2**(sum(1 for a, b in zip(join_pairs, join_gab) if a == b)-3))-1
                    
                    #print (str(j)+ "---string ---" + str(join_pairs)+"---"+str(join_gab)+"---"+str(teste_soma))
                if(teste_soma<=lowest_rule):
                    lowest_rule=teste_soma
                    lowest_id=j
                print ("summm _> "+str(lowest_id) +"   "+str(lowest_rule))    
                
            
            
            if(lowest_id not in stored_ids):
                n_rule=[0]*len(n_rule)
                stored_ids.append(lowest_id)               
                training_set.append(list_of_pairs_discrete[lowest_id])
                training_set_gabarito.append(gabarito[lowest_id])  
                training_gabarito.append(gabarito[lowest_id])
                self.training_set_final.append(list_of_pairs[lowest_id])
                self.gabarito_set_final.append(gabarito[lowest_id])   
                print ("************************novo training set size %i " % len(self.training_set_final))
                print ("**********************************")
                end = time.time()      
                print("time to select %f" %(end - start))
                
            else:
                print ("convergiu com a linha %i" % lowest_id)
                print ("tamanho do treinamento %i " % len(training_set))
                print ("Gabarito do treinamento %s" % self.gabarito_set_final)
                break    
            
            
                     
#             start = time.time()
#             for pair in list_of_pairs_discrete:
#                 
#                 if(n_rule[contador]!=0):
#                     contador+=1
#                     continue
#                 
#                 projection=copy.deepcopy(training_set);
#                 for line in range(len(training_set)):
#                     for ele in range(len(pair)):
#                         if(training_set[line][ele]!=pair[ele]):
#                             projection[line][ele]=""
#                 #print ("projetion %s " % projection)       
#                 #fim da criacao da projecao
#                 #print (projection)
#                 
#                 rules=set()
#                 id_projection=0
#                 
#                 for pair in projection:
#                     
#                     for i in range(len(pair)): #criando uma regra
#                         if(pair[i]!=""):
#                             rules.add(str(i)+"-"+(pair[i])+"->"+str(training_gabarito[id_projection]))
#                     for i in range(len(pair)-1):   #criando duas regras 
#                         for j in range(i+1, len(pair)):
#                             if(pair[i]!="" and pair[j]!=""):
#                                rules.add(str(i)+"-"+(pair[i]) +"#"+str(j)+"-"+(pair[j])+"->"+str(training_gabarito[id_projection]))    
#                         
#                     id_projection+=1;
#                 
#                 n_rule[contador]=len(rules)                
#                 contador+=1
#                 
#            # endB = time.time()        
#            # print("            time to create rules %f  regras %i " % ((endB - end), len(training_set)))
#             print ("numero de rules  " +str(n_rule))
#             sorted_list = sorted(enumerate(n_rule), key=lambda x: x[1])
#             memory=sorted_list[0];
#             equal_elements=[memory[0]]
#             for tuple in sorted_list[1:]:
#                 if(memory[1]==tuple[1]):
#                     memory=tuple
#                     equal_elements.append(tuple[0])
#                 else:
#                     break;
#             print ("elementos iguais %i " % len(equal_elements))    
#             #frequencia colunar 
#             matrix_frequency=collections.Counter()
#             
#             if(len(equal_elements)>1):  #tem mais  de um elemento
#                 for i in (equal_elements): #lista de elementos
#                     for j in range(0,len(list_of_pairs_discrete[0])):
#                         matrix_frequency[i]+=  collumn_frequency[j][list_of_pairs_discrete[i][j]]
# #                 
#                 candidate=sorted(enumerate(matrix_frequency), key=lambda x: x[1])
#                 memory=candidate[0]
#                 for i in range(len(candidate)):
#                     if(memory[1]==candidate[i][1]):
#                         memory=candidate[i]
#                     else:
#                         break;
# #                 print 
#                 candidate_final=equal_elements[memory[0]]    
#                # print ("memory %s  %s   ---> %s" % (matrix_frequency, equal_elements, candidate_final))   
#                 #print "matrix de frequencia %s" % sorted(enumerate(matrix_frequency), key=lambda x: x[1], reverse=True)
#             else:
#                 candidate_final=equal_elements[0]
#             end2 = time.time()        
#            # print("            time to compute de rules %f  regras %i " % ((end2 - end), len(training_set)))   
#             print (" candidate final \n\n" + str(list_of_pairs_discrete[candidate_final]) + "   ---- "+ str(candidate_final))              
#             #actual_line =    list_of_pairs[memory[0]]
#             if(candidate_final not in stored_ids):
#                 n_rule=[0]*len(n_rule)
#                 stored_ids.append(candidate_final)               
#                 training_set.append(list_of_pairs_discrete[candidate_final])
#                 training_set_gabarito.append(gabarito[candidate_final])  
#                 training_gabarito.append(gabarito[candidate_final])
#                 self.training_set_final.append(list_of_pairs[candidate_final])
#                 self.gabarito_set_final.append(gabarito[candidate_final])   
#                 if(gabarito[candidate_final]==1):
#                     print ("************************novo training set size %i " % len(self.training_set_final))
#                     print ("**********************************")
#                 end = time.time()        
#                 print("time to select %f" %(end - start))
#                 
#             else:
#                 print ("convergiu com a linha %i" % contador)
#                 print ("tamanho do treinamento %i " % len(training_set))
#                 print ("Gabarito do treinamento %s" % self.gabarito_set_final)
#                 break    
                               
         
                
        
        
                
        return training_set, training_gabarito ,stored_ids           
# ============================================================================




# Define special functions for post code encoding and comparison
# Any other function can be used 
def __get_substr__(s):  
    # Function used for post code blocking
    # Returns last three digits of post code
    return s[1:]  
    
     
    
        
       
        
        
        
        

def __postcode_cmp__(s1, s2): 
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
    
#=============================================================================
    

if __name__ == '__main__':
    
    total_num_attr = 4  # Total number of attribute 
                        # including rec-id, and ent-id
    min_threshold = float(sys.argv[2])          # Minimal similarity threshold
    min_total_threshold = float(sys.argv[3])    # Minimal total threshold
    build_percentage = float(sys.argv[4])       # Percentage of records used to
                                                # build the index
    file_name = sys.argv[5]             # optimization flag
    arff_file="/tmp/final_treina.arff"
    svm_file="/tmp/final_treina.svm"
    svm_file_full="/tmp/svm_full.svm"
    
    index_name = 'Active Online Blocking'
    line_number=0
    # Define encoding and comparison methods to be used for attributes
    # Note: first element in the list should always be None. 
    enco_methods = [None, encode.dmetaphone, encode.dmetaphone, 
                    encode.dmetaphone, __get_substr__,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,]
    comp_methods = [None, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist , stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist, stringcmp.editdist]
    
    ind = ActiveOnlineBlocking(total_num_attr,enco_methods, comp_methods, 
                  min_threshold, min_total_threshold)
     
    
    print
    print('Testing method: {0}'.format(index_name))
    print('================' + '=' * len(index_name))
    print       
    
    start_time = time.time()  # Load data set from file(s)
    ind.load(file_name,build_percentage)
    load_time = time.time() - start_time
    
    print(' Loading time: %.1f sec' % (load_time))
    
    # Getting memory usage does not work in windows
    #load_memo_str = auxiliary.get_memory_usage()
    #print ('    ', load_memo_str)
    #print  
    ##
    file="/tmp/arff_out"
   
   
    # Match query records - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    query_time_res = []  # Collect results for each of query record
    query_acc_res = []
    num_comp_res = []
    
    query_cnt = 1
    num_rec = 0
    print (' Processing Query records ...')
   
    # Go through query records and try to find a match for each query 
    tuples_count=0
    count = 0 # count of true duplicates 
    flag=1;
    set_gabarito=[]
    list_of_dict=[]
    training_set_discreto=[]
    training_gabarito_discreto=[]
    set_list_of_pairs=[]
    set_list_of_pairs_to_process=[]
    set_gabarito_to_process=[]
    list_of_pais_selection=[]
    set_label=[]
    set_label_to_process=[]
    n_rule=[]       
    stored_ids=[];
    f = open(file, 'w',100)
    for rec_id, clean_rec in ind.query_records.items():        
        ent_id = rec_id
        start_time = time.time()
        res_list, num_comp = ind.query(rec_id,clean_rec)
        query_time = time.time() - start_time
       # print "query %s pairs %s" % (rec_id, res_list)
        
        num_rec += 1
        if (num_rec % 100 == 0):
            print ('\t Processed %d records in the query phase' % (num_rec))
            #print "inverted inde size %i" % ((ind.count))
            
        query_time_res.append(query_time)
        num_comp_res.append(num_comp)
            
        tuples_count+=len(res_list);
        #gera arquivo de saida para avaliacao da tupla
        
        #evitar que registros nao formaram pares sejam processados
        print ("file size ---->  %i " % len(res_list) )
        gabarito, list_of_pairs, label = ind.create_output_file(ent_id, res_list,f)
       
        #ind.header(arff_file)       
        #test active active_learning
        #if( ind.active_learning(list_of_pairs_,gabarito)==1):
        #    break  
        if(len(list_of_pairs)==0):
            continue;
                    
        set_gabarito=set_gabarito+gabarito
        set_list_of_pairs=set_list_of_pairs+list_of_pairs
        set_list_of_pairs_to_process=set_list_of_pairs_to_process+list_of_pairs
        set_gabarito_to_process=set_gabarito_to_process+gabarito
        set_label=label+set_label
        set_label_to_process=set_label_to_process+label
        n_rule=n_rule+[0]*len(gabarito)
        count+=len(list_of_pairs)
        if(count>10 ):
             
             count=0 
             print ("numero de pares a serem processados %i" % (len(set_list_of_pairs)))
#              f.flush()             
             print ("\n ############################starting active  \n\n")             
             training_set_discreto, training_gabarito_discreto, stored_ids= ind.active_learning(set_list_of_pairs,set_gabarito,training_set_discreto, training_gabarito_discreto,stored_ids)
            # set_list_of_pairs=ind.training_set_final
            # set_gabarito=ind.gabarito_set_final
             n_rule=[0]*len(set_gabarito)
             
             print ("\n ############################starting training \n\n")
             model= ind.train_svm(svm_file,ind.training_set_final, ind.gabarito_set_final)  
               # break
            # flag=0;   
             
             #tuples_count=0                                   
            # if(len(list_of_pairs)>0):
             print ("\n #############################starting testing \n\n")
             ind.test_svm_online(model,set_gabarito_to_process, set_list_of_pairs_to_process, set_label_to_process); 
             set_list_of_pairs_to_process=[]
             set_gabarito_to_process=[]
             set_label_to_process=[]
             #set_gabarito=[]
             #set_list_of_pairs=[]
             #set_label=[]
             
             #ind.arfftoSVM(file, svm_file_full);
             #ind.test_svm(model,svm_file_full); 
             #print "list of pairs %s" % list_of_pairs_
             
             
             #p_label, p_acc, p_val = svm_predict(gabarito, list_of_dict_, model)
             #print p_label
             #f.close
             #open(file, 'w').close()
             #f = open(file, 'w',100)
            # time.sleep(10)
       
     #############################################################     
    if(len(set_gabarito_to_process)>0):
        ind.test_svm_online(model,set_gabarito_to_process, set_list_of_pairs_to_process, set_label_to_process);     
    print ("####################")
    print ("false positive %i" % ind.false_positive)
    print ("true positive %i" % ind.true_positive)
    print ("false_negative %i" % ind.false_negative)
    print ("true_negative %i" % ind.true_negative)
    print ("full size %i" % ind.compute)
    
      
       
    size_gab=0   
    for inv_list in ind.inv_index_gab.values():
        if(len(inv_list)>1  ):
            size_gab+=len(inv_list)-1
            print ("%s %d " % (inv_list[0],len(inv_list)))
            for i in range(len(inv_list)):
                print ("\n\ngab %s" % inv_list[i])
    print (' TAMANHO GAB %d' % size_gab)

      
    # Summarise query results - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    num_tm = query_acc_res.count('TM')
    num_fm = query_acc_res.count('FM')
    #assert num_tm + num_fm == len(ind.query_records)
    print
    print (' Query summary results for index: %s' % (index_name))
    print ('-' * (33 + len(index_name)))
    
    print ('  minimum threshold: %.2f;' % \
              ( min_threshold) + ' minimum total threshold: %.2f' % \
              (min_total_threshold))
    #if ind.count > 0:
        #print '  Matching accuracy: %d/%d true matches (%.2f%%)' % \
              #(num_tm, ind.count, 100.0 * num_tm / ind.count) 
    #else:
        #print' No duplicates where found' 
    if num_tm>0 :    
        print (' precisao %f  revo %f' %  ((100.0*num_tm/(num_tm+num_fm)),(100.0*num_tm/(size_gab+num_tm))))
        print (' true pos %d  false posit %d' %  (num_tm, num_fm))
    else:
        print ('true matching equal zero')
        
   
  
   


