import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt1
import matplotlib.pyplot as plt2
import os
import DySimII2013 as dy
import sys
def run():
    objects = (1,2,3)
    y_pos = np.arange(len(objects))
    prec = []
    recall=[]
    
   
    
    #ind.run("data/teste_20");
    for i in range(1):
        #print (weight)
        ind = dy.ActiveOnlineBlocking(15,5)
        ind.run("data/drift_110");
    #ind.run("data/teste_20");
    
    
    
    #    prec.append(p)
    #    recall.append(r)
    
    #plt.bar(y_pos, prec, align='center', alpha=0.5)
    #plt1.xticks(y_pos, objects)
    
    
    #plt2.bar(y_pos, recall, align='center', alpha=0.5)
    #plt2.xticks(y_pos, objects)
    #plt.ylabel('Usage')
    #plt.title('Programming language usage')
     
#     plt1.show()    
#     plt2.show()
#     
#     
#     
#     
#     print ("XXXXXXXXXXXXXXXXXX")
    #print ("prec %i recl %i " % (pre, rec))

    
    
    
if __name__ == '__main__':
    run()
    
    
            
            
            
            