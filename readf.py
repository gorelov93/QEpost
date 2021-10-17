#!/usr/bin/python
#SBATCH -N1 -n10
#SBATCH --time=11:29:00        
#SBATCH --error Py.err  
#SBATCH --output Py.out  
#SBATCH --mem=86000
#SBATCH --account=IscrB_MMCRHY
#SBATCH --partition=knl_usr_prod

#module purge 
#module load profile/base
#module load intel 
#module load mkl
#module load python/2.7.12
#module load numpy/1.11.2--python--2.7.12

import sys
import os
import numpy
from multiprocessing import Process, Array
from multiprocessing import Pool

sys.path.append(os.getcwd())

#c=numpy.zeros((40,11099900,2))
siz=1696878
nproc=10
name=0
def f2numpy(name,c,a):
    print(os.getpid())
    with open(name) as f:
        n=0
        for line in f:
            tmp=numpy.fromstring(line.replace(') (',',')[2:-2],sep=',')
            if tmp.shape[0]==4:
                c[a*siz*2+n]=tmp[0]
                c[a*siz*2+n+1]=tmp[1]
                c[a*siz*2+n+2]=tmp[2]
                c[a*siz*2+n+3]=tmp[3]
                n+=4
            else:
                c[a*siz*2+n]=tmp[0]
                c[a*siz*2+n+1]=tmp[1]
                n+=2

def f(c,a):
    for i in range(2):
        c[a*2+i]=a*2+i

if __name__ == '__main__':
    jobs=[]
    c=Array('d',siz*2*nproc)
    for i in range(nproc):
#        p = Process(target=f,args=(i,))
#        jobs.append(p)
#        p.start() 
        tmp=Process(target=f2numpy, args=(('../c%d/vdW_pwscf/psi_grad_psi-k0_b%d.dat' % ((i+1),name)),c,i))
#        tmp=Process(target=f,args=(c,i))
        tmp.start()
        jobs.append(tmp)
    for a in jobs:
        a.join()
 
    with open('../ca/vdW_pwscf/psi_grad_psi-k0_b%d.dat' % name,'w') as f:
        for x in numpy.average(numpy.asarray(c).reshape(nproc,siz,2),axis=0):
            if x[0]!=0.0 or x[1]!=0.0:
                f.write(' ('+','.join(map(str,x))+')\n')
