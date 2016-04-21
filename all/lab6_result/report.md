## Report for 理解调度算法支撑框架的执行过程

高博 2012012139

> 运行结果及分析

```
idle schedule                                       进程创建初始化后idle proc开始运行
schedule: timer finished for process pid = 0        idle proc(pid = 0) 时间片用完
schedule: ticks process pid = 1 to run              选择init proc(pid = 1)，来执行用户态进程
Wake up process pid = 2                             唤醒proc 2，将其放入就绪队列
proc 1 do_wait schedule                             init proc(pid = 1)进入wait状态（等待proc 2），执行schedule
schedule: ticks process pid = 2 to run              选择proc 2来运行，来执行用户态进程
kernel_execve: pid = 2, name = "exit".              执行exit proc(pid = 2)
I am the parent. Forking the child...               创建一个子进程
Wake up process pid = 3                             并唤醒它(pid = 3)，将其放入就绪队列
I am parent, fork a child pid 3
I am the parent, waiting now..                      
proc 2 do_wait schedule                             exit proc(pid = 2)进入wait状态（等待proc 3），执行schedule
schedule: ticks process pid = 3 to run              选择proc 3
I am the child.                                     执行proc 3，并且由于其他进程(1, 2)均处于wait状态，
schedule: timer finished for process pid = 3        每次用完时间片之后再次选择proc时还会选择proc 3
schedule: ticks process pid = 3 to run
schedule: timer finished for process pid = 3
schedule: ticks process pid = 3 to run
schedule: timer finished for process pid = 3
schedule: ticks process pid = 3 to run
schedule: timer finished for process pid = 3
schedule: ticks process pid = 3 to run
schedule: timer finished for process pid = 3
schedule: ticks process pid = 3 to run
schedule: timer finished for process pid = 3
schedule: ticks process pid = 3 to run
schedule: timer finished for process pid = 3
schedule: ticks process pid = 3 to run
proc 3 do_exit use schedule                         proc 3结束，调用schedule
Wake up process pid = 2                             唤醒proc 2，将其放入就绪队列
schedule: ticks process pid = 2 to run              选择proc 2来运行
waitpid 3 ok.                                       执行proc 2
exit pass.
proc 2 do_exit use schedule                         proc 2结束，调用schedule
Wake up process pid = 1                             唤醒proc 1，将其放入就绪队列
schedule: ticks process pid = 1 to run              选择proc 1来运行
proc init_main schedule                             执行proc 1
schedule: timer finished for process pid = 1
schedule: ticks process pid = 1 to run
all user-mode processes have quit.
```
