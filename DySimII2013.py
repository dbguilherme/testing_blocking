'''
  
        
        
    To run the code, type:
              python ANOB2013.py t 0.75 2.5 50 
              where:
                    t (optimisation option) leave it always as t
                    0.75 (minimum threshold) this threshold is used to compare single attribute values
                                             for example compare the first name of two records
                                             if sim('smith','smyth')>0.75 then attribute value is 
                                             considered to be similar 
                    2.5 (overall threshold)  this threshold  is used in comparing two records.
                                             for example to compare record1, and record2 that have 4 
                                             attributes (first name, surname, suburb, post code)
                                             the value 2.5 means that : when more than 2 attributes out of 
                                             the four attributes are similar the two records are considered
                                             as a match 
                                             i.e. if sim(record1, record2) > 2.5 then the records 
                                             are considered as a match.  
                                             
                    50(build size)           the percentage of the size of the build records used from the 
                                             data set to build the index.
                               

'''

import string
import sys
import time
import re


# From Febrl  http://sourceforge.net/projects/febrl/
import auxiliary  
import encode
import stringcmp
import random


class ANOB:
    def __init__(self, total_num_attr, encoding_methods, comparison_methods, 
                 min_threshold, min_total_threshold):
        """
        Constructor. Initialize an index, set common parameters.
            
        Arguments:
        - total_num_attr: the total number of attributes for a record including 
                        rec-id and ent-id.
        - encoding_methods: A list with (phonetic) encoding methods, one per
                            attribute in the data set (thus, this list needs
                            to be of length equal to the number of attributes
                            in the data set used.
        - comparison_methods: A similarity list with one comparison method per
                              attribute.
        - min_threshold: Minimum similarity threshold for a comparison, if
                         below then a comparison result will not be stored.
        - min_total_threshold: Minimum total similarity threshold for all
                               comparisons of two records, can be used to 
                               remove potential matches in an index.
        """
        
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
                                
        self.inv_index_gab = {}                                
        
        self.count = 0          # The number of true duplicates in the data set
         
        # Number of attributes in the data set without the rec_id field                            
        self.num_attr_without_rec_id = self.total_num_attr -1   
        
        # Number of actual attributes in the data set 
        # i.e. without the rec-id and ent-id
        self.num_compared_attr = self.total_num_attr - 2  

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
        for inv_list in ind.inv_index_gab.itervalues():
            if(len(inv_list)>1):
                size_gab+=len(inv_list)-1 
           # print inv_list[0]
        print ' TAMANHO GAB %d' % size_gab
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
        
        
        print ' Loading data file...'
        
        #if (file_name.lower().endswith('.csv')):
            #pass  
        #else:
            #print '\t Only (csv) file format is supported' 
            #sys.exit()
    
      
        # Get number of lines of the file   
        num_lines = self.getLineNumber(file_name)-1
         
         
         ##############################################
        file_name=self.formatFile(file_name) 
        
        print num_lines    
        # Calculate the number of records that should be in the build 
        # dictionary based on the percentage provided by user
        build_records_count = int(round(num_lines *
                                            float(build_percentage)/ 100))
            
            
        in_file = open(file_name)   
        
        
        # Skip over header line
        self.header_line = in_file.readline()  
            
        this_line_num = 0
        for rec in in_file:
            rec = rec.lower().strip()
            rec = rec.split(',')
                
            # Clean the record and remove all surrounding white-spaces
            clean_rec = map(string.strip, rec) 
            
            #Mmake sure that each record has the same number of attributes
            # which is equal to total_num_attr                    
           # assert len(clean_rec) == total_num_attr, (rec, clean_rec)
            
            # Get the record id of the record
            rec_id = clean_rec[0].strip()
            
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
        
            
# ===============================================================================================        

    def build(self):
        """Build a similarity aware inverted index using the data set in memory.
        """
    
        inv_index = self.inv_index  # Shorthands to make program faster
        sim_dict = self.sim_dict
        block_dict = self.block_dict
        build_records = self.build_records
        num_attr_without_rec_id = self.num_attr_without_rec_id
          
       
        num_rec = 0 # counter to be used to check the number of processed records
        for (rec_id, rec_values) in build_records.iteritems():
            # note: rec_values is the list of all attributes including ent-id
            # i.e [ent-id,attr-1,...,attr-n]
            
            # Process all attributes in the rec_values but not
            # including the first element as it is the ent-id           
            for i in range(1,num_attr_without_rec_id):   
                rec_val = rec_values[i]
                ent_id = rec_values[0]
               # if(rec_val == '' or rec_val == 'norole' or len(rec_val)<2):
                #    continue
                if(rec_val == 'norole' ):
                    continue
                self.Insert_value(rec_id,ent_id, rec_val, i)
                #print '%s %s %s ' % (rec_id, ent_id, rec_val)
            num_rec += 1
          
            if (num_rec % 100 == 0):
                print '\t Processed %d records in the build phase' % (num_rec)        
        
     
        
        max_inv_list_len = 0
        sum_inv_list_len = 0
        
        for inv_list in inv_index.itervalues():
            max_inv_list_len = max(max_inv_list_len, len(inv_list))
            sum_inv_list_len += len(inv_list)
        print '\t Number of unique record values (inverted index keys):  %d' % \
              (len(inv_index))
       
        print '\t    Maximum number of records in an inverted index list: %d' % \
              (max_inv_list_len)
        print '\t    Sum of lengths of all inverted index lists:          %d' % \
              (sum_inv_list_len)
    
        max_sim_dict_len = 0
        sum_sim_dict_len = 0
        for this_sim_dict in sim_dict.itervalues():
            max_sim_dict_len = max(max_sim_dict_len, len(this_sim_dict))
            sum_sim_dict_len += len(this_sim_dict)
        print '\t  Number of unique values in similarity dictionary:   %d' % \
              (len(sim_dict))
        print '\t    Maximum number of records in a similarity set:    %d' % \
              (max_sim_dict_len)
        print '\t    Sum of lengths of all similarity dictionary sets: %d' % \
              (sum_sim_dict_len)
    
        max_block_list_len = 0
        sum_block_list_len = 0
        
        for block_list in block_dict.itervalues():
            max_block_list_len = max(max_block_list_len, len(block_list))
            sum_block_list_len += len(block_list)
        print '\t  Number of unique values in block dictionary:    %d' % \
              (len(block_dict))
        print '\t    Maximum number of records in a block list:    %d' % \
              (max_block_list_len)
        print '\t    Sum of lengths of all block dictionary lists: %d' % \
              (sum_block_list_len)
    
        assert sum_block_list_len == len(sim_dict)
        
        print
        
         
