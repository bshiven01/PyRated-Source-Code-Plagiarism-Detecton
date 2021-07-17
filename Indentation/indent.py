'''
This code compares two text files for similarity based on the degree of indent match.
fname1, fname2 are the two files being compared. Change path accordingly

'''
from array import *

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
    return L[n1][n2]                                                            #Return length of LCS

# For generationg the array containinbg the size of indentation for each line
def generateArray(f):
    space = []
    for line1 in f:
        ct=0
        
        for char1 in line1:
            if char1==' ':
                ct+=1
            elif char1 == '\t':
                ct+=4
            else:
                break
        space.append(ct)
    return space

def indentComparison(f1, f2):
    #Array containing size of indent for each line 
    space1=generateArray(f1)
    space2=generateArray(f2)

    # #Print sequence of indents for both files
    # print(space1)
    # print(space2)

    if len(space1) + len(space2) == 0:
        return 100
    
    return 200*(lcs(space1,space2))/(len(space1) + len(space2))                           #Calculate Percentage indent match


if __name__ == "__main__":
    fname1=r'./original.txt'                              #Path for original file
    fname2=r'./copy.txt'                                  #Path for file that is being checked for plagiarism (copy)

    # Read the files
    f1 = open(fname1, 'r')
    f2 = open(fname2, 'r')

    print("Percentage indent match = ",indentComparison(f1, f2))

    # Close the files
    f1.close()
    f2.close()

