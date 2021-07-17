import subprocess, os, re

def exe_comp(fname1, fname2):
    file_o = fname1
    file_t = fname2
    '''
    Compares the compiled exes of the two source codes to check for plagiarism.
    file_o, file_t are names of the files to be compared, with extensions, as strings. o is original, t is the one to be tested.
    Returns true for plagiarised (>80% match), else false.
    file_o must not be considerably larger than file_t, because the excess length of one file is also counted in difference.
    '''
    subprocess.call("rm original.out test.out", shell=True, executable='/bin/bash', stderr = subprocess.PIPE)
    address_o = os.path.join(os.path.dirname(__file__), os.pardir, file_o)
    address_t = os.path.join(os.path.dirname(__file__), os.pardir, file_t)
    subprocess.call("g++ -std=c++11 "+address_o+" -o original.out", shell=True, executable='/bin/bash')
    subprocess.call("g++ -std=c++11 "+address_t+" -o test.out", shell=True, executable='/bin/bash')

    comp_process = subprocess.Popen('cmp -l original.out test.out', shell=True, executable='/bin/bash', stdout = subprocess.PIPE)
    result, error = comp_process.communicate()
    differ = re.findall(r'\\n', str(result))
    num_diff = len(differ)
    with open('test.out', 'rb') as f:
        total_t = len(f.read())
    with open('original.out', 'rb') as f:
        total_o = len(f.read())
    subprocess.call("rm original.out test.out", shell=True, executable='/bin/bash', stderr = subprocess.PIPE)
    perc = 100 - (num_diff*2/(total_t+total_o)*100)
    return perc
