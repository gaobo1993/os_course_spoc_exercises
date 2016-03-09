# lec6 SPOC思考题


NOTICE
- 有"w3l2"标记的题是助教要提交到学堂在线上的。
- 有"w3l2"和"spoc"标记的题是要求拿清华学分的同学要在实体课上完成，并按时提交到学生对应的git repo上。
- 有"hard"标记的题有一定难度，鼓励实现。
- 有"easy"标记的题很容易实现，鼓励实现。
- 有"midd"标记的题是一般水平，鼓励实现。


## 个人思考题
---

（1） (w3l2) 请简要分析64bit CPU体系结构下的分页机制是如何实现的
```
  + 采分点：说明64bit CPU架构的分页机制的大致特点和页表执行过程
  - 答案没有涉及如下3点；（0分）
  - 正确描述了64bit CPU支持的物理内存大小限制（1分）
  - 正确描述了64bit CPU下的多级页表的级数和多级页表的结构或反置页表的结构（2分）
  - 除上述两点外，进一步描述了在多级页表或反置页表下的虚拟地址-->物理地址的映射过程（3分）
 ```
- [x]  

>  　　64位CPU的逻辑地址空间理论上可以高达2^64B，即2物理内存大小为2^64 Byte=16 EB,但是实际的物理地址空间和需求要远小于这个值，因此厂商实际只使用52位的地址总线，也即4 PB的虚拟地址空间。  
>  　　x64下使用的四级页表(PML4-PDPT-PD-PT)及其映射过程：（参考资料IA32e的内存_paging和TLB流程）   
>  　　0. 最底层的paging structures的基地址保存在CR3中，直接是52-bit的地址。CR3中保存的是 PML4 table的物理地址，而PML4 table中保存的是地址寄存器(线性地址) 47-39 bits所使用的物理地址序列。所有paging mode中的线性地址47-39 bits都是用来从PML4 table中选择更详细层的 paging structures的物理地址。    
>  　　1. 根据线性地址47-39 bits得到了PML4对应元素中的物理地址，其指向的是 page-directory-pointer table，每一个 page-directory-pointer包含的是一个索引512 GB的物理内存范围，(注意，此512GB的内存范围是不必须相连的)此范围内的线性地址 paging时都会来到此page-directory-pointer,原因是它们的线性地址的47-39 bits相同。 page-directory-pointer table中保存的是page-directroy的物理地址(简称PDP, page directroy-pointer)。线性地址的38-30 bits用来从此序列中得到更详细层的paging structures的物理地址。    
>  　　2. 根据 线程地址38-30的bits得到一个PDP，它所指向的page-directory包含索引1GB的物理地址范围的物理地址序列。地址值在同一1GB范围内的线性地址，也象上面的512GB范围内的地址一样，会来到同一个 page-directory，它们的线性地址47-30 bits是一样的。   
>  　　3. 根据47-30 bits到达了page-directroy，它里面的物理地址是以29-21 bits来索引的，代表的是一个 page table的物理地址。在同一个2MB内存范围的线性地址都在此索引到同一个物理地址，它们有相同的 47-21 bits。事实上，在IA32e的设计中，相同2MB范围内的线性地址，63-21bits都是相同的。 另外，page-directory中的物理地址被称为 PDE(page-diredtroy entry),看过IA32 paging流程介绍的一定非常熟悉PDE了，没错，IA32e扩展的流程到此基本结束了，当然单说的paging流程。PDE提供了4GB的线性内存访问范围。   
>  　　4. 从page-directory中选中的PDE内存是一个page table(页表)的物理地址，一个页表的元素简称为PTE(page-table entry)。用在page table中的线性地址部分是20-12的 bits。在相同4KB范围内的线性地址使用的都是同一个page table，即在同一个page frame中，它们的 63-12 bits是相同的。 5.从page table中根据20-12 bits得到了一个(4KB大小)内存页面的物理基地址后,11-0 bit的值作为索引用来加在此基地(PTE)上，到此得到的值便是线性地址完成paging后的物理地址。

## 小组思考题
---

（1）(spoc) 某系统使用请求分页存储管理，若页在内存中，满足一个内存请求需要150ns (10^-9s)。若缺页率是10%，为使有效访问时间达到0.5us(10^-6s),求不在内存的页面的平均访问时间。请给出计算步骤。

- [x]  

> 500=0.9\*150+0.1\*x

（2）(spoc) 有一台假想的计算机，页大小（page size）为32 Bytes，支持32KB的虚拟地址空间（virtual address space）,有4KB的物理内存空间（physical memory），采用二级页表，一个页目录项（page directory entry ，PDE）大小为1 Byte,一个页表项（page-table entries
PTEs）大小为1 Byte，1个页目录表大小为32 Bytes，1个页表大小为32 Bytes。页目录基址寄存器（page directory base register，PDBR）保存了页目录表的物理地址（按页对齐）。

PTE格式（8 bit） :
```
  VALID | PFN6 ... PFN0
```
PDE格式（8 bit） :
```
  VALID | PT6 ... PT0
```
其
```
VALID==1表示，表示映射存在；VALID==0表示，表示映射不存在。
PFN6..0:页帧号
PT6..0:页表的物理基址>>5
```
在[物理内存模拟数据文件](./03-2-spoc-testdata.md)中，给出了4KB物理内存空间的值，请回答下列虚地址是否有合法对应的物理内存，请给出对应的pde index, pde contents, pte index, pte contents。
```
Virtual Address 6c74
Virtual Address 6b22
Virtual Address 03df
Virtual Address 69dc
Virtual Address 317a
Virtual Address 4546
Virtual Address 2c03
Virtual Address 7fd7
Virtual Address 390e
Virtual Address 748b
```

比如答案可以如下表示：
```
Virtual Address 7570:
  --> pde index:0x1d  pde contents:(valid 1, pfn 0x33)
    --> pte index:0xb  pte contents:(valid 0, pfn 0x7f)
      --> Fault (page table entry not valid)

Virtual Address 21e1:
  --> pde index:0x8  pde contents:(valid 0, pfn 0x7f)
      --> Fault (page directory entry not valid)

Virtual Address 7268:
  --> pde index:0x1c  pde contents:(valid 1, pfn 0x5e)
    --> pte index:0x13  pte contents:(valid 1, pfn 0x65)
      --> Translates to Physical Address 0xca8 --> Value: 16
```



（3）请基于你对原理课二级页表的理解，并参考Lab2建页表的过程，设计一个应用程序（可基于python, ruby, C, C++，LISP等）可模拟实现(2)题中描述的抽象OS，可正确完成二级页表转换。


（4）假设你有一台支持[反置页表](http://en.wikipedia.org/wiki/Page_table#Inverted_page_table)的机器，请问你如何设计操作系统支持这种类型计算机？请给出设计方案。

 (5)[X86的页面结构](http://os.cs.tsinghua.edu.cn/oscourse/OS2015/lecture06#head-1f58ea81c046bd27b196ea2c366d0a2063b304ab)
---

## 扩展思考题

阅读64bit IBM Powerpc CPU架构是如何实现[反置页表](http://en.wikipedia.org/wiki/Page_table#Inverted_page_table)，给出分析报告。

---
