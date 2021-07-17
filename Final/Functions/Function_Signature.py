#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import sys
from collections import Counter

def lines_words(file,error_flag=False):
    try:
        updated_lines = []
        change_words={"*/":"*/;"}
        for line in file:
            line = line.lstrip()
            if(not line.startswith("//") and line!="\n"  and not line.startswith('#') and not line.startswith('using')):
                updated_lines.append(line.lower().strip())
            try:
                if(line.startswith("#define")):
                    words = line.split(' ')
                    #print(words)
                    replace = words[1]
                    string = ""
                    for i in range(2,len(words)):
                        string += words[i]
                        string += " "
                    string = string[:-2]
                    #print(string)
                    change_words[replace.lower().strip()] = string.lower().strip()
                if(line.startswith("typedef")):
                    words = line.replace("std::","").split(' ')
                    #print(words)
                    replace = words[-1:]
                    repl=replace[0].strip("\n").strip(";")
                    rep=repl.lower()
                    string = ""
                    for i in range(1,len(words)-1):
                        string += words[i]
                        string += " "
                    string = string[:-1]
                    #print(string,rep,type(string),type(rep))
                    change_words[rep] = string.lower().strip()
            except:
                print(sys.exc_info()[0])
        code=""
        for i in range(len(updated_lines)):
            updated_lines[i]=updated_lines[i].replace("std::","")
            code += updated_lines[i]

        code = code.translate({ord("}"):"}; ",ord("("):" ( ",ord("{"):" { ;",ord(">"):"> ",ord("*"):" * "})
        for key,value in change_words.items():
            code=code.replace(key,value)
        #print(code)
        lines_code=code.split(';')
        #print(lines_code)
        return lines_code
    except:
        print(sys.exc_info()[0])
        error_flag=True
        return []


# In[2]:


def hashmap_function(lines_code,hashmap,error_flag=False):
    try:
        pattern ="\((.*?)\)"
        for i in range(len(lines_code)): 
            if ('{'in lines_code[i] and '(' in lines_code[i] and ')' in lines_code[i] and not('for ' in lines_code[i]) 
                and not('while ' in lines_code[i]) and not('main' in lines_code[i]) and not('if ' in lines_code[i])):

                substring = re.search(pattern, lines_code[i]).group(1)
                #print(substring)
                count_parameter=[]
                type_parameter=[]
                parameters = substring.split(',')
                # print(parameters)
                parameter_type = [re.sub('\s+', ' ', i.strip().rsplit(' ', 1)[0]) for i in parameters]
                # print(parameter_type)
                #parameter_type=parameter_type.replace(' ','')
                count_parameter_all = dict(Counter(parameter_type))
                # print(count_parameter_all)
                for key,value in count_parameter_all.items():
                    if key != "":
                        count_parameter.append(value)
                        type_parameter.append(key.replace(' ',''))

                #print(lines_code[i])
                words = lines_code[i].strip().split()
                if(words[0]=='static' or words[0]=='inline'):
                    words[0]=''
                return_type=""
                #print(words)
                for j in range(len(words)):
                    if(words[j]=='('):
                        for k in range(j-1):
                            return_type +=words[k]
                            return_type +=" "
                        break
                #print(return_type)
                function_signature=(return_type.replace(' ',''),tuple(count_parameter),tuple(type_parameter))
                # print(function_signature)
                # print('======================================')
                hash_value=hash(function_signature)
                if hash_value not in hashmap:
                    hashmap[hash_value]=1
                else:
                    hashmap[hash_value]+=1
    except:
        error_flag=True
        pass


# In[3]:


def common_percentage(hashmap1,hashmap2,error_flag=False):
    common=[min(hashmap1[i],hashmap2[i]) for i in hashmap1 if i in hashmap2]
    
    try:
        val = (2*sum(common)/(sum(hashmap1.values())+sum(hashmap2.values())))*100
        if(not error_flag):
            return val
        elif (val!=0):
            return val
        else:
            return 100
    except:
        return 100

def functionSignatureComp(f1, f2):
    hashmap1={}
    hashmap2={}
    error_flag = False
    lines_code1=lines_words(f1,error_flag)
    lines_code2=lines_words(f2,error_flag)
    hashmap_function(lines_code1,hashmap1,error_flag)
    hashmap_function(lines_code2,hashmap2,error_flag)

    return common_percentage(hashmap1,hashmap2,error_flag)

# In[7]:

if __name__ == "__main__":
    fname1=r'./q02.cpp'                              #Path for original file
    fname2=r'./q03.cpp'                              #Path for file that is being checked for plagiarism (copy)

    # Read the files
    f1 = open(fname1, 'r')
    f2 = open(fname2, 'r')

    print("Percentage function signature match = ",functionSignatureComp(f1, f2))

    # Close the files
    f1.close()
    f2.close()
