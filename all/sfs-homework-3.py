#! /usr/bin/env python

import random
from optparse import OptionParser

DEBUG = False

def dprint(str):
    if DEBUG:
        print str

printOps      = True
printState    = True
printFinal    = True

class bitmap:
    def __init__(self, size):
        self.size = size
        self.bmap = []
        for num in range(size):
            self.bmap.append(0)

    def alloc(self):
        for num in range(len(self.bmap)):
            if self.bmap[num] == 0:
                self.bmap[num] = 1
                return num
        return -1

    def free(self, num):
        assert(self.bmap[num] == 1)
        self.bmap[num] = 0

    def markAllocated(self, num):
        assert(self.bmap[num] == 0)
        self.bmap[num] = 1

    def dump(self):
        s = ''
        for i in range(len(self.bmap)):
            s += str(self.bmap[i])
        return s

class block:
    def __init__(self, ftype):
        assert(ftype == 'd' or ftype == 'f' or ftype == 'free')
        self.ftype = ftype
        # only for directories, properly a subclass but who cares
        self.dirUsed = 0
        self.maxUsed = 32
        self.dirList = []
        self.data    = ''

    def dump(self):
        if self.ftype == 'free':
            return '[]'
        elif self.ftype == 'd':
            rc = ''
            for d in self.dirList:
                # d is of the form ('name', inum)
                short = '(%s,%s)' % (d[0], d[1])
                if rc == '':
                    rc = short
                else:
                    rc += ' ' + short
            return '['+rc+']'
            # return '%s' % self.dirList
        else:
            return '[%s]' % self.data

    def setType(self, ftype):
        assert(self.ftype == 'free')
        self.ftype = ftype

    def addData(self, data):
        assert(self.ftype == 'f')
        self.data = data

    def getNumEntries(self):
        assert(self.ftype == 'd')
        return self.dirUsed

    def getFreeEntries(self):
        assert(self.ftype == 'd')
        return self.maxUsed - self.dirUsed

    def getEntry(self, num):
        assert(self.ftype == 'd')
        assert(num < self.dirUsed)
        return self.dirList[num]

    def addDirEntry(self, name, inum):
        assert(self.ftype == 'd')
        self.dirList.append((name, inum))
        self.dirUsed += 1
        assert(self.dirUsed <= self.maxUsed)

    def delDirEntry(self, name):
        assert(self.ftype == 'd')
        tname = name.split('/')
        dname = tname[len(tname) - 1]
        for i in range(len(self.dirList)):
            if self.dirList[i][0] == dname:
                self.dirList.pop(i)
                self.dirUsed -= 1
                return
        assert(1 == 0)

    def dirEntryExists(self, name):
        assert(self.ftype == 'd')
        for d in self.dirList:
            if name == d[0]:
                return True
        return False

    def free(self):
        assert(self.ftype != 'free')
        if self.ftype == 'd':
            # check for only dot, dotdot here
            assert(self.dirUsed == 2)
            self.dirUsed = 0
        self.data  = ''
        self.ftype = 'free'

class inode:
    def __init__(self, ftype='free', addr=-1, refCnt=1):
        self.setAll(ftype, addr, refCnt)

    def setAll(self, ftype, addr, refCnt):
        assert(ftype == 'd' or ftype == 'f' or ftype == 'free' or ftype == 'link')
        self.ftype  = ftype
        self.addr   = addr
        self.refCnt = refCnt

    def incRefCnt(self):
        self.refCnt += 1

    def decRefCnt(self):
        self.refCnt -= 1

    def getRefCnt(self):
        return self.refCnt

    def setType(self, ftype):
        assert(ftype == 'd' or ftype == 'f' or ftype == 'free')
        self.ftype = ftype

    def setAddr(self, block):
        self.addr = block

    def getSize(self):
        if self.addr == -1:
            return 0
        else:
            return 1

    def getAddr(self):
        return self.addr

    def getType(self):
        return self.ftype

    def free(self):
        self.ftype = 'free'
        self.addr  = -1


