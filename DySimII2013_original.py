'''
Created on Mar 22, 2013
@author: Banda Ramadan

    This program provides a dynamic inverted index .
    The program first loads a data set that follows the following format:
        rec_id, entity_id, attr1, attr2, ..., attr(n). where rec_id is a 
        unique identifier for records, and entity_id is an identifier for 
        each real-world entity (when two records have the same entity-id
        this means that they both represents the same real-world entity)
        however they both have unique rec_id in the data set.
        
   When loading the data set, the program break the data set into to parts, 
        build records and query records. 
        the build record are used to build the initial 
        index while the query records are used as stream of query records to
        query the built index. Arriving queries are added to index.
             
    
    Things to change in the main section of the program to run the required 
    data set successfully:
        - Total_num_attr: The total number of fields in the data set including 
                           rec-id and ent-id so if we have a data set that have
                           the following fields:
                                rec-id, ent-id, first-name, last-name, 
                                suburb, post-code
                           then the number of attributes should be = 6.
                           
        - file_name: the data set full path and name.
          
        - enco_methods: the list of encoding methods for each of the 
                        attributes in the data set 
        
        - comp_methods: the list of comparison methods for each of the 
                        attributes in the data set.        
        
    
        
        
    To run the code, type:
              python DySimII2013.py t 0.75 2.5 50 
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


# From Febrl  http://sourceforge.net/projects/febrl/
import auxiliary  
import encode
import stringcmp


class DySimII:
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
                                
                                
        self.count = 0          # The number of true duplicates in the data set
         
        # Number of attributes in the data set without the rec_id field                            
        self.num_attr_without_rec_id = self.total_num_attr -1   
        
        # Number of actual attributes in the data set 
        # i.e. without the rec-id and ent-id
        self.num_compared_attr = self.total_num_attr - 2  

# ===============================================================================================        
    
    
    def getLineNumber(self, filename):
        ''' Counts the line numbers of a file
            #it only works on csv '''

        lines = 0
        for line in open(filename):
            lines += 1
        return lines


    def formatFile(self, filename):
        

        count = 0
        #for line in open(filename):
            
        #return lines
        saida=open('teste2.txt', 'w')
        with open(filename) as books:
            lines = books.readlines()
        
        
        
        for rec in lines:
            rec = rec.lower().strip()
            rec = rec.split(',')
            rec[0]= rec[0].replace('rec-','').replace('-org','').replace('-dup-0','')

            if (count == 0):
                saida.write('id')
            else:    
                saida.write(str(count))
            saida.write(',')
            saida.write(",".join(rec))
            saida.write('\n')
            count+=1
            
        saida.close()
        return "teste2.txt"
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
    
      
        file_name = self.formatFile(file_name)
      
  
        # Get number of lines of the file   
        num_lines = self.getLineNumber(file_name)-1
           
            
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
            assert len(clean_rec) == total_num_attr, (rec, clean_rec)
            
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
        
    def Insert_value(self,identifier ,rec_id,rec_val,i):
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
        this_rec_id = (identifier, rec_id)    # this is a set of -->(rec id, entity id)
        rec_id_list.append(this_rec_id)
        
        inv_index[rec_val_ind] = rec_id_list
        
        
        # Check if this record value has already been processed or not (if it
        # has, then nothing needs to be done)
        #
        if (rec_val not in sim_dict):  # A new value, have to process it
            
            # Compute the encoding of this value and add attribute qualifier
            #
          
            this_code = '%s' % (enco_methods[i](rec_val))
            
            # Get the other record values from this attribute in this block
            #
            this_block_list = block_dict.get(this_code, [])
        
            
            # The dictionary to be filled with record values (keys) and
            # similarities (values) of the other records in this block
            #
            this_sim_dict = {}  # Other record values with their similarities
            
            for other_val in this_block_list:
                sim_val = comp_methods[i](rec_val, other_val)
                
                if (sim_val >= min_thres):  # Only if a certain similarity
                    this_sim_dict[other_val] = sim_val
                
                    # Also insert this new record value into the similarity set of
                    # the other record values
                    #
                    other_sim_dict = sim_dict[other_val]
                    other_sim_dict[rec_val] = sim_val
                    sim_dict[other_val] = other_sim_dict
            
            # Add the new similarity set into the similarity dictionary
            #
            sim_dict[rec_val] = this_sim_dict

            # Finally insert this record value into this block and put it back
            #
            this_block_list.append(rec_val)
            
            block_dict[this_code] = this_block_list
            
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
                
                self.Insert_value(rec_id,ent_id, rec_val, i)
               
            num_rec += 1
          
            if (num_rec % 1000 == 0):
                print '\t Processed %d records in the build phase' % (num_rec)        
        
     
        
        max_inv_list_len = 0
        sum_inv_list_len = 0
        print
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

    def query(self, rec_id, query_rec, optimise=0):
        """ Query the index with the given record. Returns a list with the record
            identifiers that have the largest similarity value with the query
            record, the number of comparisons performed, and an additional value
            that is index type specific.
    
            It is assumed a data set has been loaded and an index has been built
            previously.
    
            The argument 'optimize' sets certain levels of optimization in the
            query process. Default is 0, i.e. no optimization.
        """
       
        inv_index = self.inv_index  # Shorthands to make program faster
        min_tot_thres = self.min_tot_thres
        num_attr_without_rec_id = self.num_attr_without_rec_id
        sim_dict = self.sim_dict
        entity_records = self.entity_records
        num_compared_attr = self.num_compared_attr
             
        
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
        ent_id = query_rec[0]
        ent_rec_list = entity_records.get(ent_id, [])
        if ent_rec_list != []:
            self.count += len(ent_rec_list)
        ent_rec_list.append(rec_id)
        entity_records[ent_id] = ent_rec_list
        
        # Process all attribute values started from 1 since the first
        # attribute is the query record is the entity id 
        for i in range(1, num_attr_without_rec_id ):     
            
            if ((optimise == 0) or (i < phase_thres)):
                accu_phase = 1  # Accu can grow with new record identifiers being added
            else:
                accu_phase = 2  # No new record identifiers are added (as they would
                                # not reach the minimum threshold)
                               
            rec_val = query_rec[i]  
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
                
                self.Insert_value(rec_id,query_rec[0],rec_val,i)
                
            # Case 2: This record value is available in the inverted index
            # in this case the record id will be added to the inverted index (RI)   
            else:
                
                num_case_two += 1
                case_counts[2] = case_counts[2] + 1
                start_time = time.time()
                             
                # Add the record id into the inverted index
                temp_list = inv_index.get(rec_val_ind, [])
                temp_list.append((rec_id,ent_id))
                inv_index[rec_val_ind]= temp_list 
                  
            
            # Get all records from inverted index with this value 
            rec_id_list = inv_index.get(rec_val_ind, [])
            
            # Exactly matching other records                       
            for this_rec_id in rec_id_list:  
                if(accu_phase == 1):  
                    # Add new record identifier into accu
                    accu[this_rec_id] = 1.0 + accu.get(this_rec_id, 0.0)
                else:
                    # Only update similarities of existing records
                    if (this_rec_id in accu): 
                        accu[this_rec_id] = 1.0 + accu[this_rec_id]
             
                         
            # Next get approximate matches and insert them into accu with their
            # similarity values
            #
            rec_val_sim_dict = sim_dict.get(rec_val,[])
            
            # For all other similar records and their similarities
            #
            for other_rec_val in rec_val_sim_dict:
                sim_val = rec_val_sim_dict[other_rec_val]
                other_rec_val_ind = '%s' % (other_rec_val) # Attribute qualifier
                    
                # Get record identifiers of this record value (possibly there are no
                # such values in the similarity dictionary for this attribute)
                #
                if (other_rec_val_ind in inv_index):
                    other_rec_id_list = inv_index[other_rec_val_ind]
                
                    for other_rec_id in other_rec_id_list:  # Insert into accu
                        if(accu_phase == 1):  # Add new record identifier into accu
                            accu[other_rec_id] = sim_val + accu.get(other_rec_id, 0.0)
                        else:
                            if (other_rec_id in accu):  # Only update
                                accu[other_rec_id] = sim_val + accu[other_rec_id]
            
            end_time = time.time()
            case_timings[1] = case_timings[1] + (end_time - start_time)
            case_timings[2] = case_timings[2] + (end_time - start_time)
                                
        assert (num_case_two >= 0) and (num_case_two <= num_compared_attr)
        assert sum(case_counts.values()) == num_compared_attr
        assert num_case_two == case_counts[2]
        
        num_comp = len(accu)
        max_sim_val = -1.0      # Maximum so far calculated similarity value
        sim_rec_id_list = []    # List with record identifiers of the records that
                                # have the maximum similarity value
        
        # Extract the matches with a maximum similarity value
        #
        for (this_rec_id, total_sim_val) in accu.iteritems():           
            
            if(this_rec_id[0] != rec_id):
            
                if ((optimise == 0) or (total_sim_val >= min_tot_thres)):
        
                    if (total_sim_val > max_sim_val):  # A new maximum similarity value
                        max_sim_val = total_sim_val
                        sim_rec_id_list = [this_rec_id]
                    elif (total_sim_val == max_sim_val):  # Same as previous largest
                        sim_rec = this_rec_id
                        sim_rec_id_list.append(sim_rec)      # Similarity value
        del accu
        
        # Similarity aware inverted index specific information: The number of case
        # one (available in the inverted index) of the four query record values
        #
        spec_info = (num_case_two, case_timings, case_counts)
        
        return (sim_rec_id_list, num_comp, spec_info)    

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
    
    file_name = 'data/sample_data_set.csv'  # only csv files are allowed
    
    total_num_attr = 19  # Total number of attribute 
                        # including rec-id, and ent-id
    
    
    optimise_flag_str = sys.argv[1]             # optimization flag
    min_threshold = float(sys.argv[2])          # Minimal similarity threshold
    min_total_threshold = float(sys.argv[3])    # Minimal total threshold
    build_percentage = float(sys.argv[4])       # Percentage of records used to
                                                # build the index
     
    file_name = sys.argv[5]
    
    index_name = 'Dynamic Similarity Aware Indexing Technique'
                                
    
    if (optimise_flag_str.lower()[0] == 't'):
        optimise_flag = 1  # Optimisation level to be used in query() method
    else:
        optimise_flag = 0
 
        
    
    
    # Define encoding and comparison methods to be used for attributes
    # Note: first element in the list should always be None. 
    enco_methods = [None, encode.dmetaphone, encode.dmetaphone, 
encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,encode.dmetaphone,         encode.dmetaphone, __get_substr__]
    comp_methods = [None, stringcmp.winkler, stringcmp.winkler, 
stringcmp.winkler, stringcmp.winkler, stringcmp.winkler,stringcmp.winkler,stringcmp.winkler,stringcmp.winkler,stringcmp.winkler,stringcmp.winkler,stringcmp.winkler, stringcmp.winkler, stringcmp.winkler, stringcmp.winkler, stringcmp.winkler, stringcmp.winkler, stringcmp.winkler, stringcmp.winkler, stringcmp.winkler, stringcmp.winkler, stringcmp.winkler, __postcode_cmp__]
    
    
    ind = DySimII(total_num_attr,enco_methods, comp_methods, 
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
    print('  Finished building the index.')
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
       
      
        ent_id = clean_rec[0]
      
         
        start_time = time.time()
        res_list, num_comp, spec_info = ind.query(rec_id,clean_rec, optimise=optimise_flag)
        query_time = time.time() - start_time
        
        
        num_rec += 1
        if (num_rec % 100 == 0):
            print '\t Processed %d records in the query phase' % (num_rec)
        
        query_time_res.append(query_time)
        num_comp_res.append(num_comp)
            
        # Process index specific special information returned
        #        
        case_two_sum += spec_info[0]        
        if (spec_info[2][1] > 0):  # There were case 1
                case_timing[1] = case_timing[1] + (spec_info[1][1] / spec_info[2][1])
                case_counts[1] = case_counts[1] + 1
        if (spec_info[2][2] > 0):  # There were case 2
                case_timing[2] = case_timing[2] + (spec_info[1][2] / spec_info[2][2])
                case_counts[2] = case_counts[2] + 1
        
        
        if (res_list != []):  # Some results were returned

      
            # Check if the result list contains the correct matching record 
            # identifier
            #
           
            
            for i in range(len(res_list)):
                if (ent_id)== res_list[i][1] and rec_id != res_list[i][0]:
                    query_acc_res.append('TM')             
                else:
                    query_acc_res.append('FM')          
        
        query_cnt += 1
        
    assert (query_cnt - 1) == len(ind.query_records), \
               (query_cnt, len(ind.query_records))
        
    query_memo_str = auxiliary.get_memory_usage()
        


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
    if ind.count > 0:
        print '  Matching accuracy: %d/%d true matches (%.2f%%)' % \
              (num_tm, ind.count, 100.0 * num_tm / ind.count) 
    else:
        print' No duplicates where found' 
        
              
    print '  Query timing (min / max / avrg): %.3f / %.3f / %.3f sec' % \
              (min(query_time_res), max(query_time_res), \
               sum(query_time_res) / len(ind.query_records))
    print '  Number of comparisons (min / max / avrg): %d / %d / %d' % \
              (min(num_comp_res), max(num_comp_res), \
               int(round(sum(num_comp_res) / len(ind.query_records))))
    print '  %s' % (query_memo_str)
    
    print '  Average ratio of case 2 : case 1 query matching: %.2f' % \
                ((0.25 * case_two_sum) / len(ind.query_records))
    if (case_counts[1] != 0):
            print '    Case 1 average time: %.2f (ms)' % \
                    (1000.0 * (case_timing[1] / case_counts[1]))
            print '                 count: {0} (number of all new attributes) '.format(case_counts[1])
    if (case_counts[2] != 0):
            print '    Case 2 average time: %.2f (ms)' % \
                    (1000.0 * (case_timing[2] / case_counts[2]))
            print '                 count: {0} (number of all attributes that are indexed before)'.format(case_counts[2])
    print



    