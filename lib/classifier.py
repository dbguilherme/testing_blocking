import sys
sys.path.append("./libsvm/tools/")
sys.path.append("./libsvm/python/")
sys.path.append("./auxiliar/")

import numpy as np
#from svmutil import *
#from grid import *



def train_svm(self,rf, svm_file, pairs, gabarito):

    #os.system("export PYTHONPATH=//home/guilherme/git/testing_blocking/libsvm/tools/:$PYTHONPATH")
    #y, x = svm_read_problem(svm_file)
    
    #rate, param = find_parameters(svm_file, '-log2c -1,1,1 -log2g -1,1,1 -gnuplot null')
    #print ("xxxxxxxxxxxxxxxxxx %s %s" % (param.get('c'),(param.get('g'))))
    #p='-c '+ str(param.get('c')) +' -g ' + str(param.get('g'))
    gabarito=[float(i) for i in gabarito]
    print ("treinamento  %i " % ( len(pairs)))
    print ("gabarito  %i" % (len(gabarito)))
    x=np.array([])
    #array=np.array(pairs)
    for w in pairs:
         for key, value in w.items():
             #print (value)
             x=np.append(x, value);
   # print (x)
   # print (len(pairs))
    x=x.reshape(len(pairs),len(pairs[0]))
   # y=np.array(gabarito);
    #print(y.astype(int))
    
    
    
    m = rf.fit(x,gabarito ) #svm_train(gabarito, pairs, '-c 4') 
    return m         
     
def test_svm(self, model, file_full):  
    y, x = svm_read_problem(file_full)
    
   # x0, max_idx = gen_svm_nodearray({1:1, 3:1})
    _labs, p_acc, p_vals = svm_predict(y, x, model)
  
    
    for i in range(len(y)):
        if(y[i] != _labs[i]):
            self.false_positive+=1;
        else:
            self.true_positive+=1;
    
def test_svm_online(self,rf ,model, y, x, gabarito ):  
    #y, x = svm_read_problem(file_full)
   # print ("labellll-> " +str(y))
   # x0, max_idx = gen_svm_nodearray({1:1, 3:1})
    np_array=np.array([])
    #array=np.array(pairs)
    for w in x:
         for key, value in w.items():
             #print (value)
             np_array=np.append(np_array, value);
   # print (x)
    print (len(x[0]))
    np_array=np_array.reshape(len(x),len(x[0]))
    
    
    _labs = model.predict_proba(np_array) #svm_predict(y, x, model )
#         print (_labs)
#         print ()
#         print (y)
    for i in range(len(_labs)):
        if(_labs[i][0]>0.1 and _labs[i][0]<0.9):
            print ("---------------" + str(_labs[i]))
            
    
#         training_set_discreto, training_gabarito_discreto, stored_ids, flag_train = ind.active_learning(set_list_of_pairs, set_gabarito, training_set_discreto, training_gabarito_discreto, stored_ids)
#         set_list_of_pairs = ind.training_set_final
#         set_gabarito = ind.gabarito_set_final
#         n_rule = [0] * len(set_gabarito)


    _labs = model.predict(np_array) #svm_predict(y, x, model )
    
   # print(np_array.reshape(len(x),10))
    #print(np_array[1][5])
    #prediction, bias, contributions = ti.predict(rf, np_array)
   # pred, bias, contributions =ti.predict(rf, np_array)
    
    
    #if(prediction[0][0]>0.2 and  prediction[0][0]<0.8):
        #print (prediction)
    #    count+=1
        #print (count)   
    
    
    #print _labs
    for i in range(len(y)):
        self.compute+=1;
        #true positive
        if( _labs[i]==1 and y[i]==1):
            self.true_positive+=1;
           # print ("------------------------------------------------------------true positive pair " +str(x))                
            #remove do gabarito as tags reais 
            for x in (gabarito):
                if(x!=-1):
                    try:
                        res_clean=x.split("-")[0]  
                        
                        gab_list=ind.inv_index_gab.get(res_clean,[])
                        #print "gab_list %s" % gab_list
                        #print "remove  %s" % x
                        #gab_list.remove(x)
                        ind.inv_index_gab[res_clean]=gab_list
                        #print "gab_list %s" % gab_list
                    except ValueError:
                        print ("element not exists" + str(x))
        #false positive
        if(_labs[i] ==1 and y[i]==0):
            self.false_positive+=1;
        #false negative 
        if(_labs[i] ==0 and y[i]==1):
            self.false_negative +=1;
        if(_labs[i] ==0 and y[i]==0):
            self.true_negative +=1;    
  #  print ("#####################fim do teste")



def arfftoSVM(self, inputfilename,outfile):
    print ("gerando arquivo svm")
    fin = open(inputfilename,'r')
    lines = fin.readlines()
    #fin.close()
    outputfilename = outfile
    fout = open(outputfilename,'w')
    
    beginToRead = False
    for line in lines:
        flag =0
        if beginToRead == True:
            if len(line) > 1:# not an empty line
                #read this line
                dataList = line.split(',')
                resultLine =''
                resultLine += dataList[-1].strip()
                if (flag==0):
                    resultLine += ' '
                    flag=1
                    
                for i in range(1,len(dataList)-1):
                    resultLine += str(i)
                    resultLine += (":"+dataList[i].strip()+" ")
               # print(resultLine)
                fout.write(resultLine+"\n")

        if line[0:6] == ' @DATA' or len([pos for pos, char in enumerate(line) if char == ','])>5:
            beginToRead = True

    fout.close()