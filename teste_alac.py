import string
import sys
import time
import os
from numpy.matlib import rand
sys.path.append("/home/guilherme/git/testing_blocking/libsvm/tools/")
sys.path.append("/home/guilherme/git/testing_blocking/libsvm/python/")
sys.path.append("/home/guilherme/git/testing_blocking/libsvm/python/")
import distance


# From Febrl  http://sourceforge.net/projects/febrl/

import random
from collections import OrderedDict,defaultdict
from grid import *
import collections
import copy
import numpy as np
from timeit import default_timer as timer


def allac (file, flag):
        
        if(flag==1):
            os.system("cd ssarp &&  rm train-B10-* ")
            os.system("cd ssarp &&  ./gera_bins_TUBE.sh "+ file +"  10")
            os.system("cd ssarp && ./discretize_TUBE.pl train-B10 "+file+ "  10 lac_train_TUBEfinal.txt 1")
            os.system("cd ssarp && ./updateRows.pl lac_train_TUBEfinal.txt lac_train_TUBEfinal_rows.txt ")
            os.system("cd ssarp && rm alac_lac_train_TUBEfinal_rows.txt")
            os.system("cd ssarp && ./run_alac_repeated.sh lac_train_TUBEfinal_rows.txt 1")
            os.system("cd ssarp && ./desUpdateRows.pl alac_lac_train_TUBEfinal_rows.txt alac_lac_train_TUBEfinal.txt ")
            os.system("cd ssarp && cat alac_lac_train_TUBEfinal.txt | awk '{ print $1 }'  | while read instance; do  sed  -n  \"$instance\"p  " + file+"; done >> /tmp/final_treina.arff;")
            
            
allac("/tmp/lixo999",1)