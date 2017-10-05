"""Module with active learning functions
"""
import pandas as pd
import numpy as np
import sys 
import os


class Active_learning:
    
    def __init__(self, rule_value):
        print ("start active object")
        self.least_frequent_rule_value=rule_value
        self.least_frequent_rule_id=0
        
        self.df_train_d=pd.DataFrame()
        
        
#     def load_struct_active(self,list_of_pairs,gabarito):
#         
#         
#         ###load discretized file
#         list_of_pairs_discrete=[]
#         for line in list_of_pairs:
#             dict ={}
#             for k,v in line.items():
#                   dict[k]=str(int(v*10))
#                   if(v==1.0):
#                       dict[k]='k'
#             list_of_pairs_discrete.append(dict);
#     
#         return list_of_pairs_discrete,id 
    
    def active_select_first_pair(self, df_test,df_train,df_test_discrete,total_num_attr):
        
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
        df_train=df_train.append(df_test.iloc[memory[0]])
        
        
        df_train= pd.DataFrame(np.array([[1,1,1,1,1,1,1,1,1,1]])).append(df_train, ignore_index=False)
        df_train.at[0, 100]=1
        df_train.at[0, 1001]=-1

    
        return df_train
    
    def active_learning(self,df_test, df_train,first_time_active,total_num_attr):
        
       # print(type(df_test.ix[:,100]))
        
        df_test_discrete=(df_test.loc[:,0:total_num_attr]*10).astype(int)
        
        assert (len(df_test_discrete)==len(df_test)), "problem with active learning  %s %s " %(df_test,df_test_discrete)                  
        
        flag=False
           
        for i in range(total_num_attr):
            df_test_discrete[(i+total_num_attr)] = df_test_discrete.groupby([i])[i].transform('count')
       
        if(first_time_active==1):      
            df_train=(self.active_select_first_pair(df_test,df_train,df_test_discrete,total_num_attr))
            first_time_active=0
        #print(df_train)  
        self.df_train_d=((df_train.loc[:,0:total_num_attr])*10).astype(int)
        while(1):
            som=0
            #print(("starting selection"))
            rules=[1000000]
            parcial=0
            try:
                for i in range(1,(len(df_test_discrete))):        
                    for index, row in self.df_train_d.iterrows():
                        for j in range(total_num_attr-1):  
                            if (df_test_discrete.iat[i,j]==self.df_train_d.loc[index,j]):
                                som+=1;
                                if(df_train.loc[index,100]==0):
                                    som+=2
                        parcial+=2**(som)
                        som=0;
                    #print (str(i) + " valor da soma " + str(parcial) +"  "+ str(som))
                    rules.append(parcial)
                    parcial=0
            except  ValueError as e:
                #print (str(e.strerror))
                print ("exception .............")
                print (self.df_train_d)
                raise
            #print (rules)
           #print((sorted(range(len(rules)), key=lambda i: rules[i], reverse=False)))
            memory=(sorted(range(len(rules)), key=lambda i: rules[i], reverse=False)[:1])
           # print ("top value %s "% memory)
            
            index_training= (df_train.index.tolist())
            index_test_discrete=df_test_discrete.index.tolist()
           # print (index_test_discrete[memory[0]])
            if(index_test_discrete[memory[0]] not in index_training):
                print ("**************add the following pair "+  "  with " + str(memory[0]) + "  label " + str(df_test.ix[memory[0],100]))
                df_train=df_train.append(df_test.iloc[memory[0]])
                #for i in range(total_num_attr,total_num_attr+total_num_attr):
                 #   df_train.iat[len(df_train)-1, i]=df_test.iloc[memory[0],(i-total_num_attr)]  
                flag=True
                self.df_train_d=((df_train.loc[:,0:total_num_attr])*10).astype(int)
                self.least_frequent_rule_value=rules[memory[0]]
                #print(df_train)
                print ("less frequent rule value " + str(self.least_frequent_rule_value))
            else:
                print("convergiu com a regra "+ str(memory[0]))
                break;    
       
            rules=[]
        return df_train,flag
    
    def rule_calculation(self, df_test, df_train,total_num_attr,rule_number):
        
        try:
            df_test_discrete=(df_test.iloc[:,0:total_num_attr-1]*10).astype(int)
        except:
            print("exception ")
            return 
        
        #if(df_test.loc[:,100].any()==1 and rule_number!=0):
        #    print("entrou " + str(self.least_frequent_rule_value))
        
        assert (len(df_test_discrete)==len(df_test)), "problem with active learning  %s %s " %(df_test,df_test_discrete)                  
        flag=False
        som=0
        #print(("starting selection"))
        if(len(df_test_discrete.columns)==0):
            print ("Dataframe  EMPTY")
            print((df_test.iloc[:,0:total_num_attr]*10))
            return df_train,flag
        inicial_positin=1
        if(rule_number!=0):
            rules=[rule_number]
            inicial_positin=0
        else:
            rules=[]
            inicial_positin=1
        parcial=0
        try:
            for i in range(inicial_positin,(len(df_test_discrete))): 
                for index, row in self.df_train_d.iterrows():
                    for j in range(total_num_attr-1):  
                        if (df_test_discrete.iat[i,j]==self.df_train_d.loc[index,j]):
                            som+=1;
                            if(df_train.loc[index,100]==0):
                                som+=2
                    parcial+=2**(som)
                    som=0;
            #print (str(i) + " valor da soma " + str(parcial) +"  "+ str(som))
                rules.append(parcial)
                parcial=0
        except  ValueError as e:
            print (str(e.strerror))
            print ("exception .............")
            print (self.df_train_d)
            return
        except IndexError as e:           
            print ("posiçaõ invalida ")
            return
        #print (rules)
       #print((sorted(range(len(rules)), key=lambda i: rules[i], reverse=False)))
        memory=(sorted(range(len(rules)), key=lambda i: rules[i], reverse=False))
        
        return rules, memory    
    
    def partial_active_learning(self, df_test, df_train,total_num_attr):
        
        if(df_test.loc[:,100].any()==1):
            print("entrou " + str(self.least_frequent_rule_value))
        flag=False
        rules,memory = self.rule_calculation(df_test, df_train, total_num_attr,self.least_frequent_rule_value)
        
        if(memory[0]!=0):        
            print ("**************add the following pair "+  "  with " + str(memory[0]-1))
            df_train=df_train.append((df_test.iloc[memory[0]-1]))
                        
            rules,memory = self.rule_calculation(df_train, df_train, total_num_attr,0)
            
            self.df_train_d=((df_train.iloc[:,0:total_num_attr-1])*10).astype(int)
            self.least_frequent_rule_value=rules[memory[0]]
            print(" self.least_frequent_rule_value    " + str(self.least_frequent_rule_value))
            flag=True
       
   
        
        return df_train,flag
    
         ##############encontrar bug aqui!!!!!!!!!!!!!!!!!!!!!!!!!
