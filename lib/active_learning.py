"""Module with active learning functions
"""
import pandas as pd
import numpy as np
import sys 
import os
import collections
from numpy.core.defchararray import lower
from collections import defaultdict
from collections import Counter

class Active_learning:
    
    
    
    def __init__(self, rule_value):
        print ("start active object")
        self.less_frequent_rule_value=sys.maxsize
        self.less_frequent_rule_id=0
        self.df_train_d=pd.DataFrame()
        self.rule=sys.maxsize;
        
        self.lists_p = defaultdict(lambda  : defaultdict(list))
        self.lists_n = defaultdict(lambda  : defaultdict(list))
  
    
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
        df_train=df_train.append(df_test.iloc[memory[0]])
        
        a = np.empty(total_num_attr)
        a=a.reshape(1,total_num_attr)
        a.fill(1)
        df_train= pd.DataFrame(a).append(df_train, ignore_index=True)
        df_train.at[0, 100]=1
        df_train.at[0, 1001]=-1

        return df_train
    
    def active_learning(self,df_test, df_train,first_time_active,total_num_attr):
        
        df_test_discrete=(df_test.loc[:,0:total_num_attr]*10).astype(int)
        
        assert (len(df_test_discrete)==len(df_test)), "problem with active learning  %s %s " %(df_test,df_test_discrete)                  
        for i in range(total_num_attr):
            df_test_discrete[(i+total_num_attr)] = df_test_discrete.groupby([i])[i].transform('count')
            
        flag=False
        if(first_time_active==1):      
            df_train=(self.active_select_first_pair(df_test,df_train,df_test_discrete,total_num_attr))
            first_time_active=0
        self.df_train_d=((df_train.loc[:,0:total_num_attr])*10).astype(int)
        
        for i in range(1,len(self.df_train_d)):
            for j in range(total_num_attr):
                if(df_train.iloc[i,total_num_attr]==1.0):
                    self.lists_p[self.df_train_d.iloc[i][j]][j].append(df_test.iloc[i].name)
                else:
                    self.lists_n[self.df_train_d.iloc[i][j]][j].append(df_test.iloc[i].name)
        
        lower_pair_id=0
        while(1):
            lower_frequency, lower_pair_id= self.find_pair_less_frenquent(df_test,df_test_discrete,total_num_attr)
            
           
            
            if(len(df_train)==2):
                as_list = df_train.index.tolist()
                idx = as_list.index(0)
                as_list[idx] = -1
                df_train.index = as_list
            index_training= (df_train.index.tolist())
            index_test_discrete=df_test_discrete.index.tolist()
            if(lower_frequency<self.less_frequent_rule_value and   index_test_discrete[lower_pair_id] not in index_training):
                print ("first add the following pair "+  "  with " + str(lower_frequency) + "  label " + str(df_test.ix[lower_pair_id,100]))
                df_train=df_train.append(df_test.iloc[lower_pair_id])
                #for i in range(total_num_attr,total_num_attr+total_num_attr):
                 #   df_train.iat[len(df_train)-1, i]=df_test.iloc[memory[0],(i-total_num_attr)]  
                flag=True
                self.df_train_d=((df_train.loc[:,0:total_num_attr])*10).astype(int)
                for i in range(total_num_attr):   
                    if(df_train.iloc[len(self.df_train_d)-1,total_num_attr]==1):
                        self.lists_p[self.df_train_d.iloc[len(self.df_train_d)-1,i]][i].append(df_test.iloc[lower_pair_id].name)
                    else:    
                        self.lists_n[self.df_train_d.iloc[len(self.df_train_d)-1,i]][i].append(df_test.iloc[lower_pair_id].name)
                self.count_less_frequent_pair(df_train,self.df_train_d,total_num_attr)
                print ("new rule value " + str(self.less_frequent_rule_value))                 
            else:
                #print("convergiu com a regra "+ str(lower_pair_id))
                break
        return df_train,flag       
  
    def count_less_frequent_pair(self,df_train, df_train_d,total_num_attr):
        self.less_frequent_rule_value=sys.maxsize
        for i in range(1,len(self.df_train_d)):
            list_p=[]
            list_n=[]
            rules=0;
            for j in range((total_num_attr)):
                list_p+=((self.lists_p[self.df_train_d.iloc[i,j]][j]))
                list_n+=((self.lists_n[self.df_train_d.iloc[i,j]][j]))
            merge_p = dict(Counter(list_p))
            merge_n = dict(Counter(list_n))
            for j in (merge_p):
                temp=(merge_p[j])
                rules+= temp +((temp*(temp-1))/2) 
            for j in (merge_n):
                temp=(merge_n[j])
                rules+=(temp +((temp*(temp-1))/2))*3
            if(rules < self.less_frequent_rule_value):
                self.less_frequent_rule_value=rules    
    
    def find_pair_less_frenquent(self,df_test,df_test_discrete,total_num_attr):
        lower_frequency=sys.maxsize
        for i in range(len(df_test)):
            soma=0;
            for w in range(total_num_attr):
                soma+=df_test_discrete.iloc[i,w]
