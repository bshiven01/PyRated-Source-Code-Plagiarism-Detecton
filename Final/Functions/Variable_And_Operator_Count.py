import re
import math

# To count the operators
def countOperators(s, dict):
    operators = ['+', '-', '*', '/', '%', '++', '--', '==', '!=', '>=', '<=', '>', '<', '&&', '||', '!', '&', '|', '^', '~', '<<', '>>']
    
    for op in operators:
        if len(op) == 1:
            _op = '\\' + op
            pat = '[^' + _op + ']' + _op
            if op in ['!', '<', '>']:
                pat += '[^' + _op + '\=]'
            else:
                pat += '[^' + _op + ']'
            dict[op] = len(re.findall(pat, s))
        else:
            dict[op] = len(re.findall('\\'+'\\'.join(op), s))
    

# To count the variable types
def countVariables(s, dict):
    s = re.sub('[^_]int32|unsigned int|[^n]signed int','int',s)
    s = re.sub('[^_]int64|long long|long long int','long',s)
    dataTypes = ['int','float','char','short','long','double']
    counts = {'int':0,'float':0, 'char':0, 'short':0, 'long':0, 'double':0, 'int1d':0, 'float1d':0, 'char1d':0, 'short1d':0, 'long1d':0, 'double1d':0, 'int2d':0, 'float2d':0, 'char2d':0, 'short2d':0, 'long2d':0, 'double2d':0}
    lines = re.split('\n|;|{|}|\(|\)',s)
    for line in lines:
        if(line):
            line = line.strip(' ')
            for dataType in dataTypes:
                if(line.startswith(dataType)):
                    dimension = line.count('[')
                    if(dimension == 0):
                        counts[dataType] += (line.count(',')+1)
                    else:
                        if(line.count(',') == 0):
                            if(dimension == 1):
                                counts[dataType+'1d'] += 1
                            else:
                                if(dimension == 2):
                                    counts[dataType+'2d'] += 1
                        else:
                            words = line.split(',')
                            for word in words:
                                dim = word.count('[')
                                if(dim == 1):
                                    counts[dataType+'1d'] += 1
                                else:
                                    if(dim == 2):
                                        counts[dataType+'2d'] += 1
    for k,v in counts.items():
        dict[k] = v

# Function to make dictionary with var and operator counts
def makeDict(f):
    dict = {}
    s = f.read()
    to_replace = {}

    for line in f:
        line = line.strip()
        if not line.startswith('#define'):
            continue
        st = line.split()
        to_replace[st[1]] = ' '.join(st[2:])
    
    s = re.sub('#.*\n', '', s)
    s = re.sub('\/\/(.*?)\n', '', s)
    s = re.sub('\"(.*?)\"', '', s)
    s = re.sub('\s+', ' ', s)
    s = re.sub('\/\*(.*?)\*\/', '', s)

    for k,v in to_replace.items():
        s = re.sub('(?:[^a-zA-Z0-9_])' + k + '(?:[^a-zA-Z0-9_])', v, s)

    countOperators(s, dict)
    s = re.sub('\((.*?)\)', '()', s)
    countVariables(s, dict)
    return dict

def varAndOperCount(f1, f2):
    dict1 = makeDict(f1)
    dict2 = makeDict(f2)
    # Write logic to find percent similarity
    cnt = 0
    sz = 0
    for k,v1 in dict1.items():
        v2 = dict2[k]
        va = max(v1,v2)
        vb = min(v1,v2)
        if(va == 0):
            continue
        sz += 1
        if((va-vb) <= math.ceil(0.1*va)):
            cnt += 1

    ret_val = (cnt/sz)*100
    return ret_val

if __name__ == "__main__":
    fname1=r'./original.cpp'                              #Path for original file
    fname2=r'./copy.cpp'                                  #Path for file that is being checked for plagiarism (copy)

    # Read the files
    f1 = open(fname1, 'r')
    f2 = open(fname2, 'r')

    print("Percentage VariableAndOperator match = ", varAndOperCount(f1, f2))

    # Close the files
    f1.close()
    f2.close()

