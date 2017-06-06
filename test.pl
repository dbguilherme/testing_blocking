#!/usr/local/bin/perl


    my $counter =0.9;
    
    for (my $i=5; $i <= 13; $i++) {
        #for (my $i=0; $i <= 9; $i++) {
            print "DySimII2013.py t $counter 8 $i $ARGV[0]\n";
            
            print `python2.7 DySimII2013.py t $counter $i 0 $ARGV[0] >> saida$ARGV[0]` ;
            #$counter+=0.1;
         #}           
       
    }

$variable = 1;
print "The variable has the value of $variable\n";
