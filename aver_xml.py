#!/usr/bin/python

import sys
import os
import numpy
from xml.dom import minidom

def getData(filename):
    tmp=minidom.parse(filename)
    vals=tmp.getElementsByTagName('eigenvalues')
    #occ=tmp.getElementsByTagName('occupations')
    return numpy.stack((numpy.fromstring(vals[i].firstChild.data,dtype=float,sep='\n') for i in range(500)))


if __name__ == '__main__':
    aver_data=numpy.average(numpy.stack((getData('../c%d/pwscf/C.xml' % k) for k in range(1,21))),axis=0)
    numpy.save('aver_eigen',aver_data)
#    for i in range(1,21):
#        data_xml=minidom.parse('../c%d/pwscf/C.xml' % i)
#        for kp in range(500):
#            data_xml.getElementsByTagName('eigenvalues')[kp].childNodes[0].nodeValue='\n '+numpy.array_str(aver_data[kp])[1:-1]+' \n'
            #data_xml.getElementsByTagName('occupations')[kp].childNodes[0].nodeValue='\n '+numpy.array_str(aver_data[kp,1])[1:-1]+' \n'
        #writeData('CA/c%d/pwscf/C.xml' % i,data_xml)
#        with open( "c%d/pwscf/C.xml" % i, "w" ) as fs:
#            fs.write( data_xml.toxml() )
#            fs.close()
#        with open( "c%d/pwscf/C.save/data-file-schema.xml" % i, "w" ) as fs:
#            fs.write( data_xml.toxml() )
#            fs.close()
