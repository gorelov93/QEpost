import numpy
#import matplotlib
#matplotlib.use('svg')
#import matplotlib.pyplot as plt
eV=27.2114

#confs=numpy.stack((numpy.loadtxt('c%d.xyz' % i,skiprows=7)[:96] for i in range(1,41)))

#confR0=numpy.loadtxt('CMCA12P250.xyz',skiprows=7)

'putting configuration in a unitary box from 0 to 1'
#confs01=confs-numpy.floor(confs) 

'delta R in a periodic cell'
#DeltaR=confs01-confR0-numpy.rint(confs01-confR0) #
Nk=108
PBox=numpy.array([[-2.780116852428872,0.000000000000000,4.806373972677576],
                 [0.000000000000000,9.884202456312384,0.000000000000000],
                 [5.560233704857745,0.00000000000000,0.000000000000000]])
V=numpy.linalg.det(PBox)
BZvec=numpy.stack((numpy.cross(PBox[1],PBox[2])/V,numpy.cross(PBox[2],PBox[0])/V,numpy.cross(PBox[0],PBox[1])/V))
twists=numpy.loadtxt('twistgrid.out')[:Nk]
print(BZvec)

avec1=8.992427774450754E-002
avec2=1.011715416008468E-001
avec3=1.040285260452706E-001
   
Gvec=numpy.asarray([[0,  0,  0],
 [-1,  0,  0],
  [1,  0,  0],
  [0, -1,  0],
  [0,  1,  0],
  [0,  0, -1],
  [0,  0,  1],
 [-1, -1,  0],
 [-1,  1,  0],
  [1, -1,  0],
  [1,  1,  0],
 [-1,  0, -1],
 [-1,  0,  1],
  [1,  0, -1],
  [1,  0,  1],
  [0, -1, -1],
  [0, -1,  1],
 [ 0,  1, -1],
 [ 0,  1,  1],
 [-1, -1, -1]])*numpy.array([avec1,avec2,avec3])

phase_622=numpy.load('phase.npy')

"folding K vect back in the BZ"
def KvectBZ(Kvect,BZvec):
    M=Nk
    KvecBZ=numpy.zeros((M,3))
    KvecBZprim=numpy.zeros((M,3))
    for theta in range(M):
        tm=(numpy.linalg.solve(numpy.transpose(BZvec),Kvect[theta]))
        KvecBZ[theta]=numpy.dot(numpy.transpose(BZvec),(tm-numpy.round(tm)))
        KvecBZprim[theta]=tm-numpy.round(tm)
    return KvecBZprim,KvecBZ

#N1ovlp_q=numpy.reshape(numpy.loadtxt('N1ovlp_qk.dat'),(40*108,19,4))
#Nm1ovlp_q=numpy.reshape(numpy.loadtxt('Nm1ovlp_qk.dat'),(40*108,19,4))

def getTn_cvk(Rc,Ic,Rv,Iv,DeltaR,K,Nc,nc=40):
    Tc=numpy.reshape((Rc+1j*Ic),(K,Nc))
    Tv=numpy.reshape((Rv+1j*Iv),(K,Nc))
    Ovlp_cv=numpy.zeros((nc,K,96,3),dtype='complex')
    for i in range(nc):
        for j in range(K):
            Ovlp_cv[i,j]=DeltaR[i]*Tv[j,i] *numpy.conjugate(Tc[j,i])
    return numpy.sum(numpy.absolute(numpy.average(Ovlp_cv,axis=0)),axis=(1,2))

#TN1_q =numpy.zeros((19,108))
#TmN1_q =numpy.zeros((19,108))
#for i in range(19):
#    TN1_q[i] =getTn_cvk(N1ovlp_q[:,i,0],
#                          N1ovlp_q[:,i,1],
#                          N1ovlp_q[:,i,2],
#                          N1ovlp_q[:,i,3],DeltaR,108,40,40)
#    TmN1_q[i] =getTn_cvk(Nm1ovlp_q[:,i,0],
#                          Nm1ovlp_q[:,i,1],
#                          Nm1ovlp_q[:,i,2],
#                          Nm1ovlp_q[:,i,3],DeltaR,108,40,40)
Nb=phase_622.shape[1]
print(Nb)
K_cv=numpy.zeros((Nb,Nk,3))
K_Check=numpy.zeros(Nk)
for j in range(Nb):
    for i in range(Nk):
        K_cv[j,i]=KvectBZ(twists+phase_622[:,j].real/(2*numpy.pi),BZvec)[1][i] #Gvec[Gvecind[numpy.argmax(TN1_q[Gvecind],axis=0)]]

#IndDir=numpy.zeros((Nb-48,48,Nk))
#for i in range(48):
#    for j in range(48,Nb):
#        IndDir[j-48,i]=[1 if numpy.sum(abs(K_cv[j,k]-K_cv[i,k]),axis=0)<1e-2 else 0 for k in range(Nk)]
#IndDir2=numpy.where(numpy.sum(abs(K_cv[2]-K_cv[0]),axis=1)<1e-2)
#IndDir3=numpy.where(numpy.sum(abs(K_cv[3]-K_cv[0]),axis=1)<1e-2)
#IndDir42=numpy.where(numpy.sum(abs(K_cv[48]-K_cv[42]),axis=1)<1e-2)
#IndDir5=numpy.where(numpy.sum(abs(K_cv[1]-K_cv[4]),axis=1)<1e-2)
#IndDir6=numpy.where(numpy.sum(abs(K_cv[2]-K_cv[4]),axis=1)<1e-2)

#print(IndDir1,IndDir2,IndDir3,IndDir4,IndDir5,IndDir6)
#numpy.save('IndDir_CMCA12T200P250',IndDir)
#numpy.save('IndDir2_CMCA12T200P250',IndDir2)
#numpy.save('IndDir3_CMCA12T200P250',IndDir3)
#numpy.save('IndDir42_CMCA12T200P250',IndDir42)
#numpy.save('IndDir5_CMCA12T200P250',IndDir5)
numpy.save('K_unfld',K_cv)
