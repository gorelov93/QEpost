#!py
import numpy
DIS=numpy.array([[-2.780116852428872,0.000000000000000,4.806373972677576],
                 [0.000000000000000,9.884202456312384,0.000000000000000],
                 [5.560233704857745,0.00000000000000,0.000000000000000]])

Nk=108
Nb=64

BNDphase_62=numpy.reshape(numpy.loadtxt('BNDph.dat'),(Nk,Nb,3,2))
BNDphase_62=BNDphase_62[:,:,:,0]+1j*BNDphase_62[:,:,:,1]
BNDphase_62=numpy.log(BNDphase_62/numpy.absolute(BNDphase_62))*-1j

phase_622=numpy.zeros((Nk,Nb,3),dtype='complex')
for j in range(Nk):
    for i in range(Nb):
        phase_622[j,i]=numpy.linalg.solve(DIS,BNDphase_62[j,i])

#IndQQ62=numpy.zeros((Nk,20))
#for k in range(Nk):
#    a=0
#    for i in range(49,Nb):
#        if numpy.linalg.norm(abs(phase_622[k,48].real)-abs(phase_622[k,i].real))<1e-1:
#            IndQQ62[k,a]=i
#            a+=1

#IndmQQ62=numpy.zeros((Nk,20))
#for k in range(Nk):
#    a=0
#    for i in reversed(range(0,47)):
#        if numpy.linalg.norm(abs(phase_622[k,47].real)-abs(phase_622[k,i].real))<1e-1:
#            IndmQQ62[k,a]=i
#            a+=1
#print(numpy.where(IndQQ62[:,0]==0))
#print(phase_622[numpy.where(IndQQ62[:,0]==0),48:].real/(2*numpy.pi))
#print(IndmQQ62[:,0])
#print(IndQQ62[:,0])
#print(phase_622[0,48:].real/(2*numpy.pi))
numpy.save('phase',phase_622)
#numpy.savetxt('IndmQQ62.dat',IndmQQ62[:,:2]+1,fmt='%d')
#numpy.savetxt('IndQQ62.dat',IndQQ62[:,:2]+1,fmt='%d')
