import nltk
import string

def lcs(a, b):
    tbl = [[0 for B in range(len(b) + 1)] for A in range(len(a) + 1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            tbl[i + 1][j + 1] = tbl[i][j] + 1 if x == y else max(
                tbl[i + 1][j], tbl[i][j + 1])
    res = []
    i, j = len(a), len(b)
    while i and j:
        if tbl[i][j] == tbl[i - 1][j]:
            i -= 1
        elif tbl[i][j] == tbl[i][j - 1]:
            j -= 1
        else:
            res.append(a[i - 1])
            i -= 1
            j -= 1
    return res[::-1]

def ksc(code1,code2):
    C_Keywords = ['auto', 'double', 'int', 'struct', 'break', 'else', 'long', 'switch', 'case', 'enum', 'register', 'typedef', 'char', 'extern', 'return', 'union', 'continue', 'for', 'signed', 'void', 'do', 'if', 'static', 'while', 'default', 'goto', 'sizeof', 'volatile', 'const', 'float', 'short', 'unsigned' ]
    #print(C_Keywords)
    keyword_sequence1 = []
    keyword_sequence2 = []
    words1 = []
    words2 = []
    lines1 = ''
    lines2 = ''

    for line in code1:
        lines1 += line.strip()
    for line in code2:
        lines2 += line.strip()

    words1 += nltk.word_tokenize(lines1)
    words2 += nltk.word_tokenize(lines2)

    #print(lines1)
    #print(lines2)
    #print(words1)
    #print(words2)

    for word in words1:
        if word in C_Keywords:
            keyword_sequence1.append(word)

    for word in words2:
        if word in C_Keywords:
            keyword_sequence2.append(word)

    #print(keyword_sequence1)
    #print(keyword_sequence2)
    LCS_kw = ''
    LCS_kw = lcs(keyword_sequence1,keyword_sequence2)
    #print(LCS_kw)

    a = len(LCS_kw)
    b = max(len(keyword_sequence1),len(keyword_sequence2))
    if b == 0 :
        return 100
    matching = (a/b)*100
    return matching

if __name__ == '__main__':
    print(ksc(open(r'./Source_code1.txt','r'),open(r'./Source_code2.txt','r')))

