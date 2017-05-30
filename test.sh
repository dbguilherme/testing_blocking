 #!/bin/bash

COUNTER=0.1
echo "" > saidaTeste01
 for i in `seq 1 9`;
        do
                echo 'DySimII2013.py t '$COUNTER' 8 1 '$1
                python DySimII2013.py t $COUNTER 8 1 $1 &>> saidaTeste01
                echo $i
                COUNTER=$(python -c "print $COUNTER+0.1")
                
        done    
        