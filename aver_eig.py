#!/usr/bin/python
import sys
import os
import numpy
from xml.dom import minidom
#sys.path.append(os.getcwd())



def getData(filename):
    tmp=minidom.parse(filename)
    vals=tmp.getElementsByTagName('EIGENVALUES')
    occ=tmp.getElementsByTagName('OCCUPATIONS')
    return numpy.stack((numpy.fromstring(vals[0].firstChild.data,dtype=float,sep='\n'), 
                        numpy.fromstring(occ[0].firstChild.data,dtype=float,sep='\n')))


def writeData(name,data,K):
    f=open(name,'w')
    f.write('<?iotk version="1.2.0"?> \n')
    f.write('<?iotk file_version="1.0"?> \n')
    f.write('<?iotk binary="F"?> \n')
    f.write('<?iotk qe_syntax="F"?> \n')
    f.write('<Root> \n')
    f.write('  <INFO nbnd="68" ik="%d"/> \n' % K)
    f.write('  <UNITS_FOR_ENERGIES UNITS="Hartree"/> \n')
    f.write('  <EIGENVALUES type="real" size="68"> \n')
    f.write(numpy.array2string(data[0],precision=20,separator='\n')[1:-1])
    f.write('\n  </EIGENVALUES>\n  <OCCUPATIONS type="real" size="68">')
    f.write(numpy.array2string(data[1],precision=20,separator='\n')[1:-1])
    f.write('\n  </OCCUPATIONS>\n</Root>')
    f.close()


if __name__ == '__main__':
    c1=numpy.stack((getData('HSE_pwscf/H.save/K00%03d/eigenval.xml' % i) for i in range(1,501)))
    numpy.save('eig_val',c1)
    #aver_data=numpy.average(c1,axis=0)
    #for K in range(1,109):
    #    writeData('ca/vdW_pwscf/H.save/K00%03d/eigenval.xml' % K,aver_data[K-1],K)
