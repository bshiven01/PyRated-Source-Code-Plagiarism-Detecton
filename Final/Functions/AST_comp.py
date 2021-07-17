import re
# In[2]:

class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def insert_left(self, node):
        if self.data:
            if self.left is None:
                self.left = node
            else:
                self.left.insert_left(node)
        else:
            self.data = node.data

    def insert_right(self, node):
        if self.data:
            if self.right is None:
                self.right = node
            else:
                self.right.insert_right(node)
        else:
            self.data = node.data

    def __str__(self):
        return str(self.data)

# In[9]:

def nodes_of_tree(root,nodes_list=[]):
    if root:
        nodes_of_tree(root.left,nodes_list)
        nodes_list.append(root)
        nodes_of_tree(root.right,nodes_list)
    return nodes_list

def preOrder(root,list_preorder=[]):
    if root:
        list_preorder.append(root.data)
        preOrder(root.left,list_preorder)
        preOrder(root.right,list_preorder)
    return list_preorder

def inOrder(root,list_inorder=[]):
    if root:
        inOrder(root.left,list_inorder)
        list_inorder.append(root.data)
        inOrder(root.right,list_inorder)
    return list_inorder

def postOrder(root,list_postorder=[]):
    if root:
        postOrder(root.left,list_postorder)
        postOrder(root.right,list_postorder)
        list_postorder.append(root.data)
    return list_postorder


# In[3]:


def curlybracketcounter(code, i):
    j = i
    stack = []
    while j>(i-1):
        if('{' in code[j]):
            stack.append('{')
        if('}' in code[j] and '{' in stack):
            stack.remove('{')
        if(len(stack) == 0):
            k = j
            break
        j+=1
    return k


# In[4]:

def condn(code,i):
    j = i+1
    k = curlybracketcounter(code,j-1)
    c = Node("C")
    cur_node = c
    while j < k:
        if('for' in code[j] or 'while' in code[j]):
            temp = loop(code, j)
            l = temp[0]
            j = temp[1]
            new_node = Node('L')
            cur_node.insert_left(new_node)
            cur_node = new_node
            cur_node.insert_right(l)
            j+=1
            continue
        if('else' in code[j] or 'if' in code[j] or 'elseif' in code[j] or 'switch' in code[j]):
            temp = condn(code, j)
            c = temp[0]
            j = temp[1]
            new_node = Node('C')
            cur_node.insert_left(new_node)
            cur_node = new_node
            cur_node.insert_right(c)
            j+=1
            continue
        if('cout' in code[j] or 'cin' in code[j] or 'break' in code[j]):
            new_node = Node('I')
            cur_node.insert_left(new_node)
            cur_node = new_node
            j+=1
            continue
        if('=' in code[j]):
            a = code[j].find('=')
            if((a-1)>1):
                new_node = Node('D')
                cur_node.insert_left(new_node)
                cur_node = new_node
            else:
                new_node = Node('A')
                cur_node.insert_left(new_node)
                cur_node = new_node
            j+=1
            continue
        if('return' in code[j]):
            new_node = Node('R')
            cur_node.insert_left(new_node)
            cur_node = new_node
            j+=1
            continue
        if('(' in code[j] and ')' in code[j]):
            new_node = Node('I')
            cur_node.insert_left(new_node)
            cur_node = new_node
            j+=1
            continue
        if('}'in code[i]):
            j+=1
            continue
        if('{'in code[i]):
            j+=1
            continue
        new_node = Node('D')
        cur_node.insert_left(new_node)
        cur_node = new_node
        j+=1
    return[c,k]


# In[5]:

