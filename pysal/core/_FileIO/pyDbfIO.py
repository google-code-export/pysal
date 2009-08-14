import pysal
import datetime
import struct
import itertools

class DBF(pysal.core.Tables.DataTable):
    """ """
    FORMATS = ['dbf']
    MODES = ['r','w']
    def __init__(self,*args,**kwargs):
        pysal.core.Tables.DataTable.__init__(self,*args,**kwargs)
        if self.mode == 'r':
            self.f = f = open(self.dataPath,'rb')
            numrec, lenheader = struct.unpack('<xxxxLH22x', f.read(32))
            numfields = (lenheader - 33) // 32
            self.n_records = numrec
            self.n_fields = numfields
            self.field_info = [('DeletionFlag', 'C', 1, 0)]
            record_size = 1
            fmt = 's'
            for fieldno in xrange(numfields):
                name, typ, size, deci = struct.unpack('<11sc4xBB14x', f.read(32))
                fmt+='%ds'%size
                record_size+=size
                name = name.replace('\0', '')       # eliminate NULs from string
                self.field_info.append((name, typ, size, deci))
            terminator = f.read(1)
            assert terminator == '\r'
            self.header_size = self.f.tell()
            self.record_size = record_size
            self.record_fmt = fmt
            self.pos = 0
            self.header = [fInfo[1] for fInfo in self.field_info[1:]]
            field_spec = []
            for fname,ftype,flen,fpre in self.field_info[1:]:
                field_spec.append((ftype,flen,fpre))
            self.field_spec = field_spec
            #self.spec = [types[fInfo[0]] for fInfo in self.field_info]
        elif self.mode == 'w':
            self.f = open(self.dataPath,'wb')
            self.header = None
            self.field_spec = None
            self.numrec = 0
            self.FIRST_WRITE = True
    def __len__(self):
        if self.mode != 'r': raise IOError, "Invalid operation, Cannot read from a file opened in 'w' mode."
        return self.n_records
    def seek(self,i):
        self.f.seek(self.header_size + (self.record_size*i))
        self.pos = i
    def read_record(self,i):
        self.seek(i)
        rec = list(struct.unpack(self.record_fmt, self.f.read(self.record_size)))
        if rec[0] != ' ':
            return self.read_record(i+1)
        result = []
        for (name, typ, size, deci), value in itertools.izip(self.field_info, rec):
            if name == 'DeletionFlag':
                continue
            if typ == 'N':
                value = value.replace('\0', '').lstrip()
                if value == '': 
                    value = 0 
                elif deci:
                    value = float(value)
                else:
                    value = int(value)
            elif typ == 'D':
                y, m, d = int(value[:4]), int(value[4:6]), int(value[6:8])
                value = datetime.date(y, m, d)
            elif typ == 'L':
                value = (value in 'YyTt' and 'T') or (value in 'NnFf' and 'F') or '?' 
            elif typ == 'F':
                value = float(value)
            if isinstance(value, str):
                value = value.rstrip()
            result.append(value)
        return result
    def _read(self):
        if self.mode != 'r': raise IOError, "Invalid operation, Cannot read from a file opened in 'w' mode."
        if self.pos < len(self):
            rec = self.read_record(self.pos)
            self.pos+=1
            return rec
        else:
            return None
    def list_dbf(self):
        if self.mode != 'r': raise IOError, "Invalid operation, Cannot read from a file opened in 'w' mode."
        dbf=self.f
        print "%d records, %d fields" % (dbf.record_count(), dbf.field_count())
        format = ""
        for i in range(dbf.field_count()):
            type, name, len, decc = dbf.field_info(i)
            print type,name,len,decc
            if type == 0: #string
                format = format + " %%(%s)%ds" % (name, len)
            elif type == 1: #int
                format = format + " %%(%s)%dd" % (name, len)
            elif type == 2: #float
                format = format + " %%(%s)%dg" % (name, len)
        print format
        for i in range(dbf.record_count()):
            print format % dbf.read_record(i)
    def write(self,obj):
        self._complain_ifclosed(self.closed)
        if self.mode != 'w': raise IOError, "Invalid operation, Cannot write to a file opened in 'r' mode."
        if self.FIRST_WRITE:
            self._firstWrite(obj)
        if len(obj) != len(self.header):
            raise TypeError, "Rows must contains %d fields"%len(self.header)
        self.numrec+=1
        self.f.write(' ')                        # deletion flag
        for (typ, size, deci), value in itertools.izip(self.field_spec, obj):
            if typ == "N":
                value = str(value).rjust(size, ' ')
            elif typ == 'D':
                value = value.strftime('%Y%m%d')
            elif typ == 'L':
                value = str(value)[0].upper()
            else:
                value = str(value)[:size].ljust(size, ' ')
            try:
                assert len(value) == size
            except:
                print value,len(value),size
                raise
            self.f.write(value)
            self.pos+=1
    def flush(self):
        self._complain_ifclosed(self.closed)
        self._writeHeader()
        self.f.flush()
    def close(self):
        if self.mode == 'w':
            self.flush()
            # End of file
            self.f.write('\x1A')
            self.f.close()
        pysal.core.Tables.DataTable.close(self)
    def _firstWrite(self,obj):
        if not self.header: raise IOError, "No header, DBF files require a header."
        if not self.field_spec: raise IOError, "No field_spec, DBF files require a specification."
        self._writeHeader()
        self.FIRST_WRITE = False
    def _writeHeader(self):
        """ Modified from: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/362715 """
        POS = self.f.tell()
        self.f.seek(0)
        ver = 3
        now = datetime.datetime.now()
        yr, mon, day = now.year-1900, now.month, now.day
        numrec = self.numrec
        numfields = len(self.header)
        lenheader = numfields * 32 + 33
        lenrecord = sum(field[1] for field in self.field_spec) + 1
        hdr = struct.pack('<BBBBLHH20x', ver, yr, mon, day, numrec, lenheader, lenrecord)
        self.f.write(hdr)
        # field specs
        for name, (typ, size, deci) in itertools.izip(self.header, self.field_spec):
            name = name.ljust(11, '\x00')
            fld = struct.pack('<11sc4xBB14x', name, typ, size, deci)
            self.f.write(fld)
        # terminator
        self.f.write('\r')
        if self.f.tell() != POS and not self.FIRST_WRITE:
            self.f.seek(POS)

if __name__ == '__main__':
    file_name = "../../weights/examples/usCounties/usa.dbf"
    f=pysal.open(file_name,'r')
    newDB = pysal.open('copy.dbf','w')
    newDB.header = f.header
    newDB.field_spec = f.field_spec
    print f.header
    print f.spec
    for row in f:
        print row
        newDB.write(row)
    newDB.close()
    copy = pysal.open('copy.dbf','r')
    f.seek(0)
    print "HEADER: ", copy.header == f.header
    print "SPEC: ", copy.field_spec == f.field_spec
    print "DATA: ",list(copy) == list(f)



