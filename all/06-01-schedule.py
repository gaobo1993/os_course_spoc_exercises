#! /usr/bin/env python
import sys
from optparse import OptionParser
import random

parser = OptionParser()
parser.add_option("-s", "--seed", default=0, help="the random seed",
                  action="store", type="int", dest="seed")
parser.add_option("-j", "--jobs", default=3, help="number of jobs in the system",
                  action="store", type="int", dest="jobs")
parser.add_option("-l", "--jlist", default="", help="instead of random jobs, provide a comma-separated list of run times",
                  action="store", type="string", dest="jlist")
parser.add_option("-m", "--maxlen", default=10, help="max length of job",
                  action="store", type="int", dest="maxlen")
parser.add_option("-p", "--policy", default="FIFO", help="sched policy to use: SJF, FIFO, RR",
                  action="store", type="string", dest="policy")
parser.add_option("-q", "--quantum", help="length of time slice for RR policy", default=1,
                  action="store", type="int", dest="quantum")
parser.add_option("-c", help="compute answers for me", action="store_true", default=True, dest="solve")

(options, args) = parser.parse_args()

random.seed(options.seed)

print 'ARG policy', options.policy
if options.jlist == '':
    print 'ARG jobs', options.jobs
    print 'ARG maxlen', options.maxlen
    print 'ARG seed', options.seed
else:
    print 'ARG jlist', options.jlist

print ''

print 'Here is the job list, with the run time of each job: '

import operator

queuenum = 3;
joblist = []
jobqueue = []
jobqueuepiece = [3,2,1]
if options.policy == 'MLFQ':
    if options.jobs < queuenum:
        options.jobs = queuenum;

if options.jlist == '':
    for jobnum in range(0,options.jobs):
        runtime = int(options.maxlen * random.random()) + 1
        if options.policy == 'STRIDE':
            runtime = options.maxlen
        prio = int(3 * random.random()) + 1
        stride = 0
        passnum = 6/prio
        joblist.append([jobnum, runtime, prio,stride,passnum])
        print '  Job', jobnum, '( length = ' + str(runtime) + ' prior = '+str(prio)+' stride = '+str(stride)+' passnum = '+str(passnum)+')'
else:
    jobnum = 0
    for runtime in options.jlist.split(','):
        joblist.append([jobnum, float(runtime)])
        jobnum += 1
    for job in joblist:
        print '  Job', job[0], '( length = ' + str(job[1]) + ' )'
print '\n'


if options.policy == 'MLFQ':
    for i in range(0,queuenum):
        jobqueue.append([])
    for i in range(0,options.jobs):
        jobqueue[i%queuenum].append(joblist[i])