#     def allac (self, file, flag):
#         self.count+=100;
#         if(flag==1):
#             os.system("cd ssarp &&  rm train-B5-* ")
#             os.system("cd ssarp &&  ./gera_bins_TUBE.sh "+ file +"  5")
#             os.system("cd ssarp && ./discretize_TUBE.pl train-B5 "+file+ "  5 lac_train_TUBEfinal.txt 1")
#     #             os.system("cd ssarp && ./updateRows.pl lac_train_TUBEfinal.txt lac_train_TUBEfinal_rows.txt " + str(self.count))
#     #             os.system("cd ssarp && rm alac_lac_train_TUBEfinal_rows.txt")
#     #             os.system("cd ssarp && ./run_alac_repeated.sh lac_train_TUBEfinal_rows.txt 1")
#     #             os.system("cd ssarp && ./desUpdateRows.pl alac_lac_train_TUBEfinal_rows.txt alac_lac_train_TUBEfinal.txt " + str(self.count))
#     #             os.system("cd ssarp && cat alac_lac_train_TUBEfinal.txt | awk '{ print $1 }'  | while read instance; do  sed  -n  \"$instance\"p  " + file+"; done >> /tmp/final_treina.arff;")
#         else:
#             #os.system("cd ssarp &&  rm train-B16-* && ./gera_bins_TUBE.sh "+ file +"  16")
#             #os.system("cd ssarp && ./discretize_TUBE.pl train-B16 "+file+ "  16 lac_train_TUBEfinal.txt 1")
#             #os.system("cd ssarp && ./updateRows.pl lac_train_TUBEfinal.txt  lac_train_TUBEfinal_rows.txt  " + str(self.count))
#             
#             #os.system("cd ssarp && ./run_alac_repeated.sh lac_train_TUBEfinal_rows.txt 1")
#             #os.system("cd ssarp && ./desUpdateRows.pl alac_lac_train_TUBEfinal_rows.txt alac_lac_train_TUBEfinal.txt " + str(self.count))
#             #os.system("cd ssarp && cat alac_lac_train_TUBEfinal.txt | awk '{ print $1 }'  | while read instance; do  sed  -n  \"$instance\"p  " + file+"; done >> /tmp/final_treina.arff;")
#             #os.system("cd ssarp && wc -l alac_lac_train_TUBEfinal.txt")  
#             print ("erro ")
#         #os.system("cd ssarp && cat "+file+" > /tmp/temp " )                          
