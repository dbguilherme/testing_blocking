import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt1
import matplotlib.pyplot as plt2
import os
import DySimII2013 as dy
 
<<<<<<< HEAD
=======
from subprocess import Popen, PIPE

 
 
>>>>>>> e2341f7e498a088bb6df57cb79b6c8e931036263
def run():
    objects = (1,2,3)
    y_pos = np.arange(len(objects))
    prec = []
    recall=[]
<<<<<<< HEAD
    
   
    ind = dy.ActiveOnlineBlocking(10)
    #ind.run("data/teste_20");
    ind.run("data/teste_1000_desbanc");
=======
    os.system("ls aaa $> /tmp/lixo10")
    for i in range(1,4):
        for j in range(1,3):
            os.system("python2.7 DySimII2013.py " + str(i)+" 1  1 0 /home/guilherme/git/testing_blocking/data/teste_1000_desbanc $>> /tmp/lixo10")
            
    
    
    
    #p = Popen(['python2.7 DySimII2013.py', '1 1  1 0 /home/guilherme/git/testing_blocking/data/teste_1000_desbanc'], stdout=PIPE, stderr=PIPE, stdin=PIPE)

    
    #ind = dy.ActiveOnlineBlocking(10)
    #ind.run("data/teste_20");
    #ind.run("data/teste_1000_desbanc");
>>>>>>> e2341f7e498a088bb6df57cb79b6c8e931036263
    
    
    
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
<<<<<<< HEAD
    
    
            
            
            
            
=======
    
>>>>>>> e2341f7e498a088bb6df57cb79b6c8e931036263
