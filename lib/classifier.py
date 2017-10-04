import sys

sys.path.append("./libsvm/tools/")
sys.path.append("./libsvm/python/")
sys.path.append("./auxiliar/")

import numpy as np
import pandas as pd
from lib import active_learning
#from svmutil import *
#from grid import *



def train_svm(rf,df_train,total_num_attr):

	print ("treinamento  %i " % ( len(df_train)))
	print (df_train.iloc[:,total_num_attr:total_num_attr+total_num_attr].values)
	   
	X=df_train.iloc[:,0:total_num_attr].values
	import numpy.ma as ma
	np.where(np.isnan(X), ma.array(X, mask=np.isnan(X)).mean(axis=0), X)
	Y=df_train[100].values
	print (df_train)
	print (Y)
	m = rf.fit(X.astype(int),Y ) #svm_train(gabarito, pairs, '-c 4') 
	return m		 
 
	
def test_svm_online(rf, df_test,df_train, model,ind ,total_num_attr, active):  
	
	X=df_test.iloc[:,0:total_num_attr]
	Y=df_test[100].values
	
	_labs = model.predict_proba(X) #svm_predict(y, x, model )
	#print(df_test)   
#		 print ()
#		 print (y

	for i in range(len(_labs)):
		if(df_test.index[10]==10):
			break;
		if (1 in Y):
			#print(_labs)	
		
			
			
			df2=pd.DataFrame(columns = [0,1,2,3,4,5,6,7,8,9, 100, 1001]);
			
			df2.loc[df_test.index[i]] = df_test.iloc[i]
		
			df_train, flag= active.partial_active_learning(df2, df_train,total_num_attr)
			if(flag==True):
				model=train_svm(rf,df_train,total_num_attr)
	
	_labs = model.predict(X) #svm_predict(y, x, model )
	
	for i in range(len(Y)):
		#self.compute+=1;
		#true positive
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
						print ("element not exists" + str(x))
						continue
		#false positive
		if(_labs[i] ==1 and Y[i]==0):
			ind.false_positive+=1;
			print( " false positive " + str(i) + "  ") )
		#false negative 
		if(_labs[i] ==0 and Y[i]==1):
			ind.false_negative +=1;
		if(_labs[i] ==0 and Y[i]==0):
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