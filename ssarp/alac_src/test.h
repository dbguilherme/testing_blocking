#ifndef _TEST_
#define _TEST_

#include <stdio.h>
#include <string.h>
#include <set>

#include "limits.h"
#include "training.h"
#include "itemset.h"
#include "timer.h"
#include "list.h"

using namespace std;

extern long N_TRANSACTIONS, N_TESTS;
extern int MODE, MIN_FC;
extern map<string, int> CLASS_NAME;
extern map<string, int> ITEM_MAP;
extern map<int, string> SYMBOL_TABLE;
extern list_t* TEST;


int project_training(int* items, int n_items, int* n_transactions);
int read_test_set(char* test);

#endif
