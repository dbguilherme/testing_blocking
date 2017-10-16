
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
#   First_graph.py
#   Authour: Alan Richmond, Python3.codes
 
from pylab import plot, show, bar
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV 
 
from sklearn import svm
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, VotingClassifier

df = pd.read_csv('/tmp/lixo999')
x=df.iloc[:,0:10]
y=df.loc[:,'100']
df2 = pd.read_csv('/tmp/lixo99922')
x2=df2.iloc[:,0:10]
y2=df2.loc[:,'100']

X1 = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
y1 = np.array([1, 1, 1, 2, 2, 2])
clf1 = ExtraTreesClassifier()
clf2 = RandomForestClassifier()
clf3 = GaussianNB()
eclf = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3)], voting='soft')
#eclf1 = eclf1.fit(X1, y1)
#eclf1.predict(X1)

probas = [c.fit(X1, y1).predict_proba(X1) for c in (clf1, clf2, clf3, eclf)]

class1_1 = [pr[0, 0] for pr in probas]
class2_1 = [pr[0, 1] for pr in probas]

print (class1_1)
print (class2_1)
#clf = svm.SVC(kernel='linear', C=1.0)
#clf.fit(x, y)
#print(clf.predict(x2))


#wclf = svm.SVC(kernel='linear', class_weight={1: 10})
#wclf.fit(x, y)

#print(wclf.predict(x2))

#clf = svm.SVR()
#extraTree=ExtraTreesClassifier(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
#p_grid = {"C": [1, 10, 100], "gamma": [.01, .1, .001]}		
#svm = svm.SVC(kernel="rbf")

##svm = GridSearchCV(estimator=svm, param_grid=p_grid,cv=3)
#clf.fit(x, y) 

#m = svm.fit(x,y )
#ext=extraTree.fit(x,y)

#_labs = m.predict(x2)
#print (y2)


#print(_labs)

#print ("---------------------")
#print (extraTree.predict(x2))


#print(x2.iloc[0,:])
#print(x2.iloc[1,:])

#x=[ {0: 1.0, 1: 1.0, 2: 0.0, 3: 1.0, 4: 1.0, 5: 1.0, 6: 1.0, 7: 0.5, 8: 1.0, 9: 0.75}]
#y= [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#lista= ['365-dup-5', -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

#plot(x)                     # draw the graph
#show()   



#dt=pd.DataFrame(x,columns = [0,1,2,3,4,5,6,7,8,9])


#df2=pd.DataFrame(columns = [0,1,2,3,4,5,6,7,8,9]);

#df2.loc[dt.index[0]] = dt.iloc[0]
##dt= dt.append(dt, one_row)
#print (df2)



#print(dt.iloc[3].index)


#index=range(10,len(x)+10)




##print(dt)
#dt[100]=y
#dt[1000]=lista



#df_train_d=((dt.loc[:,0:5])*10).astype(int)
#print (df_train_d) 


#print(dt.iloc[0].index)
#print () 
#print (dt.iloc[0].index.isin(dt.index))


##print (dt.index.tolist())
##print (df.index.isin(df.iloc[0].index.values))

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
 
objects = (1,2,3,4,5,6)
y_pos = np.arange(len(objects))
performance = [10,8,6,4,2,1]
 
plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
#plt.ylabel('Usage')
#plt.title('Programming language usage')
 
plt.show()
#df_test_discrete= dt.iloc[:,:10].apply(lambda x: ((x*10)))
#df_test_discrete=df_test_discrete.iloc[:,:10].astype(int)
##df_test_discrete=df_test_discrete.replace([10,'k'],'k')
#df_test_discrete['label']=y
#df_test_discrete['rotulo']=lista

##print (df_test_discrete)
##print (df_test_discrete.index)



#x = (df_test_discrete)

#df2=df_test_discrete.iloc[0,5:10]
#index=[1,2,3,4,5]  
##df2.index = index
##x=x.append(df_test_discrete.loc[10], ignore_index=False)

