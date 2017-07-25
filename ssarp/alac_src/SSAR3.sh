
#bin/bash

FOLDER="XXX" # diretorio a ser criado dentro de cada Fold
numfeatures=5 # numero de features no treino / teste
partitions=5 # numero de particoes a ser usado
binsfrom=10 # numero de bins (de) 
binsto=10 # numero de bins (at

treina_arff=$1".arff"
treina_txt=$1".txt"
test_arff=$2
suffix=B$4
flag=$3
numfeatures=$4
	

echo "the file have "$7;
if [ ! -f $treina_arff ]; then
        echo "treinamento nao foi definido";
fi


if [ ! -f $test_arff  ]; then
        echo "teste nao foi definido";
fi
# roda
# gera arquivos contendo os limites dos BINS determinados pelo TUBE

    echo "Produce bins and remove training set"
 #  ../.././gera_bins_TUBE.sh $treina_arff  $numfeatures 10 10

    rm -r result_temp_lac_train_TUBEfinal.txt/
    rm  /tmp/final_treina.txt
      rm  /tmp/final_treina.arff
    rm alac_lac_train_TUBEfinal.txt*
    rm test_nohead.arff
    rm composite_train_un*
    rm saida_SSARP
    grep  @ $treina_arff | grep -v ^$ > /tmp/final_treina.arff

# ../.././gera_bins_TUBE.sh $treina_arff  $numfeatures $binsfrom $binsto
# rm alac_lac_train_TUBEfinal.txt*
#   echo "ONLY Produce bins"
 rm -r result_temp_lac_train_TUBEfinal.txt/ 
 rm -r result_temp_lac_train_TUBE*
 rm composite_train_uniqB$4new
 rm train_nohead.arff


# remove os headers dos arquivos weka
if [ ! -f train_nohead.arff ]; then
    grep -v @ $treina_arff | grep -v ^$ > train_nohead.arff
    
    grep -v @ $treina_arff | grep -v ^$ > train_semNormalizacao_nohead.arff
#     grep -v @ $test_arff | grep -v ^$ > test_nohead.arff
fi 

if [ ! -s train_nohead.arff ]; then
    echo "empty file"
    exit;
fi

if [ -f lac_train_TUBE$suffix.txt ]; then rm -f lac_train_TUBE$suffix.txt; fi
if [ -f lac_train_TUBE$suffix.txt ]; then rm -f lac_train_TUBEfinal.txt; fi


x=$(cat train_nohead.arff | wc -l)

if [ $x -le 5 ]; then
    echo "file almost empty"
    exit;
fi



 # discretiza usando os bins definidos pelo TUBE; os arquivos jah sao gerados no formato LAC
echo "Discretizando treino e teste de acordo com os bins TUBE"
../../discretize_TUBE.pl train-$suffix train_nohead.arff $numfeatures lac_train_TUBE$suffix.txt
echo ../../discretize_TUBE.pl train-$suffix train_nohead.arff $numfeatures lac_train_TUBE$suffix.txt
echo ./updateRows.pl lac_train_TUBE$suffix.txt lac_train_TUBEfinal.txt $3
 ./updateRows.pl lac_train_TUBE$suffix.txt lac_train_TUBEfinal.txt $3
echo " roda o ALAC"
 i=1;
while [ $i -le $5 ]; do
  ../../run_alac_repeated.sh lac_train_TUBEfinal.txt $i

  cat alac_lac_train_TUBEfinal.txt* | awk '{ print $1 }' |  while read instance; do  sed -i  "/^$instance /d" lac_train_TUBEfinal.txt  ;  done
  i=$(($i+1))
done
# junta as instancias selecionadas em cada particao em um arquivo unico contendo todas as features
# echo "Gerando o treino a partir das instancias selecionadas em cada particao.."

./scriptRemoveRows.pl alac_lac_train_TUBEfinal.txt1 composite_train_uniqB$4new composite_train_uniqB$4old $3

cat alac_lac_train_TUBEfinal.txt1  > composite_train$suffix.txt



cat composite_train_uniqB$4new | awk '{ print $1 }'  | while read instance; do  sed  -n  "$instance"p  train_semNormalizacao_nohead.arff; done >> /tmp/final_treina.arff;
cp /tmp/final_treina.arff /tmp/teste_apagar.arff
echo "fim do script!!!";