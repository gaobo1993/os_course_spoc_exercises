## 理解文件访问的执行过程
高博 2012012139

修改的文件包括kern/fs/file.c, kern/fs/sysfile.c, kern/fs/sfs/sfs_io.c, kern/fs/sfs/sfs_inode.c, kern/fs/devs/dev_disk0.c, kern/driver/ide.c

输出：

```
sysfile_read begin
file_read begin
file_read file acquired
   vop_read(sfs_read) begin
   sfs_io begin
       sfs_io_nolock begin
       sfs_io_nolock begin reading (by sfs_rblock or sfs_rbuf)
           sfs_rbuf begin
           sfs_rwblock_nolock begin
           sfs_rwblock_nolock iobuf_init
               disk0_io begin
               disk0_read_blks_nolock begin
                   ide_read_secs begin
                   ide_read_secs call insl to read from disk
                   ide_read_secs end
               disk0_read_blks_nolock end
               disk0_io end
           sfs_rwblock_nolock end
           sfs_rbuf end
       sfs_io_nolock end
   sfs_io end
file_read file released
file_read end
sysfile_read end

sysfile_read begin
file_read begin
file_read file acquired
   vop_read(sfs_read) begin
   sfs_io begin
       sfs_io_nolock begin
       sfs_io_nolock begin reading (by sfs_rblock or sfs_rbuf)
           sfs_rblock begin
           sfs_rwblock begin
           sfs_rwblock_nolock begin
           sfs_rwblock_nolock iobuf_init
               disk0_io begin
               disk0_read_blks_nolock begin
                   ide_read_secs begin
                   ide_read_secs call insl to read from disk
                   ide_read_secs end
               disk0_read_blks_nolock end
               disk0_io end
           sfs_rwblock_nolock end
           sfs_rwblock end
           sfs_rblock end
       sfs_io_nolock end
   sfs_io end
file_read file released
file_read end
sysfile_read end

```
可以看出，具体的调用过程是:  
syscall => sysfile_read => file_read => vop_read => sfs_io => sfs_io_nolock => sfs_rbuf / sfs_rblock->sfs_rwblock => sfs_rwblock_nolock => disk0_io => disk0_read_blks_nolock => ide_read_secs => insl
