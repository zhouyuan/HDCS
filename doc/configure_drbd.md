#DRBD(distributed replication block deivce kernel module) 8.4.4 was shiped with Ubuntu 14.04 defautly.

* install drbd on both nodes
`apt-get update; apt-get install drbd8-utils`

* load kernel module
`modprobe drbd`

* create disk resource
```

cat /etc/drbd.d/disk1.res
resource disk1
{
   startup {
   wfc-timeout 30;
   outdated-wfc-timeout 20;
   degr-wfc-timeout 30;
 }

net {
   cram-hmac-alg sha1;
   shared-secret sync_disk;
 }

syncer {
   rate 200M;
   verify-alg sha1;
 }

on ctc {               # Node1 defined
   device /dev/drbd0;
   disk /dev/sde;                    # Device to use with DRBD
   address 10.44.44.7:7789;       # IP Address and port of Node1
   meta-disk internal;
 }

on ctd {               # Node2 defined
   device /dev/drbd0;
   disk /dev/sdb;                    # Device to use with DRBD
   address 10.44.44.152:7789;       # IP Address and port of Node2
   meta-disk internal;
 }
}
```


* create metadata on both nodes
`drbdadm create-md disk1`


* start drbd daemon on both nodes
`/etc/init.d/drbd start`

* set the primary copy
`drbdadm -- --overwrite-data-of-peer primary all`

* check drbd status
by default the drbd will sync the primay disk to replica disk now
the block device will be at /dev/drbd0