if options.solve == True:
    print '** Solutions **\n'
    if options.policy == 'SJF':
        #YOUR CODE
        thetime = 0
        print 'Execution trace:'
        #YOUR CODE
        time = 0;
        jobnum = 0;
        joblist.sort(lambda x,y:cmp(x[1],y[1]))
        for jobs in joblist:
            print '  [ time %3d ] Run job %d for %3.2f secs ( DONE at %3.2f )' % (time, jobs[0], jobs[1], time+jobs[1]);
            time = time + jobs[1];

        print '\nFinal statistics:'
        t     = 0.0
        count = 0
        turnaroundSum = 0.0
        waitSum       = 0.0
        responseSum   = 0.0
        for tmp in joblist:
            jobnum  = tmp[0]
            runtime = tmp[1]

            response   = t
            turnaround = t + runtime
            wait       = t
            print '  Job %3d -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f' % (jobnum, response, turnaround, wait)
            responseSum   += response
            turnaroundSum += turnaround
            waitSum       += wait
            t += runtime
            count = count + 1
        print '\n  Average -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f\n' % (responseSum/count, turnaroundSum/count, waitSum/count)

    if options.policy == 'FIFO':
        thetime = 0
        print 'Execution trace:'
        #YOUR CODE
        time = 0;
        jobnum = 0;
        for jobs in joblist:
            print '  [ time %3d ] Run job %d for %3.2f secs ( DONE at %3.2f )' % (time, jobs[0], jobs[1], time+jobs[1]);
            time = time + jobs[1];
        print '\nFinal statistics:'
        t     = 0.0
        count = 0
        turnaroundSum = 0.0
        waitSum       = 0.0
        responseSum   = 0.0
        for tmp in joblist:
            jobnum  = tmp[0]
            runtime = tmp[1]

            response   = t
            turnaround = t + runtime
            wait       = t
            print '  Job %3d -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f' % (jobnum, response, turnaround, wait)
            responseSum   += response
            turnaroundSum += turnaround
            waitSum       += wait
            t += runtime
            count = count + 1
        print '\n  Average -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f\n' % (responseSum/count, turnaroundSum/count, waitSum/count)

    if options.policy == 'RR':
        print 'Execution trace:'
        turnaround = {}
        response = {}
        lastran = {}
        wait = {}
        quantum  = float(options.quantum)
        jobcount = len(joblist)
        for i in range(0,jobcount):
            lastran[i] = 0.0
            wait[i] = 0.0
            turnaround[i] = 0.0
            response[i] = -1

        runlist = []
        for e in joblist:
            runlist.append(e)

        thetime  = 0.0
        while jobcount > 0:
            # print '%d jobs remaining' % jobcount
            job = runlist.pop(0)
            jobnum  = job[0]
            runtime = float(job[1])
            if response[jobnum] == -1:
                response[jobnum] = thetime
            currwait = thetime - lastran[jobnum]
            wait[jobnum] += currwait
            ranfor = 1
            if runtime > quantum:
                #YOUR CODE
                print '  [ time %3d ] Run job %3d for %.2f secs' % (thetime, jobnum, ranfor)
                runtime = runtime - ranfor
                runlist.append([jobnum, runtime])
            else:
                #YOUR CODE

                print '  [ time %3d ] Run job %3d for %.2f secs ( DONE at %.2f )' % (thetime, jobnum, ranfor, thetime + ranfor)
                turnaround[jobnum] = thetime + ranfor
                jobcount -= 1
            thetime += ranfor
            lastran[jobnum] = thetime

        print '\nFinal statistics:'
        turnaroundSum = 0.0
        waitSum       = 0.0
        responseSum   = 0.0
        for i in range(0,len(joblist)):
            turnaroundSum += turnaround[i]
            responseSum += response[i]
            waitSum += wait[i]
            print '  Job %3d -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f' % (i, response[i], turnaround[i], wait[i])
        count = len(joblist)

        print '\n  Average -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f\n' % (responseSum/count, turnaroundSum/count, waitSum/count)
    if options.policy == 'MLFQ':
            print 'Execution trace:'
            freequeue = 0;
            turnaround = {}
            response = {}
            lastran = {}
            wait = {}
            thetime  = 0.0
            jobcount = len(joblist)
            for i in range(0,jobcount):
                lastran[i] = 0.0
                wait[i] = 0.0
                turnaround[i] = 0.0
                response[i] = -1

            quantum  = float(options.quantum)
            while freequeue < queuenum:
                nowjoblist = jobqueue[freequeue]
                jobcount = len(nowjoblist)

                runlist = []
                for e in nowjoblist:
                    runlist.append(e)

                while jobcount > 0:
                    # print '%d jobs remaining' % jobcount
                    job = runlist.pop(0)
                    jobnum  = job[0]
                    runtime = float(job[1])
                    if response[jobnum] == -1:
                        response[jobnum] = thetime
                    currwait = thetime - lastran[jobnum]
                    wait[jobnum] += currwait
                    ranfor = jobqueuepiece[freequeue]
                    if runtime > quantum:
                        #YOUR CODE
                        print '  [ time %3d ] Run job %3d for %.2f secs' % (thetime, jobnum, ranfor)
                        runtime = runtime - ranfor
                        runlist.append([jobnum, runtime])
                    else:
                        #YOUR CODE

                        print '  [ time %3d ] Run job %3d for %.2f secs ( DONE at %.2f )' % (thetime, jobnum, ranfor, thetime + ranfor)
                        turnaround[jobnum] = thetime + ranfor
                        jobcount -= 1
                    thetime += ranfor
                    lastran[jobnum] = thetime
                freequeue += 1
            print '\nFinal statistics:'
            turnaroundSum = 0.0
            waitSum       = 0.0
            responseSum   = 0.0
            for i in range(0,len(joblist)):
                turnaroundSum += turnaround[i]
                responseSum += response[i]
                waitSum += wait[i]
                print '  Job %3d -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f' % (i, response[i], turnaround[i], wait[i])
            count = len(nowjoblist)

            print '\n  Average -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f\n' % (responseSum/count, turnaroundSum/count, waitSum/count)

    if options.policy == 'STRIDE':
        print 'Execution trace:'


        turnaround = {}
        response = {}
        lastran = {}
        wait = {}
        quantum  = float(options.quantum)
        jobcount = len(joblist)
        for i in range(0,jobcount):
            lastran[i] = 0.0
            wait[i] = 0.0
            turnaround[i] = 0.0
            response[i] = -1

        runlist = []
        for e in joblist:
            runlist.append(e)

        thetime  = 0.0
        while jobcount > 0:
            # print '%d jobs remaining' % jobcount
            runlist.sort(key=lambda x:x[3])
            job = runlist.pop(0)
            jobnum  = job[0]
            runtime = float(job[1])
            prio= job[2]
            stride = job[3]
            passnum = job[4]
            if response[jobnum] == -1:
                response[jobnum] = thetime
            currwait = thetime - lastran[jobnum]
            wait[jobnum] += currwait
            ranfor = 0
            if runtime > quantum:
                #YOUR CODE
                runtime = runtime - quantum
                ranfor = quantum
                stride = stride + passnum
                print '  [ time %3d ] Run job %3d for %.2f secs' % (thetime, jobnum, ranfor)
                runlist.append([jobnum, runtime,prio,stride,passnum])
            else:
                #YOUR CODE
                ranfor = quantum
                print '  [ time %3d ] Run job %3d for %.2f secs ( DONE at %.2f )' % (thetime, jobnum, ranfor, thetime + ranfor)
                turnaround[jobnum] = thetime + ranfor
                jobcount -= 1
            thetime += ranfor
            lastran[jobnum] = thetime


        print '\nFinal statistics:'
        turnaroundSum = 0.0
        waitSum       = 0.0
        responseSum   = 0.0
        for i in range(0,len(joblist)):
            turnaroundSum += turnaround[i]
            responseSum += response[i]
            waitSum += wait[i]
            print '  Job %3d -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f' % (i, response[i], turnaround[i], wait[i])
        count = len(joblist)

        print '\n  Average -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f\n' % (responseSum/count, turnaroundSum/count, waitSum/count)


    if options.policy != 'FIFO' and options.policy != 'SJF' and options.policy != 'RR' and options.policy != 'MLFQ' and options.policy != 'STRIDE':
        print 'Error: Policy', options.policy, 'is not available.'
        sys.exit(0)
else:
    print 'Compute the turnaround time, response time, and wait time for each job.'
    print 'When you are done, run this program again, with the same arguments,'
    print 'but with -c, which will thus provide you with the answers. You can use'
    print '-s <somenumber> or your own job list (-l 10,15,20 for example)'
    print 'to generate different problems for yourself.'
    print ''
