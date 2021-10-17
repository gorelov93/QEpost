import numpy
from xml.dom import minidom
eV=27.2114


def getData(filename):
    tmp=minidom.parse(filename)
    vals=tmp.getElementsByTagName('EIGENVALUES')
    occ=tmp.getElementsByTagName('OCCUPATIONS')
    return numpy.fromstring(vals[0].firstChild.data,dtype=float,sep='\n')


eigvP500=numpy.stack((getData('pwscf/H.save/K00%03d/eigenval.xml' % i) for i in range(1,109)))

indDirP500=numpy.load('IndDir_CMCA12T200P500.npy')

def getGap(eigv,indDir):
    a=numpy.full((68-48,48,108),numpy.nan)
    b=numpy.full((68-48,48,108),numpy.nan)
    for i in range(48):
        for j in range(68-48):
            for k in range(108):
                if indDir[j,i,k]==1:
                    a[j,i,k]=(eigv[k,48+j]-eigv[k,i])*eV
    dirGapBands=numpy.zeros((108,2),dtype='int')
    dirBand=numpy.zeros((108,2))
    for i in range(108):
        dirGapBands[i]=numpy.unravel_index(numpy.nanargmin(a[:,:,i]), a[:,:,i].shape)
        dirBand[i,0]=eigv[i,dirGapBands[i,1]]*eV
        dirBand[i,1]=eigv[i,dirGapBands[i,0]+48]*eV
    return dirGapBands, dirBand

dirGapBandsP500, dirBandP500 = getGap(eigvP500,indDirP500)

print(numpy.min(dirBandP500[:,1]-dirBandP500[:,0]))
print(numpy.argmin(dirBandP500[:,1]-dirBandP500[:,0]))
print(dirGapBandsP500[numpy.argmin(dirBandP500[:,1]-dirBandP500[:,0])])
