import re


from Functions.BagOfWords import BOWComparison
from Functions.indent import indentComparison
from Functions.Function_Signature import functionSignatureComp
from Functions.Variable_And_Operator_Count import varAndOperCount
from Functions.exe_comparison import exe_comp
from Functions.ksc import ksc
from Functions.AST_comp import ASTmatch

def multiLayerComparison(file_name1,file_name2, key=0):
    '''
    Pass file locations starting from the same directory as this functions's file.
    Return True for plagiarised, False for non-plagiarised. If some test not done, whether due to an error or that layer not being reached, None instead of percentage for that test.
    If key == 0, a list returned - [result, percentage_returned_from_test_1, ... (all test functions)].
    If key==2, a dictionary returned - {"Result":result, "BOWComparison": percentage, ...}
    If threshold crossed at any test, then file passed forwards, else declared non-plagiarised.
    If all tests fail to be executed (give some error), None returned.
    Test order: BOWComparison, Indentation Comparison, Variable & Operator Count Comparison, Function Signature, Exe Comparison, Keyword Sequence Comparison, AST Comparison.'''

    perc_list, pass_list = [None for i in range(6)], [None for i in range(6)]
    
    func_layer0 = [BOWComparison]
    func_layer1 = [indentComparison, varAndOperCount, functionSignatureComp]
    func_layer2 = [exe_comp,ksc]
    func_layer3 = [ASTmatch]
    size = [len(func_layer0),len(func_layer1), len(func_layer2), len(func_layer3)]
    
    thresholds = [65,60,60,60,85,85,45]
    
    perc_list, pass_list = [None for i in range(sum(size))], [None for i in range(sum(size))]
    
    for_key_result = ["Result","BOWComparison", "indentComparison", "varAndOperCount", "functionSignatureComp", "exe_comp", "ksc", "ASTmatch"]
    
    def key_result(plag): # Used to return value as per key. 'plag' should be True/False
        if key==0:
            return plag
        elif key==1:
            l = [plag]
            l.extend(perc_list)
            return l
        elif key==2:
            l = [plag]
            l.extend(perc_list)
            return dict(zip(for_key_result, l))
    
    ## LAYER 0
    #  String Comparison
    with open(file_name1, 'r') as f1, open(file_name2, 'r') as f2:
        # Removing comments:
        text1 = re.sub(r"(//.*?$)|(/\*.*?\*\\)","",f1.read(), flags = re.DOTALL|re.MULTILINE)
        text2 = re.sub(r"(//.*?$)|(/\*.*?\*\\)","",f2.read(), flags = re.DOTALL|re.MULTILINE)
        if text1 == text2:
            return key_result(True)
    
    #  Bag Of Words Comparison
    try:
        with open(file_name1, 'r') as f1, open(file_name2, 'r') as f2:
            perc_list[0] = round( func_layer0[0](f1, f2) ,2)
        if perc_list[0] > thresholds[0]:
            pass_list[0] = True
    except:
        print("Error in BOW_comp")
    
    if pass_list[0]==True or pass_list[0]==None:
        pass
    else:
        return key_result(False)
    
    
    ## LAYER 1
    for i in range(3):
        j = i + 1
        try:
            with open(file_name1, 'r') as f1, open(file_name2, 'r') as f2:
                perc_list[j] = round( func_layer1[i](f1, f2), 2)
            if perc_list[j]>thresholds[j]:
                pass_list[j] = True
            else:
                pass_list[j] = False
        except:
            print(f"Error in function #{i} in Layer 1")
        
    if any(pass_list[1:4]):
        pass
    else:
        return key_result(False)
    
    
    ## LAYER 2
    #  EXE COMPARISON
    # ENTER FILENAME INSTEAD OF OPEN() OBJECT.
    i = 4
    try:
        perc_list[i] = round( func_layer2[0](file_name1, file_name2), 2)
        if perc_list[i] > thresholds[i]:
            pass_list[i] = True
    except:
        print("Error in exe_comp")

    #  KEYWORD SEQUENCE COMPARISON
    try:
        with open(file_name1, 'r') as f1, open(file_name2, 'r') as f2:
            perc_list[i+1] = round( func_layer2[1](f1, f2), 2)
        if perc_list[i+1] > thresholds[i+1]:
            pass_list[i+1] = True
    except:
        print("Error in ksc")
    
    if any(pass_list[4:6]):
        pass
    else:
        return key_result(False)
    
    ## LAYER 3
    #  AST COMPARISON
    i = i+2 # = 6
    try:
        with open(file_name1, 'r') as f1, open(file_name2, 'r') as f2:
            perc_list[i] = round( func_layer3[0](f1, f2), 2)
        if perc_list[i]>thresholds[i]:
            pass_list[i] = True
        else:
            pass_list[i] = False
    except:
        print("Error in AST comparison")
    
    if pass_list[6]==True:
        return key_result(True)
    elif pass_list[6]==None and all(pass_list[4:6]):
        return key_reult(True)
    else:
        return key_result(False)

if __name__ == '__main__':
    print(multiLayerComparison('dataset3/Arithmetic/student1.cpp','dataset3/Arithmetic/student5.cpp',2))
