'''This code generates a BOW from the text of a file 
   and outputs the most frequently occuring words, 
   along with the sentence array which indicates if a sentence posessess a particular word or not.
   The variables f and num are user dependent.
   These variables have been declared using an initial value for the sake of simplicity
'''
import nltk
import numpy as np
import string
import re
import heapq

bow={}
maxbow={}
data=''

#count occurences of words and add to bag
def word_count (sentence):
  for word in sentence:
    if word in bow:
      bow[word]+=1
    else:
      bow[word]=1

#remove capital letters, white spaces and punctuations
def stringclean(s):
    s=s.lower()
    s=re.sub(r'\W',' ',s)
    s=re.sub(r'\s+',' ',s)    
    return s

#path of file to check
fname=r'C:\Users\barba\Documents\a.txt'

f=open(fname,'r')

for line in f:
   data+=line.strip()

txt = nltk.sent_tokenize(data)

#clean up the data
for i in range(len(txt)):
  txt[i]=stringclean(txt[i])

#create bag
for item in txt:
  tokens=nltk.word_tokenize(item)
  word_count(tokens)

#minimum number of occurences of word to be included in bag
num=10
#create bag with frequently occuring words
maxbow=heapq.nlargest(num,bow, key=bow.get)
print("Vector indices: ", maxbow)

#bow=sorted(bow)
senvec=[]
for sen in txt:
  token=nltk.word_tokenize(sen)
  tempsenvec=[]
  for word in maxbow:
    if word in token:
      tempsenvec.append(1)
    else:
      tempsenvec.append(0)
  senvec.append(tempsenvec)

senarr=np.asarray(senvec)

print('Sentence vectors:')

temp=0
for sen2 in txt:    
    print(sen2,": ")
    print(senarr[temp])
    temp+=1

temp=0