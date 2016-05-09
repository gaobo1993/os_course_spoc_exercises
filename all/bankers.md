## 银行家算法Report

高博 2012012139

除了对于Your Code部分的补充，我还对于程序框架做出了以下改进：

### 框架效率优化
现在的程序框架是尝试所有permutation，效率过低。我对其改进为：
1. 从尚未释放的进程中选取一个资源需求量小于等于系统剩余资源量的进程i，如果找不到，转3
2. 执行i并释放相应的资源。
3. 如果所有进程都被释放，返回True，否则返回False。
代码如下：
```
def Execute(self):
    procnum = len(self.max)
    idx = 0
    while 1:
        # Pick one valid process
        idx = self.TempSafeCheckAfterRelease()
        # if there is no valid process and the program is not done
        if idx == -1:
            print "SAFE STATE: NOT SAFE - There are no sequances can avoid Deadlock"
            return False
        # if the program is done
        if idx == procnum:
            return True
        # Execute
        print "Executing..."
        print "Request: "
        print self.need[idx]
        #check if less avaliable than Request
        if self.ExecuteProcess(idx):
            print "Dispatching Done..."
            self.print_matrixes()
            print "-----Releasing Process------"
            self.ReleasingProcess(idx)
            self.print_matrixes()
            processes.append(idx)
```

为了实现上述算法，我将TempSafeCheckAfterRelease的返回值接口定义为：
+ 返回值为[0, procnum)之间的整数： 下一步可以执行释放的进程编号
+ 返回值等于-1： 找不到可以执行释放的进程编号
+ 返回值等于procnum： 所有进程已被释放

具体实现可以参考代码文件。

### 原程序bug修正
原来的程序框架中是有bug的，在源文件第79行
```
perm = itertools.permutations(range(procnum), procnum)
```
这个procnum在我的系统里运行时一直是3，也就是说更新max, allocate等矩阵的同时没有更新procnum，导致在运行四个进程时有一个进程永远不会被释放。我在之前加了一行```procnum = len(self.max)```来改进。
