# rbd_ssd_cache

## Installation
 1. Deploy Ceph cluster firstly with your favourit tool
 2. On each compute node, patch Ceph srouce code: git checkout v10.2.5; git apply librbd-hook.patch;
 3. Update the patched headers in your system: cp -r src/include/rbd /usr/include;
 5. Install patched Ceph: cd ceph-src-dir; make && make install;
 6. Mount SSD to the cache dir: mount /dev/nvme0n1 /mnt/cache;
 7. Create the config dir: mkdir /etc/sbc/; cp general.conf /etc/sbc/
 8. Create RBD and then run

## Note
 1. By default rbd ssd caching is enbaled only if its name is prefixed as 'ssdcache'.
e.g, rbd 'testimage' will have no ssd cache while rbd 'ssdcache_testimage' will have cache enabled.
We could disable this by rbd_cache_volume_enable = false
 2. There will be a phantom volume cache_volume_xxx created along with each rbd.
 3. rbd_pool_io_events API is not supported yet, please test with < fio-2.14.
 4. Better to use the same cache_min_alloc_size as your IO request size, otherwise the performance
will be slow as each request will be splited.

