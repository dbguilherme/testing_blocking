"""Module with active learning functions
"""
import pandas as pd
import numpy as np
import sys 
import os

def load_struct_active(self,list_of_pairs,gabarito):
    
    
    ###load discretized file
    list_of_pairs_discrete=[]
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

def active_select_first_pair(df_test,df_train,df_test_discrete,total_num_attr):
    
    lista=[]
    for i in range(total_num_attr,total_num_attr+total_num_attr):
        lista.append((i))
    
    ele=df_test_discrete[lista].sum(axis=1)
    top_values=sorted(enumerate(ele), key=lambda x: x[1], reverse=True)
# 
    memory = top_values[0];
    for tuple in top_values:
        if(memory[1] == tuple[1]):
            memory = tuple
    #print ("tuple final " + str(memory))  
    #print (df_test) 
    #print (df_test_discrete.iloc[memory[0]])
    df_train=df_train.append(df_test_discrete.iloc[memory[0]])
    
    for i in range(total_num_attr,total_num_attr+total_num_attr):
        df_train.iat[len(df_train)-1, i]=df_test.iloc[memory[0],(i-total_num_attr)]  
        
   # print ("posicao ")
   # print (df_train)
    #print(df_train.iloc[len(df_train)-1])
    
    
    
    df_train= pd.DataFrame(np.array([[9,9,9,9,9,9,9,9,9,9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9]])).append(df_train, ignore_index=False)
    df_train.at[0, 'label']=1
    df_train.at[0, 'rotulo']=-1
    #df_train[9][0]=1
    print ("first two pairs")
    print (df_train )

    return df_train

def active_learning(df_test, df_train,first_time_active,total_num_attr):
    
    #print(type(df_test))
    df_test_discrete= df_test.iloc[:,:total_num_attr].apply(lambda x: ((x*10)))
    df_test_discrete=df_test_discrete.iloc[:,:total_num_attr].astype(int)
    df_test_discrete['label']=df_test['label']
    df_test_discrete['rotulo']=df_test['rotulo']
    flag=False
       
    for i in range(total_num_attr):
        df_test_discrete[(i+total_num_attr)] = df_test_discrete.groupby([i])[i].transform('count')
   
    if(first_time_active==1):      
        df_train=(active_select_first_pair(df_test,df_train,df_test_discrete,total_num_attr))
        first_time_active=0
    print(df_train)  
    while(1):
        som=0
        print(("starting selection"))
        som=0
        rules=[]
        parcial=0
        for i in range((len(df_test_discrete))):        
            for index, row in df_train.iterrows():
                for j in range(total_num_attr-1):  
                    if (df_test_discrete.iat[i,j]==df_train.loc[index,j]):
                        som+=1;
                        if(df_train.loc[index,'label']==0):
                            som+=3
                parcial+=(som)
                som=0;
            #print (str(i) + " valor da soma " + str(parcial) +"  "+ str(som))
            rules.append(parcial)
            parcial=0
        #print (rules)
       #print((sorted(range(len(rules)), key=lambda i: rules[i], reverse=False)))
        memory=(sorted(range(len(rules)), key=lambda i: rules[i], reverse=False)[:1])
       # print ("top value %s "% memory)
        rules=[]
        index_training= (df_train.index.tolist())
        index_test_discrete=df_test_discrete.index.tolist()
        print (index_test_discrete[memory[0]])
        if(index_test_discrete[memory[0]] not in index_training):
            print ("**************add the following pair "+  "  with " )
            df_train=df_train.append(df_test_discrete.iloc[memory[0]])
            for i in range(total_num_attr,total_num_attr+total_num_attr):
                df_train.iat[len(df_train)-1, i]=df_test.iloc[memory[0],(i-total_num_attr)]  
            flag=True
            
            #print(df_train)
        else:
            break;    
   
        
    return df_train,flag

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