class fs:
    def __init__(self, numInodes, numData):
        self.numInodes = numInodes
        self.numData   = numData

        self.ibitmap = bitmap(self.numInodes)
        self.inodes  = []
        for i in range(self.numInodes):
            self.inodes.append(inode())

        self.dbitmap = bitmap(self.numData)
        self.data    = []
        for i in range(self.numData):
            self.data.append(block('free'))

        # root inode
        self.ROOT = 0

        # create root directory
        self.ibitmap.markAllocated(self.ROOT)
        self.inodes[self.ROOT].setAll('d', 0, 2)
        self.dbitmap.markAllocated(self.ROOT)
        self.data[0].setType('d')
        self.data[0].addDirEntry('.',  self.ROOT)
        self.data[0].addDirEntry('..', self.ROOT)

        # these is just for the fake workload generator
        self.files      = []
        self.dirs       = ['/']
        self.nameToInum = {'/':self.ROOT}

    def dump(self):
        print 'inode bitmap ', self.ibitmap.dump()
        print 'inodes       ',
        for i in range(0,self.numInodes):
            ftype = self.inodes[i].getType()
            if ftype == 'free':
                print '[]',
            else:
                print '[%s a:%s r:%d]' % (ftype, self.inodes[i].getAddr(), self.inodes[i].getRefCnt()),
        print ''
        print 'data bitmap  ', self.dbitmap.dump()
        print 'data         ',
        for i in range(self.numData):
            print self.data[i].dump(),
        print ''

    def makeName(self):
        p = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        return p[int(random.random() * len(p))]

    def inodeAlloc(self):
        return self.ibitmap.alloc()

    def inodeFree(self, inum):
        self.ibitmap.free(inum)
        self.inodes[inum].free()

    def dataAlloc(self):
        return self.dbitmap.alloc()

    def dataFree(self, bnum):
        self.dbitmap.free(bnum)
        self.data[bnum].free()

    def getParent(self, name):
        tmp = name.split('/')
        if len(tmp) == 2:
            return '/'
        pname = ''
        for i in range(1, len(tmp)-1):
            pname = pname + '/' + tmp[i]
        return pname

    def deleteFile(self, tfile):
        if printOps:
            print 'unlink("%s");' % tfile

        inum = self.nameToInum[tfile]
        if self.inodes[inum].getRefCnt()==1:
            self.dataFree(self.inodes[inum].getAddr())
            self.inodeFree(inum)
        else:
            self.inodes[inum].decRefCnt()


        num=self.nameToInum[self.getParent(tfile)]
        self.inodes[num].decRefCnt()
        self.data[num].delDirEntry(tfile)

    # YOUR CODE, YOUR ID
        # IF inode.refcnt ==1, THEN free data blocks first, then free inode, ELSE dec indoe.refcnt
        # remove from parent directory: delete from parent inum, delete from parent addr
    # DONE

        # finally, remove from files list
        self.files.remove(tfile)
        return 0

    def createLink(self, target, newfile, parent):
    # YOUR CODE, 2012011367
        # find info about parent
        # is there room in the parent directory?
        # if the newfile was already in parent dir?
        # now, find inumber of target
        # inc parent ref count
        # now add to directory
    # DONE
        if parent not in self.dirs:
            print "!!%s does not exist" %parent
            return -1
        ip = self.nameToInum[parent]
        if self.data[ip].getFreeEntries == 0:
            print "!!no free space in %s" %parent
            return -1
        if not target in self.nameToInum:
            print "!!%s does not exist" %target
            return -1
        tinum = self.nameToInum[target]
        if self.data[ip].dirEntryExists(newfile):
            print "!!%s already exists in %s" %newfile,parent
        else:
            self.data[ip].addDirEntry(newfile, tinum)

        #inum = self.nameToInum[target]
        self.inodes[ip].incRefCnt()
        self.inodes[tinum].incRefCnt()
        #self.data[ip].addDirEntry(newfile, inum)

        return tinum

    def createSoftLink(self, target, newfile, parent):
        if parent not in self.dirs:
            print "!!%s does not exist" %parent
            return -1
        ip = self.nameToInum[parent]
        if self.data[ip].getFreeEntries == 0:
            print "!!no free space in %s" %parent
            return -1
        if not target in self.nameToInum:
            print "!!%s does not exist" %target
            return -1
        lnum = self.createFile(parent, newfile, 'link')
        self.writeFile(newfile, target)
        return lnum

    def createFile(self, parent, newfile, ftype):
    # YOUR CODE, 2012011367
        # find info about parent
        # is there room in the parent directory?
        # have to make sure file name is unique
        # find free inode
        # if a directory, have to allocate directory block for basic (., ..) info
        # now ok to init inode properly
        # inc parent ref count
        # and add to directory of parent
    # DONE
        if parent not in self.dirs:
            print "!!% does not exist" %parent
            return -1
        ip = self.nameToInum[parent]
        if self.data[ip].getFreeEntries == 0:
            print "!!no free space in %s" %parent
            return -1
        if newfile in self.files:
            print "!!not an unique file name"
            return -1
        inum = self.inodeAlloc()
        if ftype == 'd':
            iaddr = self.dataAlloc()
            self.data[iaddr].setType(ftype)
        elif ftype == 'f' or ftype == 'link':
            iaddr = -1

        if ftype == 'd':
            self.inodes[inum].setAll(ftype, iaddr, 2)
            self.data[iaddr].addDirEntry(".", inum)
            self.data[iaddr].addDirEntry("..", ip)
           # self.dirs.append(newfile)
        else:
            self.inodes[inum].setAll(ftype, iaddr, 1)
           # self.files.append(newfile)
        self.nameToInum[newfile] = inum
        self.data[ip].addDirEntry(newfile, inum)
        self.inodes[ip].incRefCnt()
        return inum

    def writeFile(self, tfile, data):
        inum = self.nameToInum[tfile]
        curSize = self.inodes[inum].getSize()
        dprint('writeFile: inum:%d cursize:%d refcnt:%d' % (inum, curSize, self.inodes[inum].getRefCnt()))

    # YOUR CODE, 2012011367
        # file is full?
        # no data blocks left
        # write file data
    # DONE
        if curSize== 0:
            iaddr = self.dataAlloc()
            if iaddr == -1:
                print "!!no data blocks left"
                return -1
            self.inodes[inum].setAddr(iaddr)
            self.data[iaddr].setType('f')
        else:
            iaddr = self.inodes[inum].getAddr()
        self.data[iaddr].addData(data)
        if printOps:
            print 'fd=open("%s", O_WRONLY|O_APPEND); write(fd, buf, BLOCKSIZE); close(fd);' % tfile
        return 0

    def doDelete(self):
        dprint('doDelete')
        if len(self.files) == 0:
            return -1
        dfile = self.files[int(random.random() * len(self.files))]
        dprint('try delete(%s)' % dfile)
        return self.deleteFile(dfile)

    def doLink(self):
        dprint('doLink')
        if len(self.files) == 0:
            return -1
        parent = self.dirs[int(random.random() * len(self.dirs))]
        nfile = self.makeName()

        # pick random target
        target = self.files[int(random.random() * len(self.files))]

        # get full name of newfile
        if parent == '/':
            fullName = parent + nfile
        else:
            fullName = parent + '/' + nfile

        dprint('try createLink(%s %s %s)' % (target, nfile, parent))
        inum = self.createSoftLink(target, nfile, parent)
        if inum >= 0:
            self.files.append(fullName)
            self.nameToInum[fullName] = inum
            if printOps:
                print 'link("%s", "%s");' % (target, fullName)
            return 0
        return -1

    def doCreate(self, ftype):
        dprint('doCreate')
        parent = self.dirs[int(random.random() * len(self.dirs))]
        nfile = self.makeName()
        if ftype == 'd':
            tlist = self.dirs
        else:
            tlist = self.files

        if parent == '/':
            fullName = parent + nfile
        else:
            fullName = parent + '/' + nfile

        dprint('try createFile(%s %s %s)' % (parent, nfile, ftype))
        inum = self.createFile(parent, nfile, ftype)
        if inum >= 0:
            tlist.append(fullName)
            self.nameToInum[fullName] = inum
            if parent == '/':
                parent = ''
            if ftype == 'd':
                if printOps:
                    print 'mkdir("%s/%s");' % (parent, nfile)
            else:
                if printOps:
                    print 'creat("%s/%s");' % (parent, nfile)
            return 0
        return -1

    def doAppend(self):
        dprint('doAppend')
        if len(self.files) == 0:
            return -1
        afile = self.files[int(random.random() * len(self.files))]
        dprint('try writeFile(%s)' % afile)
        data = chr(ord('a') + int(random.random() * 26))
        rc = self.writeFile(afile, data)
        return rc

    def run(self, numRequests):
        self.percentMkdir  = 0.40
        self.percentWrite  = 0.40
        self.percentDelete = 0.20
        self.numRequests   = numRequests

        print 'Initial state'
        print ''
        self.dump()
        print ''

        for i in range(numRequests):
            if printOps == False:
                print 'Which operation took place?'
            rc = -1
            while rc == -1:
                r = random.random()
                if r < 0.3:
                    rc = self.doAppend()
                    dprint('doAppend rc:%d' % rc)
                elif r < 0.5:
                    rc = self.doDelete()
                    dprint('doDelete rc:%d' % rc)
                elif r < 0.7:
                    rc = self.doLink()
                    dprint('doLink rc:%d' % rc)
                else:
                    if random.random() < 0.75:
                        rc = self.doCreate('f')
                        dprint('doCreate(f) rc:%d' % rc)
                    else:
                        rc = self.doCreate('d')
                        dprint('doCreate(d) rc:%d' % rc)
            if printState == True:
                print ''
                self.dump()
                print ''
            else:
                print ''
                print '  State of file system (inode bitmap, inodes, data bitmap, data)?'
                print ''

        if printFinal:
            print ''
            print 'Summary of files, directories::'
            print ''
            print '  Files:      ', self.files
            print '  Directories:', self.dirs
            print ''

