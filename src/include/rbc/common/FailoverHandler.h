

namespace rbc{

// ceph failure points
#define BACKEND_RADOS_CREATE -101
#define BACKEND_RADOS_READ_CONF_FILE -102
#define BACKEND_RADOS_CONNECT -103
#define BACKEND_RADOS_IOCTX_CREATE -104
#define BACHEND_RADOS_OPEN_SKIP_CACHE -105
#define BACKEND_RADOS_AIO_WRITE -106
#define BACKEND_RADOS_AIO_READ -107      //failure point at callback function, at C_AioBackendComplete child class.
#define BACKEND_RADOS_WRITE -108
#define BACKEND_RADOS_READ -109
#define BACKEND_RADOS_AIO_WRITE_AROUND -110
#define BACKEND_RADOS_AIO_READ_AROUND -111
#define BACKEND_RADOS_AIO_CREATE_COMPLETE -112


// metadata failure points
#define METADATA_ROCKSDB_OPEN -201
#define METADATA_ROCKSDB_GET -202
#define METADATA_ROCKSDB_PUT -203
#define METADATA_ROCKSDB_DELETE -204
#define METADATA_ROCKSDB_SCAN -205


// file system failure points, namely SSD IO operation fails.
#define SIMPLEBLOCKCACHE_FS_OPEN -301
#define SIMPLEBLOCKCACHE_FS_FTRUNCATE -302 
#define SIMPLEBLOCKCACHE_FS_NO_SSD_SPACE -303
#define SIMPLEBLOCKCACHE_FS_CLOSE -304
#define SIMPLEBLOCKCACHE_FS_WRITE -305
#define SIMPLEBLOCKCACHE_FS_READ -306
#define SIMPLEBLOCKCACHE_FS_POSIX_FADIVSE -307
#define SIMPLEBLOCKCACHE_FS_FSTAT -308
#define SIMPLEBLOCKCACHE_WRITE_INDEX_LOOKUP -309
#define SIMPLEBLOCKCACHE_READ_INDEX_LOOKUP -310

 
// Networking failure points.
#define ASIO_SOCKET_CLOSE -401
#define ASIO_SOCKET_ASYNC_READ_SOME -402
#define ASIO_FUNCTION_ASYNC_READ -403
#define ASIO_SOCKET_SEND -404
#define ASIO_SOCKET_CONNCTION -405

//IPC fails, namely message queue 
#define MQ_OPEN -501
#define MQ_CLOSE -502 
#define MQ_UNLINK -503
#define MQ_RECEIVE -504
#define MQ_SEND -505

//IPC fails, namely share memory.
#define SHM_GET -601
#define SHM_AT -602
#define SHM_DT -603 
#define SHM_CTL -604

//dynamic memory.
#define MEMORY_MALLOC -701   // mempool fail detection point
#define MEMORY_FREE  -702


/*
 * replication write fails between master and slave.
 * This failure point is in C_AioRelicateComplete.
*/
#define REPLICATE_FAILURE -801    
				

#define HDCS_CONFIG_FILE -901
#define HDCS_CONFIG_DUP2 -902





void failover_handler(int error_code, void* msg){

   switch(error_code){
	 case BACKEND_RADOS_CREATE:
	      f_backend_rados_create();
	      break;
	case BACKEND_RADOS_READ_CONF_FILE:
		f_backend_rados_read_conf_file();
		break;
	case BACKEND_RADOS_CONNECT:
		f_backend_rados_connect();
		break;
	case BACKEND_RADOS_IOCTX_CREATE:
		f_backend_rados_ioctx_create();
		break;
	case BACKEND_RADOS_OPEN_SKIP_CACHE:
		f_backend_rados_open_skip_cache();
		break;
	case BACKEND_RADOS_WRITE:
		f_backend_rados_write();
		break;
	case BACKEND_RADOS_READ:
		f_backend_rados_read();
		break;
	case BACKEND_RADOS_WRITE:
		f_backend_write();
		break;	
	case BACKEND_RADOS_READ:
		f_backend_rados_read();
		break;
	case BACKEND_RADOS_AIO_WRITE_AROUND:
		f_backend_rados_aio_write_around();
		break;
	case BACKEND_RADOS_AIO_READ_AROUND:
		f_backend_rados_aio_read_around();
		break;
	case BACKEND_RADOS_AIO_CREATE_COMPLETE:
		f_backend_rados_aio_create_complete();
		break;


	case METADATA_ROCKSDB_OPEN:
		f_metadat_rocksdb_open();
		break;
	case METADATA_ROCKSDB_GET:
		f_metadata_rocksdb_get();
		break;
	case METADATA_ROCKSDB_PUT
		f_metadat_rocksdb_put();
		break;	
	case METADATA_ROCKSDB_DELETE:
		f_metadata_rocksdb_delete();
		break;
	case METADATA_ROCKSDB_SCAN:
		f_metadate_rocksdb_scan();
		break;

	case SIMPLEBLOCKCACHE_FS_OPEN:
		f_simpleblockcache_fs_open();
		break;	
	case SIMPLEBLOCKCACHE_FS_FTRUNCATE:
		f_simpleblockcache_fs_ftruncate();
		break;
	case SIMPLEBLOCKCACHE_FS_NO_SSD_SPACE:
		f_simpleblockcache_fs_no_ssd_space();
		break;
	case SIMPLEBLOCKCACHE_FS_CLOSE:
		f_simpleblockcache_fs_close();
		break;
	case SIMPLEBLOCKCACHE_FS_WRITE:
		f_simpleblockcache_fs_write();
		break;
	case SIMPLEBLOCKCACHE_FS_READ:
		f_simpleblockcache_fs_read();
		break;
	case SIMPLEBLOCKCACHE_FS_POSIX_FADIVSE:
		f_simpleblock_fs_posix_fadivse();
		break;

	case ASIO_SOCKET_CLOSE:
		f_asio_socket_close();
		break;
	case ASIO_SOCKET_ASYNC_READ_SOME:
		f_asio_socket_asyn_read_some();
		break;
	case ASIO_FUNCTION_ASYNC_READ:
		f_asio_function_async_read();
		break;
	case ASIO_SOCKET_SEND:
		f_asio_socket_send();
		break;
	
	case MQ_OPEN:
		f_mq_open();
		break;	
	case MQ_CLOSE:
		f_mq_close();
		break;
	case MQ_UNLINK:
		f_mq_unlink();
		break;
	case MQ_RECEIVE:
		f_mq_receive();
		break;
	case MQ_SEND:
		f_mq_send();
		break;

	case SHM_GET:
		f_shm_get();
		break;
	case SHM_AT:
		f_shm_at();
		break;
	case SHM_DT:
		f_shm_dt();
		break;
	case SHM_CTL:
		f_shm_ctl();
		break;
	
	case MEMORY_MALLOC:
		f_memory_malloc();
		break;
	case MEMORY_FREE:
		f_memory_free();
		break;


  }




}







}
