import operator
import os
import re
from difflib import SequenceMatcher as SM
import difflib
import math
from nltk.tokenize import word_tokenize

def load_text(file_name):
    # load text file and return a string of its content
    with open(file_name,"r") as file:
        return file.read()

def fetch_file_names(directory):
    lst = []
    for root, dirs, files in os.walk(str(directory), topdown=False):
            for name in files:
                if name.endswith(".txt"):
                    lst.append(name)
    return lst
                    
source_files  = fetch_file_names("docs")
suspicious_files = fetch_file_names("sus_docs")

def ngrams(sequence,n):
    #len(seq)-len(n)+1
    sequence = iter(sequence)
    history = []
    while n > 1:
        history.append(next(sequence))
        n -= 1
    for item in sequence:
        history.append(item)
        yield tuple(history)
        del history[0]
        
source_dir = "docs/"
sus_dir = "sus_docs/"
def find_excerpt(source,suspicious,n,theta):
    
    src = str(load_text(source_dir+source)).replace("\n"," ")
    sus = str(load_text(sus_dir+suspicious)).replace("\n"," ")
    
    src_ngram = list(ngrams(src.split(" "),n)) #create a list of ngrams for source text
    sus_ngram = list(ngrams(sus.split(" "),n)) #create a list of ngrams for suspicious text

    src_index = dict() # dict to store indices of ngram chunks of source
    sus_index = dict() # dict to store indices of ngram chunks of suspicious

    
    
    for i in set(src_ngram).intersection(sus_ngram):
        # find intersected ngram chunks between source and suspicious
        concat = " ".join(i) # join the ngram chuncks into full strings
        src_index[concat] = src.find(concat) # find the loc of ngram chunk in source and store in the src_dict
        sus_index[concat] = sus.find(concat) # find the loc of ngram chunk in suspicious and store in the sus_dict
   
    # sort both dictionaries based on ascending indices
    sorted_src = sorted(src_index.items(), key=operator.itemgetter(1))
    sorted_sus = sorted(sus_index.items(), key=operator.itemgetter(1))
    # check the difference between the first index of ngram chunk and the last one, 
    # and if the difference is less than the threshold, 
    # return source_offset (index of 1st common ngram chunk) as well as the difference 
    # between the first and the last ngram source_length
    
    if len(sorted_src) == 0 or len(sorted_sus) == 0:
        return
    
    max_index_src = max([k[1] for k in sorted_src]) 
    for i, j in enumerate(sorted_src):
        if max_index_src - j[1] < theta:
            source_offset = j[1]
            source_length = max_index_src - j[1]
            break


    # check the difference between the first index of ngram chunk and the last one, 
    # and if the difference is less than the threshold, 
    # return source_offset (index of 1st common ngram chunk) as well as the difference 
    # between the first and the last ngram source_length

    max_index_sus = max([k[1] for k in sorted_sus]) 
    for i, j in enumerate(sorted_sus):
        if max_index_sus - j[1] < theta:
            this_offset = j[1]
            this_length = max_index_sus - j[1]
            break

    if source_length < 10 or this_length < 10: # if the length of plagirized content is less than 10 char
        return


    return str("<feature "+ "this_length=" + '"'+ str(this_length) + '"' +
                " this_offset="+'"'+str(this_offset)+'"' +
                " source_offset="+'"'+str(source_offset)+'"' +
                " source_length="+'"'+str(source_length)+'"' +
                " source_reference="+'"'+ str(source) +'"' +"/>")
                

for sus_f in suspicious_files:
    xml_name = sus_f[0:-3]+"xml"
    with open(xml_name, 'w') as f:
        f.write('''<?xml version="1.0" encoding="UTF-8"?>\n <document ''')
        for src_f in source_files:
            if find_excerpt(src_f, sus_f, 5, 240) != None:
                f.write(find_excerpt(src_f, sus_f, 5, 240))
        f.write(''' <document/>''')
    break

 