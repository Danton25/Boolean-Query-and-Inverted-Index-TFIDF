#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 17:10:43 2019

@author: nikhilyadav
"""
import operator
import sys

def create_postings(file1, file2):
    dict1 = dict()              #inverted dictionary
    dict2 = dict()              #documents containing terms
    dict3 = dict()              #tf-dictionary
    dict4 = dict()              #df-dictionary
    words_in_docs = dict()
    tfidf = dict()
    total_docs = 0               

    for line in file1:
        total_docs += 1                     #getting total number of docs for idf
        content = line.split('\t')
        docid = content[0]                  
        text = content[1].strip().split()

        
        dict3[docid] = dict()               #tf-dictionary
 
        for word in text:                       #creating inverted index

            if word not in dict1:
                dict1[word] = [docid]
            else:
                if(docid not in dict1[word]):
                    dict1[word].append(docid)
#============================TF CALCULATIONS===================================

            if word not in dict3[docid]:        #creating tf-dictionary with term frequencies
                dict3[docid][word] = 1
            else:
                dict3[docid][word] += 1 
  
             
            
            if word not in dict2:               #creating dictionary for documents containing term
                
                dict2[word] = 1
            else:
                if docid in dict1[word]:
                    dict2[word] = len(dict1[word])
                    
    for docs in dict3:                          #creating tf for terms
        words_in_docs[docs] = 0
        for words in dict3[docs]:
            words_in_docs[docs] = words_in_docs[docs] + dict3[docs][words]
            
            
    for docs in dict3:                          #finding tf
        for words in dict3[docs]:
            dict3[docs][words] = dict3[docs][words]/words_in_docs[docs]            
            
#===========================IDF CALCULATIONS===================================            
    
    
    for terms in dict1.keys():                  #idf
        dict4[terms] = total_docs/dict2[terms]
    
#===========================TF-IDF=============================================
     
    for docs in dict3:
        tfidf[docs] = dict()
        for words in dict3[docs]:
            tfidf[docs][words] = dict3[docs][words] * dict4[words]
           
    return dict1, tfidf

def operations(file2, dict1, tfidf,output_file):
    
    content = file2.readlines()
    for line in content:
        count_or = 0
        count_and = 0
        txt = line.strip().split(' ')

        get_postings(txt, dict1)
#==========================LIST CREATION FOR AND/OR OPERATIONS=================
        list1 = list()
        list2 = list()
        and_list = list()
        or_list = list()
        for i in range(0, len(txt)-1):
            
            list1 = (dict1[txt[i]])            
            list2 = (dict1[txt[i+1]])

            
            if and_list == []:
                and_list = list1

            and_list, count_and = and_op(and_list,list2,count_and)  #AND op
            if or_list == []:
                or_list = list1
            or_list, count_or = or_op(or_list, list2,count_or)      #OR op

#===========================AND OP FORMATTING==================================

        output_file.write("DaatAnd\n")
        for z in txt:
            output_file.write(z+" ")
        output_file.write("\n")
        output_file.write("Results: ")
        
        if and_list == []:
            output_file.write("empty")
        else:
            for k in and_list:
                output_file.write(k+" ")
        output_file.write("\n")
        output_file.write("Number of documents in results: "+str(len(and_list))+"\n")
        output_file.write("Number of comparisons: "+ str(count_and)+"\n")
        
        
        ranked_and = ranking(dict1, tfidf, line, and_list)
        output_file.write("Results: ")
        if(ranked_and) == []:
            output_file.write("empty\n")
        else:
            for i in ranked_and:
                output_file.write(i+" ")
            output_file.write("\n")
        
        
#===========================OR OP FORMATTING===================================
            
        output_file.write("DaatOr\n")
        for y in txt:
            output_file.write(y+" ")
        output_file.write("\n")
        output_file.write("Results: ")
        if or_list == []:
            output_file.write("empty\n")
        else:
            for l in or_list:
                output_file.write(l+" ")
            output_file.write("\n")
        output_file.write("Number of documents in results: "+str(len(or_list))+"\n")
        output_file.write("Number of comparisons: "+ str(count_or)+"\n")
        ranked_or = ranking(dict1, tfidf, line, or_list)
        output_file.write("Results: ")
        if(ranked_or) == []:
            output_file.write("empty\n")
        else:
            for i in ranked_or:
                output_file.write(i+" ")
            output_file.write("\n")
        output_file.write("\n")

#===========================SCORING AND RANKING================================
def ranking(dict1, tfidf, line, list1):
 
    unranked = dict()
    ranked = []

    text = line.strip().split(' ')
    for docs in list1:
        unranked[docs] = 0
        for words in text:
            if docs in dict1[words]:
                unranked[docs] += tfidf[docs][words] 
                
    scores = sorted(unranked.items(), key = operator.itemgetter(1), reverse = True)
    output_file.write("TF-IDF:\n")
    for r in (scores):
        ranked.append(r[0])
    
    return ranked
#===========================GET POSTINGS=======================================
def get_postings(input1, dict1):

    
    for k,v in dict1.items():

        if k in input1:
            
            output_file.write("GetPostings\n")
            output_file.write(k+"\n")
            output_file.write("Postings list: ")
            for v1 in v:
                output_file.write(v1+" ")
            output_file.write("\n")

#===========================AND OP=============================================
def and_op(list1, list2, count):
    and_list = list()
    i = 0
    j = 0
    
    
    while(list1 != [] and list2 != []):
        
        try:
            if(list1[i] == list2[j]):
                count += 1
                and_list.append(list1[i])
                i += 1
                j += 1
            else:
                
                if(list1[i] > list2[j]):
                    count += 1
                    j += 1
                else:
                    count += 1
                    i += 1
        except:
            break

    return and_list, count
        
 #===========================OR OP=============================================       
    
def or_op(list1, list2,count):
    or_list = list()
    i = 0 
    j = 0
    
    len1 = len(list1)
    len2 = len(list2)

    while(list1 != [] and list2 != []):
        try:
            
            
            if(list1[i] == list2[j]):
                count += 1
                or_list.append(list1[i])
                i += 1
                j += 1
            else:

                count += 1
                if(list1[i] > list2[j]):
                    or_list.append(list2[j])
                    j += 1
                else:
                    or_list.append(list1[i])
                    i += 1
        except:
            break
        
    while(i <len1 and list1[i] != []):
        count += 1

        or_list.append(list1[i])
        i += 1
    while(j < len2 and list2[j] != []):
        count += 1
        or_list.append(list2[j])
        j += 1
    return or_list, count
    
if __name__ == "__main__":
    infile1 = sys.argv[1]                   #input corpus
    input_corpus = open(infile1)
    
    
    infile2 = sys.argv[2]                   #output file
    output_file = open(infile2, 'w+')
    
    infile3 = sys.argv[3]                   #query file      
    query_file = open(infile3)
    
    
    dict1, tfidf = create_postings(input_corpus, query_file)
    operations(query_file, dict1, tfidf,output_file)
    lines = output_file.readlines()
    for lines in output_file:
        output_file.write(lines[:-2])


    input_corpus.close()
    output_file.close()
    query_file.close()
    