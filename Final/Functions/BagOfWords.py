#!/usr/bin/env python
# coding: utf-8

# In[2]:

def lcs(seq1 , seq2):
    
    n1 = len(seq1)                                                               #Length of sequences (n2>=n1)   
    n2= len(seq2)

    L = [[0 for seq1 in range(n2+1)] for iter in range(n1+1)]                    #Create 2D array to store values

    for iter1 in range(n1+1):
        for iter2 in range(n2+1):
            if iter1 == 0 or iter2 == 0 :
                L[iter1][iter2] = 0
            elif abs(seq1[iter1-1] - seq2[iter2-1]) < 3:                 #If elements match or are close to each other
                L[iter1][iter2] = 1+L[iter1-1][iter2-1]
            else:
                L[iter1][iter2] = max(L[iter1-1][iter2] , L[iter1][iter2-1])    #If elements do not match
    return L[n1][n2] 


def generateBOW(file):
    update_line=[]
    for line in file:
        #remove whitespaces from start and end and convert to lower characters
        update_line.append(line.lower().strip())

    remove_char = [';','#','/*','*/','@','~']
    update_line_document=[]
    [update_line_document.append(''.join((filter(lambda i: i not in remove_char, line))).strip()) for line in update_line] ;

    document_lines = []
    [document_lines.append(line.split(' ')) for line in update_line_document];


    document_words = []
    for i in document_lines:
        for j in i:
            document_words.append(j)


    from collections import Counter
    # BOL = [Counter(lines) for lines in document_lines]
    BOW = Counter(document_words)

    return list(BOW.values())


def BOWComparison(f1, f2):
    bow_f1 = generateBOW(f1)
    bow_f2 = generateBOW(f2)

    if len(bow_f1) + len(bow_f2) == 0:
        return 100
    
    return 200*(lcs(bow_f1,bow_f2))/(len(bow_f1) + len(bow_f2))

# In[ ]:
if __name__ == "__main__":
    fname1=r'./original.txt'                              #Path for original file
    fname2=r'./copy.txt'                                  #Path for file that is being checked for plagiarism (copy)

    # Read the files
    f1 = open(fname1, 'r')
    f2 = open(fname2, 'r')

    print("Percentage BOW match = ", BOWComparison(f1, f2))

    # Close the files
    f1.close()
    f2.close()