def loop(code,i):
    j = i+1
    k = curlybracketcounter(code,j-1)
    l = Node("L")
    cur_node = l
    while j < k:
        if('for' in code[j] or 'while' in code[j]):
            ans = loop(code, j)
            l = ans[0]
            j = ans[1]
            new_node = Node('L')
            cur_node.insert_left(new_node)
            cur_node = new_node
            cur_node.insert_right(l)
            j+=1
            continue
        if('else' in code[j] or 'if' in code[j] or 'elseif' in code[j] or 'switch' in code[j]):
            ans = condn(code,j)
            c = ans[0]
            j = ans[1]
            new_node = Node('C')
            cur_node.insert_left(new_node)
            cur_node = new_node
            cur_node.insert_right(c)
            j+=1
            continue
        if('cout' in code[j] or 'cin' in code[j] or 'break' in code[j]):
            new_node = Node('I')
            cur_node.insert_left(new_node)
            cur_node = new_node
            j+=1
            continue
        if('=' in code[j]):
            a = code[j].find('=')
            if((a-1)>1):
                new_node = Node('D')
                cur_node.insert_left(new_node)
                cur_node = new_node
            else:
                new_node = Node('A')
                cur_node.insert_left(new_node)
                cur_node = new_node
            j+=1
            continue
        if('return' in code[j]):
            new_node = Node('R')
            cur_node.insert_left(new_node)
            cur_node = new_node
            j+=1
            continue
        if('(' in code[j] and ')' in code[j]):
            new_node = Node('I')
            cur_node.insert_left(new_node)
            cur_node = new_node
            j+=1
            continue
        if('}'in code[i]):
            j+=1
            continue
        if('{'in code[i]):
            j+=1
            continue
        new_node = Node('D')
        cur_node.insert_left(new_node)
        cur_node = new_node
        j+=1
    return[l,k]


# In[6]:

def func(code,i):
    Lines_code = code
    j = i+1
    f = Node("F")
    cur_node = f
    k = curlybracketcounter(Lines_code,i)
    while j < k:
        if('for' in Lines_code[j] or 'while' in Lines_code[j]):
            ans = loop(Lines_code, j)
            l = ans[0]
            j = ans[1]
            left = Node('L')
            cur_node.insert_left(left)
            cur_node = left
            cur_node.insert_right(l)
            j+=1
            continue
        if('else' in Lines_code[j] or 'if' in Lines_code[j] or 'elseif' in Lines_code[j] or 'switch' in Lines_code[j]):
            ans = condn(Lines_code,j)
            c = ans[0]
            j = ans[1]
            left = Node('C')
            cur_node.insert_left(left)
            cur_node = left
            cur_node.insert_right(c)
            j+=1
            continue
        if('cout' in Lines_code[j] or 'cin' in Lines_code[j] or 'break' in Lines_code[j]):
            new_node = Node('I')
            cur_node.insert_left(new_node)
            cur_node = new_node
            j+=1
            continue
        if('=' in Lines_code[j]):
            a = Lines_code[j].find('=')
            if((a-1)>1):
                new_node = Node('D')
                cur_node.insert_left(new_node)
                cur_node = new_node
            else:
                new_node = Node('A')
                cur_node.insert_left(new_node)
                cur_node = new_node
            j+=1
            continue
        if('return' in Lines_code[j]):
            new_node = Node('R')
            cur_node.insert_left(new_node)
            cur_node = new_node
            j+=1
            continue
        if('(' in Lines_code[j] and ')' in Lines_code[j]):
            new_node = Node('I')
            cur_node.insert_left(new_node)
            cur_node = new_node
            j+=1
            continue
        if('}'in Lines_code[j]):
            j+=1
            continue
        if('{'in Lines_code[j]):
            j+=1
            continue
        new_node = Node('D')
        cur_node.insert_left(new_node)
        cur_node = new_node
        j+=1
    return[f,k]

# In[14]:

def PreProcess(file):
    s = file.read()
    to_replace = {}

    for line in file:
        line = line.strip()
        if not line.startswith('#define'):
            continue
        st = line.split()
        to_replace[st[1]] = ' '.join(st[2:])
    
    s = re.sub('#.*\n', '', s)
    s = re.sub('using.*\n', '', s)
    s = re.sub('\/\/(.*?)\n', ' ', s)
    s = re.sub('\"(.*?)\"', '', s)
    s = re.sub('\s+', ' ', s)
    s = re.sub('\/\*(.*?)\*\/', '', s)

    for k,v in to_replace.items():
        s = re.sub('(?:[^a-zA-Z0-9_])' + k + '(?:[^a-zA-Z0-9_])', v, s)
    
    s = re.sub('\((.*?)\)', '()', s)
    s = re.sub('\}', '};', s)
    s = re.sub('\{', '{;', s)
    
    return s