# =============================================================================================== 

    def query(self, rec_id,query_rec, optimise=0):
        """ Query the index with the given record. Returns a list with the record
            identifiers that have the largest similarity value with the query
            record, the number of comparisons performed, and an additional value
            that is index type specific.
    
            It is assumed a data set has been loaded and an index has been built
            previously.
    
            The argument 'optimize' sets certain levels of optimization in the
            query process. Default is 0, i.e. no optimization.
        """
        #print 'staring query phare\n'
        inv_index = self.inv_index  # Shorthands to make program faster
        min_tot_thres = self.min_tot_thres
        num_attr_without_rec_id = self.num_attr_without_rec_id
        sim_dict = self.sim_dict
        entity_records = self.entity_records
        num_compared_attr = self.num_compared_attr
             
        num_rec = 0
        accu = {}           # One combined accumulator with possible matches    
        num_case_one = 0    # Counter for how many of the record attribute
                            # values are already in the index
                            
        num_case_two =0     # Counter for how many of the record attribute
                            # values are not in the index
                            
        case_timings = {1:0.0, 2:0.0}  # Times used for case 1 and case 2
        case_counts = {1:0, 2:0}      # Number of times case 1 and case 2 occured
        
        # Calculate when to switch the accu building phase
        #
        phase_thres = num_compared_attr - min_tot_thres 
        
        # If the entity id of the query is in the entity records list, 
        # then add the number of records that have the same entity id
        # to the counter and add the record id of that 
        # query to the associated entity in the entity list. 
        # this counter is used for measuring recall purposes                                     
        ent_id = rec_id
       
       
