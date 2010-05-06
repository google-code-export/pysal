import pysal.core.FileIO as FileIO
from pysal.weights import W
  
class GalIO(FileIO.FileIO):
    """
    Opens, reads, and writes file objects in GAL format.

    Authors
    -------
    Charles Schmidt <Charles.R.Schmidt@asu.edu>

    Parameters
    ----------


    Returns
    -------


    Notes
    -----


    Examples
    --------

    Let's try to open a GAL with pysal:
    >>> 
    >>> 
    >>> 
    >>> 

    Let's try to read a GAL with pysal:
    >>> 
    >>> 
    >>> 
    >>> 

    Let's try to write a GAL with pysal:
    >>> 
    >>> 
    >>> 
    >>> 

    """
    FORMATS = ['gal']
    MODES = ['r','w']

    def __init__(self,*args,**kwargs):
        FileIO.FileIO.__init__(self,*args,**kwargs)
        self.file = open(self.dataPath, self.mode)

    def read(self, n=-1):
        return self._read()

    def seek(self, pos):
        if pos == 0:
            self.file.seek(0)
            self.pos = 0

    def _read(self):
        if self.pos > 0:
            raise StopIteration
        weights={}
        neighbors={}
        ids=[]
        # handle case where more than n is specified in first line
        header=self.file.readline().strip().split()
        header_n= len(header)
        n=int(header[0])
        if header_n > 1:
            n=int(header[1])
        w={}
        for i in range (n):
            id,n_neighbors=self.file.readline().strip().split()
            n_neighbors = int(n_neighbors)
            neighbors_i = self.file.readline().strip().split()
            weights[id]=[1]*n_neighbors
            neighbors[id]=neighbors_i
            ids.append(id)

        self.pos += 1 
        return W(neighbors,weights,ids)

    def write(self,obj):
        """ .write(weightsObject)

        write a weights object to the opened file.
        """
        self._complain_ifclosed(self.closed)
        if issubclass(type(obj),W):
            IDS = obj.id_order
            for id in IDS:
                if type(id) != int:
                    raise ValueError("GAL file support only integer IDs only. ID: \"%r\" is not of type int."%id)
            self.file.write('%d\n'%(obj.n))
            for id in IDS:
                neighbors = obj.neighbors[id]
                self.file.write('%s %d\n'%(id,len(neighbors)))
                self.file.write(' '.join(map(str,neighbors))+'\n')
            self.pos += 1
        else:
            raise TypeError,"Expected a pysal weights object, got: %s"%(type(obj))
    def close(self):
        self.file.close()
        FileIO.FileIO.close(self)





