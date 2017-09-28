"""Module with active learning functions
"""
import pandas as pd
import numpy as np
import sys 
import os

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

def active_select_first_pair(df_test,df_train,df_test_discrete):
    
        #matrix = np.zeros((len(list_of_pairs_discrete),len(list_of_pairs_discrete[0])))   #[[0 for x in range(len(list_of_pairs))] for y in range(59)]
     
   # print (df_test) 
    lista=[]
    for i in range(1,10):
        lista.append((i*100))
    
    ele=df_test_discrete[lista].sum(axis=1)
    
    top_values=sorted(enumerate(ele), key=lambda x: x[1], reverse=True)
    #print ((top_values))
# 
    memory = top_values[0];
    for tuple in top_values:
        if(memory[1] == tuple[1]):
            memory = tuple
    #print ("tuple final " + str(memory))  
    #print (df_test) 
    #print (df_test_discrete.iloc[memory[0]])
    df_train=df_train.append(df_test_discrete.iloc[memory[0]])
    
    #add positive pair 
    
    
    #     # add a  positive pair
    df_train= pd.DataFrame(np.array([[9,9,9,9,9,9,9,9,9,9]])).append(df_train, ignore_index=False)
    df_train.at[0, 'label']=1
    df_train.at[0, 'rotulo']=-1
    #df_train[9][0]=1
    print ("first two pairs")
    print (df_train )
#     temp_ele = {}
#     temp_ele_d = {}
#     for i in range (10):
#         temp_ele[i] = 0.9
#         temp_ele_d[i] = "9"
#     
#     self.training_set_final.append(temp_ele)
#     self.gabarito_set_final.append(1)
#     
#     training_set.append(temp_ele_d)
#     training_set_gabarito.append('1')
#     training_gabarito.append("1")
#     stored_ids.append("-1")

#     for i in range(len(list_of_pairs_discrete)):
#         for j in range(len(list_of_pairs_discrete[i])):
#             matrix[i][j] = collumn_frequency[j][list_of_pairs_discrete[i][j]]
#     value = []        
#     for i in range(len(list_of_pairs_discrete)):
#         value.append(sum(matrix[i]));
# 
#     print ("total de valores por linha %s" % value)
#     
#     
#     count_value = [0] * len(list_of_pairs_discrete)
#    # top_values= sorted(range(len(value)), key=lambda i: value[i], reverse=True)[:2] #get the top values positions
#     top_values = sorted(enumerate(value), key=lambda x: x[1], reverse=True)                       
#     print ("top  valores %s " % top_values)
#     
#     memory = top_values[0];
#     for tuple in top_values:
#         if(memory[1] == tuple[1]):
#             memory = tuple
#     print ("tuple final %s" % memory[0])
#     print (list_of_pairs_discrete)
# 
#     end = time.time()        
#    # print("time to select first element %f " % (end - start))
# 
#     stored_ids.append(memory[0])
#     training_set = []        
#     training_set.append (list_of_pairs_discrete[memory[0]])                      
#     training_set_gabarito.append(gabarito[memory[0]])           
#     
#     self.training_set_final.append(list_of_pairs[memory[0]])
#     self.gabarito_set_final.append(gabarito[memory[0]])
#     training_gabarito.append(gabarito[memory[0]])
#     # add a positive pair
#     self.first_time_active = 0
#     
#     # add a  positive pair 
#     temp_ele = {}
#     temp_ele_d = {}
#     for i in range (len(list_of_pairs[memory[0]])):
#         temp_ele[i] = 0.9
#         temp_ele_d[i] = "9"
#     self.training_set_final.append(temp_ele)
#     self.gabarito_set_final.append(1)
#     
#     training_set.append(temp_ele_d)
#     training_set_gabarito.append('1')
#     training_gabarito.append("1")
#     stored_ids.append("-1")
# 
#     return training_set, training_gabarito ,stored_ids 

    return df_train

def active_learning(df_test, df_train,first_time_active):
    
    
   # print (df_test)
    df_test_discrete= df_test.iloc[:,:10].apply(lambda x: ((x*10)))
    df_test_discrete=df_test_discrete.iloc[:,:10].astype(int)

    #df_test_discrete=df_test_discrete.replace([10,'k'],'k')
    #df_test_discrete=df_test_discrete.astype(str)
    df_test_discrete['label']=df_test['label']
    df_test_discrete['rotulo']=df_test['rotulo']
   
    #print("pares a serem processador %i %i " % (len(list_of_pairs), len(list_of_pairs_discrete)))
   
    #print(df_test_discrete)
    #flag_train=0
    #print()
    #print("serie "+ str(type(df_test_discrete[0][0])))  
   
    #encontrar a primeira linha
    #collumn_frequency=[]; 
    #training_set_gabarito=[]   
    #temp=collections.Counter()
   # max_value=[]
