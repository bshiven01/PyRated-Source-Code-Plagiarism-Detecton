import numpy as np
from array import *
import nltk
import re
fname=r'copy.txt'
words={}
cppkeywords=[
    'include',
    'alignas',
    'alignof',
    'and',
    'and_eq',
    'asm',
    'atomic_cancel',
    'atomic_commit',
    'atomic_noexcept',
    'auto',
    'bitand',
    'bitor',
    'bool',
    'break',
    'case',
    'catch',
    'char',
    'char8_t',
    'char16_t',
    'char32_t',
    'class',
    'compl',
    'concept',
    'const',
    'consteval',
    'constexpr',
    'constinit',
    'const_cast',
    'continue',
    'co_await',
    'co_return',
    'co_yield',
    'decltype',
    'default',
    'delete',
    'include'
    'do',
    'of',
    'on',
    'double',
    'dynamic_cast',
    'else',
    'enum',
    'explicit',
    'export',
    'extern',
    'FALSE',
    'float',
    'for',
    'friend',
    'goto',
    'if',
    'in',
    'inline',
    'int',
    'the',
    'printf',
    'long',
    'mutable',
    'namespace',
    'new',
    'noexcept',
    'not',
    'not_eq',
    'nullptr',
    'operator',
    'or',
    'or_eq',
    'private',
    'protected',
    'public',
    'reflexpr',
    'register',
    'reinterpret_cast',
    'requires',
    'return',
    'short',
    'signed',
    'sizeof',
    'static',
    'static_assert',
    'static_cast',
    'struct',
    'switch',
    'synchronized',
    'template',
    'this',
    'thread_local',
    'throw',
    'TRUE',
    'try',
    'typedef',
    'typeid',
    'typename',
    'union',
    'unsigned',
    'using',
    'virtual',
    'void',
    'volatile',
    'wchar_t',
    'while',
    'xor',
    'xor_eq',
]

def cleanup(s):
    s=s.lower()
    s=re.sub(r'\W',' ',s)
    s=re.sub(r'\s+',' ',s)    
    return s

def checkvar(s):
    flag=0
    if s in cppkeywords or s.isnumeric() or s.startswith('_') :
        flag=1
    return flag

def check_in_code(s,sen):
    flag=0
    if str([iter1.start() for iter1 in re.finditer(s,sen)])<str([iter2.start() for iter2 in re.finditer("//",sen)]):
        flag=1
    return flag

def check_not_comm(s):
    if not s.strip().startswith('#',0,len(s)) and not s.strip().startswith('//',0,len(s)) and not s.strip().startswith('/*',0,len(s)) and not s.strip().endswith('*/',0,len(s)):
        return 1
    else:
        return 0

def wordcount(sentence):
    if check_not_comm(sentence)==1:        
        sentence_words=re.findall(r'\w+', cleanup(sentence))
        for word in sentence_words:  
                if check_in_code(word,sentence)==1 and checkvar(word)==1:          
                    if word in words:
                        words.update({word:words[word]+1})
                    else:
                        words[word]=1          

f=open(fname,'r')   

for file_line in f:
    wordcount(file_line)
    #print(file_line)

f.close()

sorted_words=sorted(words.items(),key=lambda kv:kv[1],reverse=True)
sorted_vars=[]
#print(sorted_words)  
#  
for item in sorted_words:
    sorted_vars.append(item)
''' 
   item_flag=0
    if checkvar(item[0])==0:
        item_flag=1             
    if item_flag==0:'''
    
    
#print(sorted_vars)

#print(checkvar(sorted_vars[0][0]))
for i in range(10):
   print(sorted_vars[i][1]," ",sorted_vars[i][0])

freq_vars=[]

for i in range(2):
    freq_vars.append(sorted_vars[i][0])

print(freq_vars)

'''
comm='//'
use_str=[]
for i in range(2):
    use_str.append('')

print(freq_vars)
for var in freq_vars:
    num=0
    f=open(fname,'r')  
    sc_line=""
    sc_string=""
    found=[]
    flag_dec=0
    use_str[num]+='D'
    flag_dec=1
    for sc_line in f.readlines():
        sc_words=[]
        if sc_line.strip().startswith('#') or sc_line.strip().startswith('//') or len(sc_line.strip())==0 or sc_line.strip().startswith('using') :
            continue
        sc_words=re.findall(r'\w+', sc_line)
        #print(sc_line)        
        sc_string=sc_line.strip().replace(" ","")
        #print(sc_string)
        for iter in sc_string:
            if iter==[j.start() for j in re.finditer(comm,sc_string)][0]:
                break
            found=[k.start() for k in re.finditer(var,sc_string)]
            #print(found,"   ",var)
            for locn in found:
                if sc_string[locn+len(var)]=='+':
                    if sc_string[locn+2]=='+' or sc_string[locn+2]=='=':
                        use_str[num]+='I'
                if sc_string[locn+len(var)]=='-':
                    if sc_string[locn+2]=='-' or sc_string[locn+2]=='=':
                        use_str[num]+='I'
                if sc_string[locn+len(var)]=='=':
                    use_str[num]+='A'
                if sc_string[locn+len(var)]=='=' or sc_string[locn-1]=='+'or sc_string[locn-1]=='-'or sc_string[locn-1]=='/':
                    use_str[num]+='U'
                if sc_string[locn-1]=='*' and flag_dec==1:
                    use_str[num]+='U'                                                           
        #print(use_str[num])        
        #break
    f.close()
    num+=1
    #break

#print(use_str)
#teststr='Allocate memory for (n*n) 1D arrays'
#print(s([j.start() for j in re.finditer('n',teststr)]))
'''