#print (df2)
#print (type(x))
#print (df2.iloc[0])



#df = pd.DataFrame({'$a':[1,2], '$b': [10,20]})
#df2=df.iloc[1]
#print(df2)
#df2.columns = ['a', 'b']
#df.columns = ['a', 'b']
#print(df)

#print()


## OR
#print(df2.columns)
#print(df2.loc['$a'])

#print (df_test_discrete)

#X=df_test_discrete[0:9].values
#print (X)



##(df_test_discrete == df_test_discrete.iloc[0]).all(1).any()

#print(pd.merge(df_test_discrete.iloc[0], df_test_discrete, on=[1], how='left', indicator='Exist'))


#x=pd.concat([df_test_discrete,df_test_discrete]).drop_duplicates().reset_index(drop=True)
##print((df_test_discrete))


#print (len(df_test_discrete))

#print ((x))

#if(df_test_discrete.iat[0, 0]!=df_test_discrete.iat[1, 0]):
    #print("OK")

##print(dt.iloc[:,:10])




#xx= dt.iloc[:,:10].apply(lambda x: ((x*10)))


#x2=xx.iloc[:,:10].astype(int)

#x2=x2.replace([10,'k'],'k')
#x2=x2.astype(str)
#for i in range(10):
    #x2[i*100] = x2.groupby([i])[i].transform('count')

#lista=[]
#for i in range(1,10):
    #lista.append((i*100))
    
#ele=x2[lista].sum(axis=1)

#top_values=sorted(enumerate(ele), key=lambda x: x[1], reverse=True)  
##print ((top_values))

#memory = top_values[0];
#for tuple in top_values:
    #if(memory[1] == tuple[1]):
         #memory = tuple
##print ("tuple final " + str(memory))

##print (x2.iloc[memory[0]])

#print (len(x2))
#x3= pd.DataFrame(np.array([[2, 3, 4,5,6,7,8,8,8,8]])).append(x2, ignore_index=True)
#x3= pd.DataFrame(np.array([[2, 3, 4,5,6,7,8,8,8,8]])).append(x3, ignore_index=True)
#x3= pd.DataFrame(np.array([[2, 3, 4,5,6,7,8,8,8,8]])).append(x3, ignore_index=True)
#x3= pd.DataFrame(np.array([[2, 3, 4,5,6,7,8,8,8,8]])).append(x3, ignore_index=True)

#print()
##df.at['C', 'x']
#x3.at[0, 9]=-10000



##Wprint(x2[lista].sum(axis=1)   )
#print(len(x3))
    
#print (lista)

#a=1
#print()
#soma=0

##for i in range(1,10):
    ##print (x2[i*100][0])
##    soma+=(x2[i*100][0]).astype(int)

#print (x2.sum(axis=1))



#df1 = pd.DataFrame(np.random.rand(5,4))





#df2 = df1.ix[3:4]

#df2.reset_index(drop=True,inplace=True)
#df2.at[0,0]=1
#df2.at[0,2]=1
#print ("DF 2 ")
#print (df2)
#print (df1)
#print ("DF 2 ")

#som=0

#for i in range(len(df1)):
   #for j in range(len(df1.columns)):
       ##print (str(df1[j][i]) + "  " + str(df2[j][w]) + "  " + str(j) +"  "+ str(i) +" " + str(w))
       #for w in range(len (df2)):
           #if (df1[j][i]==df2[j][w]):
               #som+=1;
   #print (som)
   #som=0

#print (df1)
#df1 = pd.DataFrame({"A":['AA','AD','AD'], "B":['BA','BD','BF']})
#df2 = pd.DataFrame({"A":['AA','AD'], 'B':['BA','BF']})
#df1['compressed']=df1.apply(lambda x:'%s%s' % (x['A'],x['B']),axis=1)
#df2['compressed']=df2.apply(lambda x:'%s%s' % (x['A'],x['B']),axis=1)
#df1['Success'] = df1['compressed'].isin(df2['compressed']).astype(int)
#print (df1)