#
# main program
#
parser = OptionParser()

parser.add_option('-s', '--seed',        default=0,     help='the random seed',                      action='store', type='int', dest='seed')
parser.add_option('-i', '--numInodes',   default=8,     help='number of inodes in file system',      action='store', type='int', dest='numInodes')
parser.add_option('-d', '--numData',     default=8,     help='number of data blocks in file system', action='store', type='int', dest='numData')
parser.add_option('-n', '--numRequests', default=10,    help='number of requests to simulate',       action='store', type='int', dest='numRequests')
parser.add_option('-r', '--reverse',     default=False, help='instead of printing state, print ops', action='store_true',        dest='reverse')
parser.add_option('-p', '--printFinal',  default=False, help='print the final set of files/dirs',    action='store_true',        dest='printFinal')

(options, args) = parser.parse_args()

print 'ARG seed',        options.seed
print 'ARG numInodes',   options.numInodes
print 'ARG numData',     options.numData
print 'ARG numRequests', options.numRequests
print 'ARG reverse',     options.reverse
print 'ARG printFinal',  options.printFinal
print ''

random.seed(options.seed)

if options.reverse:
    printState = False
    printOps   = True
else:
    printState = True
    printOps   = False


printOps   = True
printState = True

printFinal = options.printFinal

#
# have to generate RANDOM requests to the file system
# that are VALID!
#

f = fs(options.numInodes, options.numData)

#
# ops: mkdir rmdir : create delete : append write
#

f.run(options.numRequests)
