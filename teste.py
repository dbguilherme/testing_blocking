import os
import matplotlib.pyplot as plt1
import numpy as np
import matplotlib.pyplot as plt2


objects = range(5)
y_pos = np.arange(len(objects))
prec = []
recall=[]
    
    

for i in range(5):
    p = os.popen("python run.py","r")
    while 1:
        line = p.readline()
        if not line: break
        if "XXXPREC" in line:
            line= line.replace("XXXPREC" , "")
            p1,r1= (line.split(','))
            print (p1.lstrip(),r1.lstrip())
            prec.append(p1)
            recall.append(r1)
            
plt1.bar(y_pos, prec, align='center', alpha=0.5)
plt1.xticks(y_pos, objects)
    
    
plt2.bar(y_pos, recall, align='center', alpha=0.5)
plt2.xticks(y_pos, objects)
    #plt.ylabel('Usage')
    #plt.title('Programming language usage')
plt1.show()    
plt2.show()