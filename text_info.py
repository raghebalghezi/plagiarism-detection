#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 08:48:14 2019

@author: raghebal-ghezi
"""

'''
<feature name="artificial-plagiarism" 
translation="false" 
obfuscation="none" 
this_offset="492343" 
this_length="19928" 
source_reference="source-document02400.txt" 
source_offset="122165" 
source_length="20282" />

## Name of the source  => source_reference
## length of the source => source_length
## length of the plagirized text (from suspicious) => this_length
## where does the above start from (in the suspicious)? => this_offset
## where does the above end (in the suspicious)? => "this_offset"+"this_length"
## where does the above start from (in the source)?=> source_offset
## where does the above end (in the source)? => "source_offset"+"source_length"
'''
#NOTE1: to find the plagirzd excerpt from sus, 
#we use "this_offset" to indicate the start, and "this_offset"+"this_length" to indicate the end.
#import xml.etree.ElementTree as et
import os

ngram_len = 5

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
                #chunks = [' '.join(i) for i in ngrams(str(load_text(full_name)).split(), ngram_len)]
                chunks = ngrams(str(load_text(full_name)).split(), ngram_len)
                docs_contents[name] = list(chunks)
    return docs_contents


docs_contents = traverse("docs")
sus_file_name = 'suspicious-document00002.txt'

sus_file_list = ['suspicious-document00246.txt',
  'suspicious-document00009.txt',
  'suspicious-document00008.txt',
  'suspicious-document00006.txt',
  'suspicious-document00007.txt',
  'suspicious-document00005.txt',
  'suspicious-document00010.txt',
  'suspicious-document00004.txt',
  'suspicious-document00001.txt',
  'suspicious-document00003.txt',
  'suspicious-document00002.txt']

def to_xml(sus_file_name):
    xml_name = sus_file_name[0:-3]+"xml"
    with open(xml_name, 'w') as file:
        file.write('''<?xml version="1.0" encoding="UTF-8"?>\n <document ''')
        for i in list(docs_contents.keys()):
            src_file = load_text("docs/"+i)
            sus_file = load_text(sus_file_name)
            sus_ngram_joint_string_set = set(ngrams(sus_file.split(),ngram_len))
            src_ngram_joint_string_set = set(docs_contents[i])
            mutual_excerpts = sus_ngram_joint_string_set.intersection(src_ngram_joint_string_set)
            if len(mutual_excerpts) == 0:
                file.write("<feature "+"source_reference="+'"'+str(i)+'"'+"/>")
            else:
                for k in mutual_excerpts:
    
                    if sus_file.find(' '.join(k)) != -1 and src_file.find(' '.join(k)) != -1:
                        file.write(
                        "<feature "+ "this_length=" + str(len(list(mutual_excerpts)[0])) + " " +
                            "this_offset="+'"'+str(sus_file.find(' '.join(k)))+'"' + " " +
                            "source_offset="+'"'+str(src_file.find(' '.join(k)))+'"' + " " +
                            "source_length="+'"'+str(len(src_file))+'"' + " " +
                            "source_reference="+'"'+ str(i) +'"' +"/>"
    
                        )
    
        file.write(''' </document>''')

for f in sus_file_list:        
    to_xml("./sus_docs/"+f)