#         ent_rec_list.append(rec_id)
       
        
        # Process all attribute values started from 1 since the first
        # attribute is the query record is the entity id 
        
        rec_id_list=[]
        for i in range(0, num_attr_without_rec_id ):     
            
#             if ((optimise == 0) or (i < phase_thres)):
#                 accu_phase = 1  # Accu can grow with new record identifiers being added
#             else:
#                 accu_phase = 2  # No new record identifiers are added (as they would
                                # not reach the minimum threshold)            
            rec_val = query_rec[i]   
            
            
          #  print "     performing att rec_val %s \n" % rec_val
           # if(rec_val == '' or rec_val == 'norole' or len(rec_val)<2):
            if(rec_val == 'norole' or rec_val == ''  or len(rec_val)<2):
                    continue
           # print rec_val
            
            rec_val_ind = '%s' % (rec_val)     # Add attribute type for inverted
                                                    # index values
            
            # Case 1: A new record value, not stored in the inverted index 
            # (Note that in this case the index is updated and the new record value added to
            # the index to speed up future matchings)
            #
            if (rec_val_ind not in inv_index):
                
                # add the value to the inverted index
                num_case_one += 1
                case_counts[1] = case_counts[1] + 1
                start_time = time.time()
                if(rec_val == 'norole' ):
                    continue  
                #print "             insert att into index"
                self.Insert_value(rec_id,rec_val,i)
                #print 'indice len %d %s' % (len(inv_index), rec_val)
            # Case 2: This record value is available in the inverted index
            # in this case the record id will be added to the inverted index (RI)   
            else:
                
#                 num_case_two += 1
#                 case_counts[2] = case_counts[2] + 1
              
                if(self.count> 500 and len(inv_index[rec_val_ind])>self.count*0.8):
                    continue
              
                             
                # Add the record id into the inverted index
                temp_list = inv_index.get(rec_val_ind, [])
               
                
                #print 'indice len %d %s' % (len(inv_index), rec_val)
                temp_list.append((rec_id))
                inv_index[rec_val_ind]= temp_list 
                  
                  
                if(len(inv_index[rec_val_ind])>self.count):
                    self.count=len(inv_index[rec_val_ind])
                    print "xxxxxxx %i %s" % (self.count,rec_val_ind)
                
            
                rec_id_list_temp=inv_index.get(rec_val_ind, [])                 
                if(len(rec_id_list)==0):                    
                    rec_id_list=rec_id_list_temp;
                else:
                    for id in rec_id_list_temp:
                
                        if(id not in rec_id_list):
                            rec_id_list.append(id);
                           # print "xxxxxxxxxxxxxxxxxxxxxxxxXXXXXXXXXXXXXXXx %s" % rec_id_list;
                 
           #     print "             att value alread exists %s" % rec_id_list      
                     
#                     temp_id_list=temp_rec_id_list[i];
#                     if(temp_id_list not in rec_id_list):
#                         if(len(rec_id_list)>0):
#                             #if(len(temp_rec_id_list)>0):
#                           
#                             rec_id_list=rec_id_list+ temp_id_list;
#                             print "no loop %s---- %s ----%s" % (rec_id_list,temp_id_list,rec_val)    
#                         else:
#                             rec_id_list=temp_id_list;
#                             print "sem loop %s---- %s ----%s" % (rec_id_list,temp_id_list,rec_val)    
                            
         
        #print  "rec_id_list %s" % (rec_id_list)                                           
        #sim_rec_id_list = []    # List with record identifiers of the records that
        #for i in range(len(rec_id_list)): 
            #this_rec_id = rec_id_list[i];  
            #if(this_rec_id[0] != str(rec_id)):
                #sim_rec = this_rec_id
                #sim_rec_id_list.append(sim_rec)      # Similarity value
        
        
        # Similarity aware inverted index specific information: The number of case
        # one (available in the inverted index) of the four query record values
        #
        spec_info = (num_case_two, case_timings, case_counts)
        
        return (rec_id_list, 0, spec_info)    

        
        
        
        ###########################################
      