#         for j in range(len(list_of_pairs_discrete[0])): # para cada coluna fazer a varedura
#             for i in range(len(list_of_pairs_discrete)): # varrear as linhas 
#                 temp[list_of_pairs_discrete[i][j]]+=1
#             collumn_frequency.append(temp)            
#             temp= collections.Counter()    
    for i in range(len(df_test.columns)-2):
        #print (i)
        df_test_discrete[(i+1)*100] = df_test_discrete.groupby([i])[i].transform('count')
   # print (df_test_discrete)
   
    if(first_time_active==1):      
        df_train=(active_select_first_pair(df_test,df_train,df_test_discrete))
        first_time_active=0
    #print(df_train)  
    while(1):
        lowest_rule=sys.maxsize
        lowest_id=0
        #for j in range(len(df_test_discrete)):
        som=0
        
        #print(df_train.ix[:,0:10])
        #print(df_train['label'])
        #print ()
    
        #print(df_test_discrete.ix[:,0:11])  
   
        print(("starting selection"))
        som=0
        rules=[]
        parcial=0
        for i in range((len(df_test_discrete))):        
            for index, row in df_train.iterrows():
               
                for j in range(9):  
                              
                   # print ("-----")
                   # print (index)
                    
                    #print (str(df_test_discrete.iat[i,j]) + "  " + str(df_train.iat[index,j])+ "  " + str(j) +"  "+ str(i) +" " )
                    if (df_test_discrete.iat[i,j]==df_train.loc[index,j]):
                        som+=1;
                        if(df_train.loc[index,'label']==0):
                            som+=1
                parcial+=(som)
                som=0;
            #print (str(i) + " valor da soma " + str(parcial) +"  "+ str(som))
            rules.append(parcial)
            parcial=0
        print (rules)
        print((sorted(range(len(rules)), key=lambda i: rules[i], reverse=False)))
        memory=(sorted(range(len(rules)), key=lambda i: rules[i], reverse=False)[:1])
        print ("top value %s "% memory)
        rules=[]
        index_training= (df_train.index.tolist())
        index_test_discrete=df_test_discrete.index.tolist()
        print (index_test_discrete[memory[0]])
        if(index_test_discrete[memory[0]] not in index_training):
            df_train=df_train.append(df_test_discrete.iloc[memory[0]])
            print(df_train)
            
        #merge=pd.merge(df_test_discrete.iloc[memory, 0:10],df_train.iloc[:, 0:10],  how='inner')
#         if(len(merge)==0):
#             df_train= df_train.append(df_test_discrete[memory, 0:10])
#             df_train.loc[len(df_train)-1,'label']=df_test_discrete.loc[memory, 'label']
#         print(df_train)
        break;
    return df_train
#        if(list_of_pairs_discrete[lowest_id] not in training_set):
#         for i in range(len(df_test_discrete)):
#             for j in range(len(df_test_discrete.columns)):
#        #print (str(df1[j][i]) + "  " + str(df2[j][w]) + "  " + str(j) +"  "+ str(i) +" " + str(w))
#                 for w in range(len (df_train)):
#                     print ("xxxxxxxxxxxx")
#                     print (df_test_discrete.iat[j, i])
#                     if (df_test_discrete.iat[j, i]==df_train.iat[j, w]):
#                         som+=1;
#             print (som)
#             som=0   
#            
#        # print "top value %s "% sorted(range(len(count_value)), key=lambda i: count_value[i], reverse=True)[:1]
#         
#         #encontra o resto 
#         
#         while(1):
#             contador=0
#             start = time.time()   
#             lowest_rule=sys.maxsize
#             lowest_id=0
#             for j in range(len(list_of_pairs_discrete)):
#                 join_pairs=' '.join('{}'.format(value) for key, value in list_of_pairs_discrete[j].items())
#                 teste_soma=0                
#                 for i in range(len(training_set)):
#                     join_gab=' '.join('{}'.format(value) for key,value in training_set[i].items())
#                     if(training_gabarito[i]==0):
#                         teste_soma+=((2**((sum(1 for a, b in zip(join_pairs, join_gab) if a == b))-(self.total_num_attr-1)))-1)
#                     else:
#                         teste_soma+=(2**((sum(1 for a, b in zip(join_pairs, join_gab) if a == b))-(self.total_num_attr-1)))-1
#                    # print (str(j)+ "---string ---" + str(join_pairs)+"---"+str(join_gab)+"---"+str(teste_soma))
#                 if(teste_soma<=lowest_rule):
#                     lowest_rule=teste_soma
#                     lowest_id=j
#                 #print ("summm _> "+str(lowest_id) +"   "+str(lowest_rule))    
#                 
#             
#             
#             if(list_of_pairs_discrete[lowest_id] not in training_set):
#                 n_rule=[0]*len(n_rule)
#                 stored_ids.append(lowest_id)               
#                 training_set.append(list_of_pairs_discrete[lowest_id])
#                 training_set_gabarito.append(gabarito[lowest_id])  
#                 training_gabarito.append(gabarito[lowest_id])
#                 self.training_set_final.append(list_of_pairs[lowest_id])
#                 self.gabarito_set_final.append(gabarito[lowest_id])  
#                 flag_train=1 
#                 print ("************************novo training set size  "+str(len(self.training_set_final)) + "   "+ str(self.training_set_final))
#                 print ("**********************************"+ str(self.gabarito_set_final))
#                 end = time.time()      
#                 print("time to select %f" %(end - start))
#                 
#             else:
#                # print ("convergiu com a linha %i" % lowest_id)
#                # print ("tamanho do treinamento %i " % len(training_set))
#                # print ("Gabarito do treinamento %s" % self.gabarito_set_final)
#                 break    
        
        
                 
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
