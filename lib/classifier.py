import sys

sys.path.append("./libsvm/tools/")
sys.path.append("./libsvm/python/")
sys.path.append("./auxiliar/")
from sklearn.model_selection import GridSearchCV

from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.cross_validation import KFold
from lib.assemble import EnsembleClassifier
#from lib import active_learning
#from svmutil import *
#from grid import *

import numpy as np


class classification:
		
	def __init__(self, x):
	
		self.eclf = x

	def train(self, df_train,total_num_attr):
		
		
		X=df_train.iloc[:,0:total_num_attr-1].values
		Y=df_train[100].values
		if(np.count_nonzero(Y == 1)>3):
			#print ("treinamento grid  %i " % ( len(df_train)))
			p_grid = {"C": [0.1, 1, 10, 100], "gamma": [.01, .1, .001]}		
			svm = SVC(kernel="rbf")
			rf = GridSearchCV(estimator=svm, param_grid=p_grid)
			self.eclf=rf
			
		print("treinando novamente")
		m = self.eclf.fit(X,Y) #svm_train(gabarito, pairs, '-c 4') 
		return m		 
	
	def test_svm_online(self, rf, df_test,df_train, model,ind ,total_num_attr, active,flag_active):  
		
		X=df_test.iloc[0:,0:total_num_attr-1]
		Y=df_test[100].values
		
		if(flag_active==0):
			df_train, flag= active.partial_active_learning(df_test, df_train,total_num_attr)
			if(flag==True):
				self.train(df_train,total_num_attr)
		
		_labs = self.eclf.predict(X) #svm_predict(y, x, model )
		
		for i in range(len(X)):
			
			if(_labs[i] ==0 and Y[i]==0):
				ind.true_negative +=1;	
				continue;
			if( _labs[i]==1 and Y[i]==1):
				ind.true_positive+=1;
				x= (df_test.iloc[i,total_num_attr+1])
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
				continue;
			if(_labs[i]==1 and Y[i]==0):
				ind.false_positive+=1;
				continue;
			if(_labs[i] ==0 and Y[i]==1):
				train=df_train.index.tolist()
				if(X.iloc[i].name in train and Y[i]==1):
					ind.true_positive+=1;
					continue;
				print( " false negative  " + str(df_test.iloc[i]) + "  " + "  " )
				ind.false_negative +=1;
				continue;
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