def remove_query(self, rec_id,query_rec, optimise=0):
    
    
     inv_index = self.inv_index  # Shorthands to make program faster
        
     num_attr_without_rec_id = self.num_attr_without_rec_id
     
     entity_records = self.entity_records
     num_compared_attr = self.num_compared_attr
        
     rec_id_list=[]
     for i in range(0, num_attr_without_rec_id ):     
            
#             if ((optimise == 0) or (i < phase_thres)):
#                 accu_phase = 1  # Accu can grow with new record identifiers being added
#             else:
#                 accu_phase = 2  # No new record identifiers are added (as they would
                                # not reach the minimum threshold)            
           rec_val = query_rec[i]   
            
            
          #  print "     performing att rec_val %s \n" % rec_val
           # if(rec_val == '' or rec_val == 'norole' or len(rec_val)<2):
           if(rec_val == 'norole' or rec_val == ''  or len(rec_val)<3):
               continue
           # print rec_val
            
           rec_val_ind = '%s' % (rec_val)     # Add attribute type for inverted
                                                    # index values
            
          
    
    
      
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
    
    
    
    total_num_attr = 17  # Total number of attribute 
                        # including rec-id, and ent-id
    
    
    optimise_flag_str = sys.argv[1]             # optimization flag
    min_threshold = float(sys.argv[2])          # Minimal similarity threshold
    min_total_threshold = float(sys.argv[3])    # Minimal total threshold
    build_percentage = float(sys.argv[4])       # Percentage of records used to
                                                # build the index
     
    file_name = sys.argv[5]             # optimization flag
    
    index_name = 'Dynamic Similarity Aware Indexing Technique'
                                
    
    if (optimise_flag_str.lower()[0] == 't'):
        optimise_flag = 1  # Optimisation level to be used in query() method
    else:
        optimise_flag = 0
 
        
    
    
    # Define encoding and comparison methods to be used for attributes
    # Note: first element in the list should always be None. 
    enco_methods = [None, encode.dmetaphone, encode.dmetaphone, 
                    encode.dmetaphone, __get_substr__,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,]
    comp_methods = [None, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro , stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro, stringcmp.jaro]
    
    
    ind = ANOB(total_num_attr,enco_methods, comp_methods, 
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
    load_memo_str = auxiliary.get_memory_usage()
    print '    ', load_memo_str
    print  
          
    
    print(' Building the index is starting ... ')
    start_time = time.time()  # Build the index from data set in memory 
    ind.build()
    build_time = time.time() - start_time
    print('  Finished building the index. ' )
    print '  Building time: %.1f sec' % (build_time)
    build_memo_str = auxiliary.get_memory_usage()
    print '    ', build_memo_str
    print
    
   
    # Match query records - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
  
    
    query_time_res = []  # Collect results for each of query record
    query_acc_res = []
    num_comp_res = []
    
    query_cnt = 1
    
    # Count of record values found in index in querying
    case_two_sum = 0  
    case_timing = {1:0.0, 2:0.0}
    case_counts = {1:0, 2:0}
    
    num_rec = 0
    print ' Processing Query records ...'
    print

    # Go through query records and try to find a match for each query 
    
    count = 0 # count of true duplicates 
    for rec_id, clean_rec in ind.query_records.iteritems():
       
      
        ent_id = rec_id
        
        #print 'PERFOMING RECORD %s \n\n' %   ((rec_id))
        start_time = time.time()
        res_list, num_comp, spec_info = ind.query(rec_id,clean_rec, optimise=optimise_flag)
        query_time = time.time() - start_time
        #print ind.count
        
        num_rec += 1
        if (num_rec % 1000 == 0):
            print '\t Processed %d records in the query phase' % (num_rec)
            print "inverted inde size %i" % ((ind.count))
            
        query_time_res.append(query_time)
        num_comp_res.append(num_comp)
            
        # Process index specific special information returned
        #        
        #case_two_sum += spec_info[0]        
        #if (spec_info[2][1] > 0):  # There were case 1
                #case_timing[1] = case_timing[1] + (spec_info[1][1] / spec_info[2][1])
                #case_counts[1] = case_counts[1] + 1
        #if (spec_info[2][2] > 0):  # There were case 2
                #case_timing[2] = case_timing[2] + (spec_info[1][2] / spec_info[2][2])
                #case_counts[2] = case_counts[2] + 1
    
        
        if (res_list != [] and len(res_list)>1):  # Some results were returned
            
      
            
            # Check if the result list contains the correct matching record 
            # identifier
            #
            #print ind.inv_index_gab 
            for i in range(len(res_list)):
                 try:
                                       
                    if(ent_id==res_list[i]):
                        continue
                     
                    
                    if(("dup") not in ent_id and  ("dup") not in res_list[i]):
                    #    print "false match 1"
                        query_acc_res.append('FM')
                        continue;
                    else:
                        
                        if(("dup") in ent_id and  ("dup") in res_list[i]):
                            continue;
                        
                        
                        #last case:
                        if(("dup") in ent_id):
                            ent_clean=ent_id.split("-")[0]
                            dirty=ent_id
                        else:
                            ent_clean=ent_id
                            #print "ent clean %s" % ent_clean
                        if(("dup") in res_list[i]):
                            res_clean=res_list[i].split("-")[0]
                            dirty=res_list[i]
                        else:
                            res_clean=res_list[i]                        
                        #if("507-" in ent_id):
                        #        print "chegouuuuuuuuuuuuuuuuuuuuuuuuuuuu %s  %s" % (res_clean, res_list );  
                        if(res_clean==ent_clean):
                            
                            gab_list=ind.inv_index_gab.get(res_clean,[])
                            count+=1
                            if(dirty in gab_list or res_list[i] in gab_list):                             
                                
                                gab_list.remove(dirty)
                                query_acc_res.append('TM')
                                ind.inv_index_gab[dirty]=gab_list
                                
                            else:
                                print "XXXXXres clean %s %s" % (res_clean,gab_list)
                        else:
                           # print "false match 2"
                            query_acc_res.append('FM')
                            
                        
                            
                    #    if(
                        
                    #if (ent_id.split('-')[0]== (res_list[i][1]).split('-')[0] ):
                        
                    
#                    
#                    
#                     #if (rec_id in ind.inv_index_gab):
#                    
#                         rec_list=ind.inv_index_gab.get((ent_id.split('-')[0]),[])
#                         
#                         
#                         if(len(rec_list)>0):
#                           #  if(ent_id.__contains__("916-") or res_list[i][1].__contains__("916-")):
#                           #         print "xzzzzzzzzzzzzzzzzzzzzzzzzzzzz %s %s" % (clean_rec, res_list)
#                             if(ent_id.__contains__("dup") and res_list[i][1].__contains__("dup")):
#                           #      print "entrou %s %s %s"    % (res_list[i] , rec_list, ent_id)
#                                 continue;
#                             if((res_list[i][1].__contains__("dup") or ent_id.__contains__("dup"))  ):
#                                 if(ent_id in rec_list and ent_id.__contains__("dup")):
#                                     rec_list.remove((ent_id))
#                                 else:
#                                     if(res_list[i][1] in rec_list and res_list[i][1].__contains__("dup")):
#                                         rec_list.remove((res_list[i][1]))
#                                     else:
#                                         print "erro "    
#                                 query_acc_res.append('TM') 
#                                 
#                                # print "         %s" %rec_list
#                             else:
#                                 print "   ja foi removido %s %s %s %s" % (ent_id, res_list[i][1] ,rec_id , res_list[i][0])    
#                         else:
#                             print 'sffsd %s' % ( (res_list[i][1]))
#                         ind.inv_index_gab[(ent_id.split('-')[0])]=rec_list    
                 except IndexError:
                        print "Oops!  That was no valid number.  Try again... %s %s" % (ent_id,res_list) 
#                    # if(len(rec_list)==0):
#                     #    ind.inv_index_gab.pop(ent_id.split('-')[0])        
#                         #else:
#                         #    print 'rec %s' % rec_list
#                         #    ind.inv_index_gab.pop(ent_id)
#                             
#                          #   ind.inv_index_gab.remove(ent_id)
#                 else:
#                     if (rec_id in ind.inv_index_gab):
#                         query_acc_res.append('FM')                     
        
 ##       query_cnt += 1        
 #   assert (query_cnt - 1) == len(ind.query_records), \
 #              (query_cnt, len(ind.query_records))
        
    query_memo_str = auxiliary.get_memory_usage()
    print "COUNTTTTT %s" % count;    
    size_gab=0   
    for inv_list in ind.inv_index_gab.itervalues():
        if(len(inv_list)>1  ):
            size_gab+=len(inv_list)
           # print "%s %d " % (inv_list[0],len(inv_list))
            #for i in inv_list:
            #    print "\n\ngab %i" % inv_list[i]
    print ' TAMANHO GAB %d' % size_gab

  #  values=[]
    for x in ind.inv_index:
  #      values.append(len(x));
        if(len(ind.inv_index[x])>500):
            print "%s %i " % (x, len(ind.inv_index[x]));
   # values.sort()
    #print ind.inv_index
    
    # Summarise query results - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    num_tm = query_acc_res.count('TM')
    num_fm = query_acc_res.count('FM')
    #assert num_tm + num_fm == len(ind.query_records)
    print
    print ' Query summary results for index: %s' % (index_name)
    print '-' * (33 + len(index_name))
    
    print '  Optimisation: %d; minimum threshold: %.2f;' % \
              (optimise_flag, min_threshold) + ' minimum total threshold: %.2f' % \
              (min_total_threshold)
    #if ind.count > 0:
        #print '  Matching accuracy: %d/%d true matches (%.2f%%)' % \
              #(num_tm, ind.count, 100.0 * num_tm / ind.count) 
    #else:
        #print' No duplicates where found' 
    if num_tm>0 :    
        print ' precisao %f  revo %f' %  ((100.0*num_tm/(num_tm+num_fm)),(100.0*num_tm/(size_gab+num_tm)))
        print ' true pos %d  false posit %d' %  (num_tm, num_fm)
    else:
        print 'true matching equal zero'
        
    print '  Query timing (min / max / avrg): %.3f / %.3f / %.3f sec' % \
              (min(query_time_res), max(query_time_res), \
               sum(query_time_res) / len(ind.query_records))
    print '  Number of comparisons (min / max / avrg): %d / %d / %d' % \
              (min(num_comp_res), max(num_comp_res), \
               int(round(sum(num_comp_res) / len(ind.query_records))))
    print '  %s' % (query_memo_str)
    
    #print '  Average ratio of case 2 : case 1 query matching: %.2f' % \
                #((0.25 * case_two_sum) / len(ind.query_records))
    #if (case_counts[1] != 0):
            #print '    Case 1 average time: %.2f (ms)' % \
                    #(1000.0 * (case_timing[1] / case_counts[1]))
            #print '                 count: {0} (number of all new attributes) '.format(case_counts[1])
    #if (case_counts[2] != 0):
            #print '    Case 2 average time: %.2f (ms)' % \
                    #(1000.0 * (case_timing[2] / case_counts[2]))
            #print '                 count: {0} (number of all attributes that are indexed before)'.format(case_counts[2])
    #print



    
