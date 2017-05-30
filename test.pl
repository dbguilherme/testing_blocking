#!/usr/local/bin/perl


    my $counter =0.1;
    
    for (my $i=0; $i <= 9; $i++) {
       print "DySimII2013.py t $counter 8 1 $ARGV[0]\n";
       
       print `python DySimII2013.py t $counter 8 1 $ARGV[0] >> saida$ARGV[0]` ;
       $counter+=0.1;
                
       
    }

$variable = 1;
print "The variable has the value of $variable\n";
