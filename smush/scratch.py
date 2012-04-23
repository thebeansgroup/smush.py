import os, sys, tempfile

class Scratch (object):
    def __init__ (self):
        tup = tempfile.mkstemp()
        self._path = tup[1]
        self._file = os.fdopen(tup[0])        
        self._file.close()

    def __del__ (self):
        if self._path != None:
            self.destruct()

    def destruct (self):
        self.close()
        os.unlink(self._path)
        self._path = None
        self._file = None

    def close (self):
        if self._file.closed == False:
            self._file.flush()
            self._file.close()

    def read (self):
        if self._file.closed == True:
            self._reopen()
        self._file.seek(0)
        return self._file.read()

    def _reopen (self):
        self._file = open(self._path, 'w+')

    def getopened (self):
        self.close()
        self._reopen()
        return self._file
    opened = property(getopened, NotImplemented, NotImplemented, "opened file - read only")

    def getfile (self):
        return self._file
    file = property(getfile, NotImplemented, NotImplemented, "file - read only")
