#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 19:29:10 2019

@author: raghebal-ghezi
"""

import os
#import time
from nltk import ngrams

ngram_len = 4


def load_text(file_name):
    # load text file and return a string of its content
    with open(file_name) as file:
        return file.read()
    
def traverse(dir_loc):
    '''
    Walks in the directory, iterates over all files and returns a dictionary of its name 
    and a list of ngram chunks of its content
    
    Arg: location of the directory[String]
    Returns: dictionary File_name[String]:ngram_chunks[List]
    '''
    docs_contents = dict() # keys are docs names: values are ngram chunks of its contents       
    for root, dirs, files in os.walk("./"+str(dir_loc), topdown=False):
       for name in files:
           if name.endswith(".txt"):
               full_name = os.path.join(root, name)
               chunks = [' '.join(i) for i in ngrams(str(load_text(full_name)).split(), ngram_len)]
               docs_contents[name] = list(chunks)
    return docs_contents

           
docs_contents = traverse("docs")
sus_docs_contents = traverse("sus_docs")


def similarity_score(l1,l2, jaccard = False, show_common = False):
    # number of common ngram bet. 1 and 2 / number of ngrams in 1
#    start_time = time.time()
    
    
    common_chuncks = set(l1).intersection(set(l2))
#    if len(common_chuncks) > 0:
#        print(common_chuncks)
    if jaccard:
#        print('It took %s seconds to query jaccard.' %(time.time()-start_time))    
        return len(common_chuncks) / len(set(l1).union(set(l2)))
#    print('It took %s seconds to query len(1).' %(time.time()-start_time)) 
    if  show_common:
        if len(common_chuncks) > 0:
            return str(len(common_chuncks) / len(l1)) + '\t' + ','.join(list(common_chuncks))
        else:
            return str()
    return len(common_chuncks) / len(l1)



with open('report.txt',"w") as file:
    for doc in docs_contents:
        for sus in sus_docs_contents:
            sim = similarity_score(docs_contents[doc], sus_docs_contents[sus], show_common=True)
            # report only documents with matching results
            if len(sim) != 0:
                file.writelines(doc+'\t'+ sus + '\t' +  str(sim)+'\n')


    



            
        

        
        
