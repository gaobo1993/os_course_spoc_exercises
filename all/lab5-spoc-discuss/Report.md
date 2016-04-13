## Report


在*kern/process/proc.c*和*kern/schedule/sched.c*中添加*cprintf*之后，得到输出结果：
```
process 1 switch to run
proc_run: switch context from idle(pid:0) to init(pid:1)...
forkret: process init(pid:1) cross from Ring 0 to Ring 3.
process 2 wakeup in schedule
Enter do_wait pid:0
do_wait: change to SLEEPING name: init, pid:1
process 2 switch to run
proc_run: switch context from init(pid:1) to (pid:2)...
forkret: process (pid:2) cross from Ring 0 to Ring 3.
====Enter user_main
kernel_execve: pid = 2, name = "exit".
do_execve: exit
I am the parent. Forking the child...
process 3 wakeup in schedule
I am parent, fork a child pid 3
I am the parent, waiting now..
Enter do_wait pid:3
do_wait: change to SLEEPING name: exit, pid:2
process 3 switch to run
proc_run: switch context from exit(pid:2) to (pid:3)...
forkret: process (pid:3) cross from Ring 0 to Ring 3.
I am the child.
do_exit name:, pid:3
process 2 wakeup in schedule
process 2 switch to run
proc_run: switch context from (pid:3) to exit(pid:2)...
Enter do_wait pid:3
Enter do_wait pid:0
waitpid 3 ok.
exit pass.
do_exit name:exit, pid:2
process 1 wakeup in schedule
process 1 switch to run
proc_run: switch context from exit(pid:2) to init(pid:1)...
Enter do_wait pid:0
all user-mode processes have quit.
init check memory pass.
```
