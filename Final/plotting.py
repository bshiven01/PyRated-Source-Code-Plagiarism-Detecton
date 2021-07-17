import subprocess, re
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np
from random import randint
from Multi_Layer_Comparison import multiLayerComparison

n_funcs = 6

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
    axes.hlines(y=i,xmin=0,xmax=7,color=(0.8,0.8,0.8))
s_plot = axes.scatter([0,0.1],[0,0], s=5, c=['green','red'])
fig.canvas.draw()

p_percs = [[] for i in range(n_funcs)]
n_percs = [[] for i in range(n_funcs)]
thresholds = [80, 90, 75, 85, 78, 92]
error = 0
tested = 0

for assignment in plag_files:
    
    folder = assignment[0]
    #print(folder)
    
    process_list_files = subprocess.run(f"ls dataset3/{folder}", shell=True, executable='/bin/bash', stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    print(process_list_files.stderr)

    test_files_str = process_list_files.stdout.decode('ascii')
    #print(test_files_str)
    test_files = test_files_str.split('\n')
    test_files.pop()
    n_files = len(test_files)
    for i in range(n_files):
        for j in range(i+1, n_files):
            #print(i,j)
            try:
                x = test_files[i]
                y = test_files[j]
            except:
                print(test_files, i, j)
            #print(x,y)
            # Be VERY careful about format of file to be sent, extensions, address, and all.
            
            for k in assignment[1:]:
            #print(x,y,k,sep = '\n')
                if (x[:-4] in k) and (y[:-4] in k):
                    actually_plagiarised = True
                    break
                else:
                    actually_plagiarised = False
         
            try:
                t = multiLayerComparison( 'dataset3/'+folder+'/'+x,'dataset3/'+folder+'/'+y, 1)
                for j in range(n_funcs):
                    temp = t[j+1]
                    if temp == None:
                        break
                    if actually_plagiarised:
                        p_percs[i].append(round(temp,2))
                        addPoint(s_plot, [j+1,temp], 'green')
                    else:
                        n_percs[i].append(round(temp,2))
                        addPoint(s_plot, [j+1.1,temp], 'red')
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
    #print(p_percs[i], n_percs[i])
plt.show()
