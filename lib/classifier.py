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


		#eclf.fit(X, y);
		#eclf.predict(X)
	
	def train(self, df_train,total_num_attr):
		
		
		#print (df_train)
		X=df_train.iloc[:,0:total_num_attr-1].values
		Y=df_train[100].values
	# 	if(len(X)>10):
	# 		print (X)
	# 		print ("--------------")
	# 		print (Y)
# 		svm = SVC(kernel='rbf', C=1.0)
# 		if(np.count_nonzero(Y == 1)>3):
# 			#print ("treinamento grid  %i " % ( len(df_train)))
# 			p_grid = {"C": [1, 10, 100], "gamma": [.01, .1, .001]}		
# 			svm = SVC(kernel="rbf")
# 			rf = GridSearchCV(estimator=svm, param_grid=p_grid)
			
			
		
		#import numpy.ma as ma
		#np.where(np.isnan(X), ma.array(X, mask=np.isnan(X)).mean(axis=0), X)
		
		#print (df_train)
		#print (Y.astype(int))
		#if(Y[len(Y)-1]==1):
		#	print ("positve")
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
		
		#for clf, label in zip([self.eclf.clf1, self.eclf.clf2, self.eclf.clf3, self.eclf.clfs], ['MultinomialNB','PassiveAggressiveClassifier','BernoulliNB' ]):#['Logistic Regression', 'Random Forest', 'SVC', 'Ensemble']):
		_labs = self.eclf.predict(X) #svm_predict(y, x, model )
		
		for i in range(len(X)):
# 				if(avg[i][0]>0.2 and avg[i][0]<0.8):
# 					print ("instavel ...."+ str(X.iloc[i].name)+"  " +str(avg[i]))
			if( _labs[i]==1 and Y[i]==1):
				
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
			if(_labs[i]==1 and Y[i]==0):
				ind.false_positive+=1;
				#print( " false positive " + str(i) + "  "+  "  "+str(avg)  )
			#false negative 
			if(_labs[i] ==0 and Y[i]==1):
				
				print( " false negative  " + str(X.iloc[i].name) + "  " + "  " )
				
				
				#print(df_train.to_string())
				#df_train.to_csv("/tmp/lixo999", sep=',')
				#df_test.to_csv("/tmp/lixo99922", sep=',')
				#print (X.iloc[i,:])
				ind.false_negative +=1;
			if(_labs[i] ==0 and Y[i]==0):
				ind.true_negative +=1;	
			
		
		
		count=0	
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