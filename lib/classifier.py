import sys

sys.path.append("./libsvm/tools/")
sys.path.append("./libsvm/python/")
sys.path.append("./auxiliar/")
from sklearn.model_selection import GridSearchCV

import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.cross_validation import KFold
#from lib import active_learning
#from svmutil import *
#from grid import *

import numpy as np

def train_svm(rf,df_train,total_num_attr):

	print ("treinamento  %i " % ( len(df_train)))
	#print (df_train)
	X=df_train.iloc[:,0:total_num_attr].values
	Y=df_train[100].values
	
	if(np.count_nonzero(Y == 1)>3):
		p_grid = {"C": [1, 10, 100], "gamma": [.01, .1]}		
		svm = SVC(kernel="rbf")
		rf = GridSearchCV(estimator=svm, param_grid=p_grid,cv=None)
		
		
	
	#import numpy.ma as ma
	#np.where(np.isnan(X), ma.array(X, mask=np.isnan(X)).mean(axis=0), X)
	
	#print (df_train)
	#print (Y.astype(int))
	m = rf.fit(X,Y.astype(int) ) #svm_train(gabarito, pairs, '-c 4') 
	
	return m		 
 
	
def test_svm_online(rf, df_test,df_train, model,ind ,total_num_attr, active,flag_active):  
	
	X=df_test.iloc[:,0:total_num_attr]
	Y=df_test[100].values
	
	temp=[]
	for i in range(total_num_attr):
		temp.append(i)
	temp.append(100)
	temp.append(1001)
	#if(1 in Y):
	#	print (" Y " + str(Y))
	for i in range(len(Y)):
		if(flag_active==0):
			
			df2=pd.DataFrame(columns = temp);
# 			if(df_test.ix[i,100]==1 ):
# 				print("entrou " + str(df_test.iloc[i]))	
				
			df2.loc[df_test.index[i]] = df_test.iloc[i]
			
			df_train, flag= active.partial_active_learning(df2, df_train,total_num_attr)
			if(flag==True):
				model=train_svm(rf,df_train,total_num_attr)
		
		
		_labs = model.predict(X.iloc[i].values.reshape(1, -1)) #svm_predict(y, x, model )
	#print(df_test)   
	
		#print (_labs)
		#self.compute+=1;
		#true positive
		if( _labs[0]==1 and Y[i]==1):
			ind.true_positive+=1;
			#print ("------------------------------------------------------------true positive pair " +str(df_test.iloc[i]))				
			#remove do gabarito as tags reais 
			for x in (df_test[1001]):
				if(x!=-1):
					try:
						res_clean=x.split("-")[0]  
						
						gab_list=ind.inv_index_gab.get(res_clean,[])
						#print ("gab_list %s" % gab_list)
						#print "remove  %s" % x
						gab_list.remove(x)
						ind.inv_index_gab[res_clean]=gab_list
						#print "gab_list %s" % gab_list
					except ValueError:
						#print ("element not exists" + str(x))
						continue
		#false positive
		if(_labs[0] ==1 and Y[i]==0):
			ind.false_positive+=1;
			print( " false positive " + str(i) + "  ")
		#false negative 
		if(_labs[0] ==0 and Y[i]==1):
			print( " false negative  " + str(i) + "  ")
			ind.false_negative +=1;
		if(_labs[0] ==0 and Y[i]==0):
			ind.true_negative +=1;	
		
			
  #  print ("#####################fim do teste")

	return df_train

# def arfftoSVM(self, inputfilename,outfile):
# 	print ("gerando arquivo svm")
# 	fin = open(inputfilename,'r')
# 	lines = fin.readlines()
# 	#fin.close()
# 	outputfilename = outfile
# 	fout = open(outputfilename,'w')
# 	
# 	beginToRead = False
# 	for line in lines:
# 		flag =0
# 		if beginToRead == True:
# 			if len(line) > 1:# not an empty line
# 				#read this line
# 				dataList = line.split(',')
# 				resultLine =''
# 				resultLine += dataList[-1].strip()
# 				if (flag==0):
# 					resultLine += ' '
# 					flag=1
# 					
# 				for i in range(1,len(dataList)-1):
# 					resultLine += str(i)
# 					resultLine += (":"+dataList[i].strip()+" ")
# 			   # print(resultLine)
# 				fout.write(resultLine+"\n")
# 
# 		if line[0:6] == ' @DATA' or len([pos for pos, char in enumerate(line) if char == ','])>5:
# 			beginToRead = True
# 
# 	fout.close()