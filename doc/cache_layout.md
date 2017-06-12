# Option 0
## Overall
Superblock(1MB) + Segment + Segment + ...

##Superblock
Superblock header + ... + Superblock tail

###Superblock header
magic 

###Superblock tail
last_written_seg, mainly for recovery

##Segment
Segment_header + Meta_block * nr_segs + Segment_block * nr_segs

###Segment_header
id + checksum + length

###Meta_block
sector_id
dirty_bits

###Segment_block
Data[4KB]

# Option 1
Move all metadata stuff to external rocksdb

# Option 2
To use bluestore
