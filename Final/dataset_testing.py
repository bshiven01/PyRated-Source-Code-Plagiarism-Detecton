import subprocess
import re
from Multi_Layer_Comparison import multiLayerComparison, indentComparison, varAndOperCount, functionSignatureComp, exe_comp, ksc, ASTmatch, BOWComparison


functions = ["multiLayerComparison","BOWComparison","indentComparison","varAndOperCount","functionSignatureComp","keywordSeqCom","exe_comp", "ASTmatch"]
n_funcs = len(functions)
start = 0
end = start+8

def func_num(x, f1, f2):
    if x==0: return multiLayerComparison(f1,f2,1)
    elif x==1: return BOWComparison(f1,f2)
    elif x==2: return indentComparison(f1,f2)
    elif x==3: return varAndOperCount(f1,f2)
    elif x==4: return functionSignatureComp(f1,f2)
    elif x==5: return ksc(f1,f2)
    elif x==6: return exe_comp(f1,f2)
    elif x==7: return ASTmatch(f1,f2)

with open('truth2.txt', 'r') as f:
	plag_files_str = f.read()
#print("%r"%plag_files_str)
plag_files = plag_files_str.split('- ')
plag_files.pop(0)
for i in range(len(plag_files)):
    plag_files[i] = plag_files[i].split('\n')
    plag_files[i].pop()
    try:
        t = [plag_files[i][0]]
    except:
        print(plag_files)
        assert Error
    for x in plag_files[i][1:]:
        t.append(x.split(','))
    plag_files[i] = t

c_pos,c_neg, f_pos, f_neg, error, avg_plag, avg_nplag = [0 for i in range(n_funcs)], [0 for i in range(n_funcs)], [0 for i in range(n_funcs)], [0 for i in range(n_funcs)], [0 for i in range(n_funcs)], [0 for i in range(n_funcs)], [0 for i in range(n_funcs)]

thresholds = [None, 65, 65, 65, 75, 85, 85, 45]
data_folder = 'dataset3'

for assignment in plag_files:
    
    folder = assignment[0]
    #print(folder)
    
    process_list_files = subprocess.run(f"ls {data_folder}/{folder}", shell=True, executable='/bin/bash', stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    print(process_list_files.stderr)

    test_files_str = process_list_files.stdout.decode('ascii')
    #print(test_files_str)
    test_files = test_files_str.split('\n')
    test_files.pop()
    n_files = len(test_files)
    
    for i in range(n_files):
        for j in range(i+1, n_files):
            #print(i,j)
            x = test_files[i]
            y = test_files[j]
            #print(x,y)
            # Be VERY careful about format of file to be sent, extensions, address, and all.
            plagiarised = [None for i in range(n_funcs)]
            for k in assignment[1:]:
            #print(x,y,k,sep = '\n')
                if (x[:-4] in k) and (y[:-4] in k):
                    actually_plagiarised = True
                    break
                else:
                    actually_plagiarised = False
            
            for v in range(start, end):
                try:
                    if v==0 or v==6:
                        value = func_num(v, data_folder+'/'+folder+'/'+x ,data_folder+'/'+folder+'/'+y)
                    else:
                        with open(data_folder+'/'+folder+'/'+x, 'r') as f1, open(data_folder+'/'+folder+'/'+y, 'r') as f2:
                            value = func_num(v, f1, f2)
                    #print('RESULT:',value,x,y)
                    
                    if v>0:
                        if value>thresholds[v]:
                            plagiarised[v] = True
                        else: plagiarised[v] = False
                    else:
                        plagiarised[v] = value[0]
                    #print(plagiarised[v])
                    
                    if actually_plagiarised:
                        if v!=0: avg_plag[v] += value
                        if plagiarised[v] == actually_plagiarised:
                            c_pos[v] += 1
                        else:
                            f_neg[v] += 1
                    else:
                        if v!=0: avg_nplag[v] += value
                        if plagiarised[v] == actually_plagiarised:
                            c_neg[v] += 1
                        else:
                            f_pos[v] += 1
                    
                except ZeroDivisionError:
                    print(functions[v],folder, x, y, '/0')
                    error[v] += 1
                '''
                except:
                    print(functions[v],folder, x, y, 'ERROR\n\n\n')
                    error[v]+=1'''
print('\n')
perc, perc_plag, perc_nplag = [0 for i in range(n_funcs)], [0 for i in range(n_funcs)], [0 for i in range(n_funcs)]

for i in range(start, end):
    try:
        perc[i] = 100*(c_pos[i] + c_neg[i])/(c_pos[i] + c_neg[i]+f_pos[i]+f_neg[i])
        perc_plag[i] = 100*c_pos[i]/(c_pos[i]+f_neg[i])
        perc_nplag[i] = 100*c_neg[i]/(c_neg[i]+f_pos[i])
        print(f"{functions[i]}: {perc_plag[i]}% of plag pairs and {perc_nplag[i]}% of non-plag pairs correctly identified. Tested {c_pos[i] + c_neg[i]+f_pos[i]+f_neg[i]} pairs. {error[i]} pairs gave an error.")
        if i!=0:
            print(f"On plag pairs, avg perc match was {avg_plag[i]/(c_pos[i] + f_neg[i])}%, and on non-plag pairs, it was {avg_nplag[i]/(c_neg[i]+f_pos[i])}%.")
        print("\n")
    except ZeroDivisionError:
        print(c_pos[i],c_neg[i],f_pos[i],f_neg[i],error[i])
    #print(c_pos[i],c_neg[i],f_pos[i],f_neg[i],error[i])
