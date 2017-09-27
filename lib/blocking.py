


def formatFile(inv_index_gab, filename):
    
    #inv_index_gab = self.inv_index_gab  
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
    for inv_list in inv_index_gab.items():
        if(len(inv_list)>1):
            size_gab+=len(inv_list)-1 
       # print inv_list[0]
    print (' TAMANHO GAB %d' % size_gab)
    saida.close()
    return file_out
    

# ===============================================================================================        
    

    
def Insert_value(inv_index,rec_id,rec_val,i):
    ''' Inserts a record value to the inverted indexes RI, SI, and BI
    '''
    # Shorthands to make program faster
    #inv_index = self.inv_index  
    #sim_dict = self.sim_dict
    #block_dict = self.block_dict
    
    #enco_methods = self.enco_methods
   # comp_methods = self.comp_methods
    
    rec_val_ind = '%s' % (rec_val)     # Add attribute qualifier for the
                                            # inverted index values

    # Insert the record value with qualifier into the inverted index
    
    rec_id_list = inv_index.get(rec_val_ind, [])
    this_rec_id = (rec_id)    # this is a set of -->(rec id, entity id)
    rec_id_list.append(this_rec_id)
    
    inv_index[rec_val_ind] = rec_id_list
    return inv_index