#             if(soma<total_num_attr*2):
#                 #print(soma)
#                 continue;
            list_p=[]
            list_n=[]
            rules=0;
            #if(df_test.iloc[i,total_num_attr]==1):
            #    print ("positive") 
            for j in range((total_num_attr)):
                list_p+=((self.lists_p[df_test_discrete.iloc[i,j]][j]))
                list_n+=((self.lists_n[df_test_discrete.iloc[i,j]][j]))
            merge_p = dict(Counter(list_p))
            
            merge_n = dict(Counter(list_n))
            
            for j in (merge_p):
                temp=(merge_p[j])
                rules+= temp +((temp*(temp-1))/2) 
            for j in (merge_n):
                temp=(merge_n[j])
                rules+=(temp +((temp*(temp-1))/2))*3
            
            if(rules<lower_frequency):
                lower_frequency=rules
                lower_pair_id=i;
                                   
        return lower_frequency, lower_pair_id
                    
    def partial_active_learning(self, df_test, df_train,total_num_attr):
         
        df_test_discrete=(df_test.loc[:,0:total_num_attr]*10).astype(int)
        flag=False
                 
        lower_pair_id=0
        while(1):
           
            lower_frequency, lower_pair_id= self.find_pair_less_frenquent(df_test,df_test_discrete,total_num_attr)
             
            index_training= (df_train.index.tolist())
            index_test_discrete=df_test_discrete.index.tolist()
            if(lower_frequency<self.less_frequent_rule_value and   index_test_discrete[lower_pair_id] not in index_training):
                print ("**************add the following pair "+  "  with " + str(lower_frequency) + "  label " + str(df_test.iloc[lower_pair_id,total_num_attr]) +" ---- ID "+ str(df_test.iloc[lower_pair_id].name))
                df_train=df_train.append(df_test.iloc[lower_pair_id])
                flag=True
                self.df_train_d=((df_train.loc[:,0:total_num_attr])*10).astype(int)
                
                for i in range(total_num_attr):   
                    if(df_train.iloc[len(self.df_train_d)-1,total_num_attr]==1):
                        self.lists_p[self.df_train_d.iloc[len(self.df_train_d)-1,i]][i].append(df_test.iloc[lower_pair_id].name)
                    else:    
                        self.lists_n[self.df_train_d.iloc[len(self.df_train_d)-1,i]][i].append(df_test.iloc[lower_pair_id].name)
                #self.less_frequent_rule_value=lower_frequency                     
                self.count_less_frequent_pair(df_train,self.df_train_d,total_num_attr)         
                print ("new rule value " + str(self.less_frequent_rule_value))    
            else:
                break
           
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