# In[7]:

def ASTgenerator(file):

    code = PreProcess(file)
    Lines_code = code.strip().split(';')
    AST = []
    i = 0
    while i <= (len(Lines_code)-1):
        if('{'in Lines_code[i] and '('in Lines_code[i] and not('while' in Lines_code[i]) and not('for' in Lines_code[i])):
            ans = func(Lines_code,i)
            f = ans[0]
            AST.append(f)
            i = ans[1]+1
            continue
        if('cout' in Lines_code[i] or 'cin' in Lines_code[i] or 'break' in Lines_code[i]):
            AST.append(Node('I'))
            i+=1
            continue
        if('=' in Lines_code[i]):
            a = Lines_code[i].find('=')
            if((a-1)>1):
                AST.append(Node('D'))
            else:
                AST.append(Node('A'))
            i+=1
            continue
        if('(' in Lines_code[i] and ')' in Lines_code[i] and not('{' in Lines_code[i])):
            AST.append(Node('I'))
            i+=1
            continue
        if('}'in Lines_code[i]):
            i+=1
            continue
        if(not('{'in Lines_code[i]) or not('}'in Lines_code[i]) or not('for'in Lines_code[i]) or not('while'in Lines_code[i])
        or not('else'in Lines_code[i]) or not('return'in Lines_code[i]) or not('('in Lines_code[i])or not(')'in Lines_code[i])
        or not('='in Lines_code[i]) or not('if'in Lines_code[i]) or not('if'in Lines_code[i]) or not('elseif'in Lines_code[i])
        or not('switch'in Lines_code[i]) or not('cout'in Lines_code[i])or not('cin'in Lines_code[i]) or not('break'in Lines_code[i])):
            AST.append(Node('D'))
            i+=1
            continue
        if i < len(Lines_code):
            i+=1
            continue
    return(AST)

# In[11]:

def TreePreInTraverse(AST, Tree_preorder_inorder_tuples):
    for binary_tree in AST:
        binary_tree_node_list=[]
        nodes_of_tree(binary_tree,binary_tree_node_list)

        for i in binary_tree_node_list:
            preorder_i=[]
            inorder_i=[]
            Tree_preorder_inorder_tuples.append((preOrder(i,preorder_i),inOrder(i,inorder_i)))


# In[10]:
    
def ASTmatch(f1, f2):
    '''Takes in open() objects.'''
    AST1 = ASTgenerator(f1)
    AST2 = ASTgenerator(f2)
    
    Tree1_preorder_inorder_tuples=[]
    Tree2_preorder_inorder_tuples=[]

    TreePreInTraverse(AST1, Tree1_preorder_inorder_tuples)
    TreePreInTraverse(AST2, Tree2_preorder_inorder_tuples)
    
    count=0
    for i in range(len(Tree1_preorder_inorder_tuples)):
        for j in range(len(Tree2_preorder_inorder_tuples)):
            if(Tree1_preorder_inorder_tuples[i]==Tree2_preorder_inorder_tuples[j] and Tree1_preorder_inorder_tuples[i]!=-1):
                count+=1
                Tree1_preorder_inorder_tuples[i]=-1
                Tree2_preorder_inorder_tuples[j]=-1
    
    percentage_common = 2*100*count/((len(Tree1_preorder_inorder_tuples)+len(Tree2_preorder_inorder_tuples)))
    return percentage_common



# In[12]:
import os.path

if __name__ == "__main__":
    file1=r'Source_code1.txt'
    file2=r'Source_code2.txt'

    # Read the files
    f1 = open(os.path.dirname(__file__) + '../dataset/B2016_Z1_Z1/student5420.cpp', 'r')
    f2 = open(os.path.dirname(__file__) + '../dataset/B2016_Z1_Z1/student5533.cpp', 'r')

    print("Percentage AST match = ", ASTmatch(f1, f2))

    # Close the files
    f1.close()
    f2.close()
