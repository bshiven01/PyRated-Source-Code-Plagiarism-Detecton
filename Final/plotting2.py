import subprocess, re
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np
from random import randint
from Multi_Layer_Comparison import multiLayerComparison

n_funcs = 5

with open('truth.txt', 'r') as f:
	plag_files_str = f.read()
#print("%r"%plag_files_str)
plag_files = plag_files_str.split('- ')

i=0
while i < len(plag_files):
    if re.match('B', plag_files[i]) == None:
        plag_files.pop(i)
        i-=1
    else:
        plag_files[i] = plag_files[i].split('\n')
        plag_files[i].pop()
        t = [plag_files[i][0], re.sub('/','_',plag_files[i][0])]
        for x in plag_files[i][1:]:
            t.append(x.split(','))
        plag_files[i] = t
    i+=1

#print(*plag_files, sep='\n')

def addPoint(scat, new_point, c='k'):
    old_off = scat.get_offsets()
    new_off = np.concatenate([old_off,np.array(new_point, ndmin=2)])
    old_c = scat.get_facecolors()
    new_c = np.concatenate([old_c, np.array(matplotlib.colors.to_rgba(c), ndmin=2)])

    scat.set_offsets(new_off)
    scat.set_facecolors(new_c)

    scat.axes.figure.canvas.draw_idle()


fig, axes = plt.subplots()
axes.yaxis.set_ticks(range(0,101,5))
axes.set_xlim(0, n_funcs+1)

for i in range(0,101,5):
    axes.hlines(y=i,xmin=0,xmax=5,color=(0.8,0.8,0.8))
s_plot = axes.scatter([0,0.1],[0,0], s=5, c=['green','red'])
fig.canvas.draw()

p_percs = [[] for i in range(n_funcs)]
n_percs = [[] for i in range(n_funcs)]
thresholds = [80, 90, 75, 78, 85]
error = 0
tested = 0

for assignment in plag_files:
    
    folder = assignment[1]
    #print(folder)
    
    process_list_files = subprocess.run(f"ls dataset/{folder}", shell=True, executable='/bin/bash', stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    print(process_list_files.stderr)

    test_files_str = process_list_files.stdout.decode('ascii')
    #print(test_files_str)
    test_files = test_files_str.split('\n')
    test_files.pop()
    n_files = len(test_files)
    
    for i in range(n_files//1):
        for j in range(i+1, n_files//1):
            #print(i,j)
            x = test_files[i]
            y = test_files[j]
            #print(x,y)
            # Be VERY careful about format of file to be sent, extensions, address, and all.
            
            for k in assignment[2:]:
            #print(x,y,k,sep = '\n')
                if (x[:-4] in k) and (y[:-4] in k):
                    actually_plagiarised = True
                    break
                else:
                    actually_plagiarised = False
            
            if not actually_plagiarised and randint(0,80)!=1:
                continue
            try:
                t = multiLayerComparison( 'dataset/'+folder+'/'+x,'dataset/'+folder+'/'+y)
                for i in range(n_funcs):
                    if actually_plagiarised:
                        p_percs[i].append(round(t[i],2))
                        addPoint(s_plot, [i+1,t[i]], 'green')
                    else:
                        n_percs[i].append(round(t[i],2))
                        addPoint(s_plot, [i+1.1,t[i]], 'red')
                tested+=1
                    
            except ZeroDivisionError:
                print(folder, x, y, '/0')
                error += 1
            #except:
                #   print(folder, x, y, 'ERROR\n\n\n')
                #   error+=1
print(*p_percs, sep='\n\n')
print(tested)
print(error)
for i in range(n_funcs):
    x=0
    n = len(p_percs[i])
    m=0
    for j in range(n):
        if p_percs[i][j]!=0:
            x+= p_percs[i][j]
            m += 1
    print(f"function {i+1} - {round(x/m,2)}, {round(sum(n_percs[i])/len(n_percs[i]),2)}")
plt.show()
