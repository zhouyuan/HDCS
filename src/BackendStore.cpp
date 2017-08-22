#include "rbc/BackendStore.h"
#include "rbc/common/FailoverHanlder.h"

static void rbc_backend_finish_aiocb( rbd_completion_t comp, void *data ){
    //rbc::log_print("rbc_backend_finish_aiocb\n");
    rbd_aio_unit *io_u = (rbd_aio_unit*)data;
    ssize_t ret = rbd_aio_get_return_value(comp);
    //rbc::log_print("rbc_backend_finish_aiocb, get_return_value: %d\n", ret);
    io_u->onfinish->finish( ret );
    delete io_u;
}

namespace rbc {

BackendStore::BackendStore( const char* client_name ){
    int r;

    r = rados_create(&cluster, client_name);
    if (r < 0) {
	failover_handler(BACKEND_RADOS_CREATE,NULL);
        log_err("rados_create failed.\n");
        goto failed_early;
    }

    r = rados_conf_read_file(cluster, NULL);
    if (r < 0) {
	failover_handler(BACKEND_RADOS_READ_CONF_FILE,NULL);
        log_err("rados_conf_read_file failed.\n");
        goto failed_early;
    }

    r = rados_connect(cluster);
    if (r < 0) {
	failover_handler(BACKEND_RADOS_CONNECT,NULL);
        log_err("rados_connect failed.\n");
        goto failed_shutdown;
    }
    return;
failed_shutdown:
    log_err("failed_shutdown\n");
    rados_shutdown(cluster);
    cluster = NULL;
failed_early:
    log_err("failed_early\n");
    return;
}

BackendStore::~BackendStore(){
    log_print("BackendStore destruction\n");
    for(std::map<std::string, rbd_data*>::iterator it=rbd_info_map.begin(); it!=rbd_info_map.end(); ++it){
        _close( it->second );
    }
    if(cluster){
        rados_shutdown(cluster);
        cluster = NULL;
    }
    log_print("BackendStore destruction complete\n");
}

int BackendStore::_open( std::string rbd_name, std::string pool_name ){
    rbd_data *rbd = new rbd_data( pool_name );
    //printf("connect to rados\n");
    int r = rados_ioctx_create(cluster, pool_name.c_str(), &rbd->io_ctx);
    if (r < 0) {
	r=BACKEND_RADOS_IOCTX_CREATE;
	failover_handler(BACKEND_RADOS_IOCTX_CREATE,NULL);
        log_err("rados_ioctx_create failed.\n");
        goto failed_shutdown;
    }

    //printf("rbd_open\n");
    log_print("BackendStore::open %s\n", rbd_name.c_str());
    r = rbd_open_skip_cache(rbd->io_ctx, rbd_name.c_str(), &rbd->image, NULL /*snap */ );
    //r = rbd_open(rbd->io_ctx, rbd_name.c_str(), &rbd->image, NULL /*snap */ );
    if (r < 0) {
	r=BACKEND_RADOS_OPEN_SKIP_CACHE;
	failover_handler(BACKEND_RADOS_OPEN_SKIP_CACHE, NULL);
        log_err("rbd_open failed.\n");
        goto failed_open;
    }

    log_print("add rbd into rbd_info_map\n");
    rbd_info_map[rbd_name] = rbd;
    return 0;

failed_open:
    log_err("failed_open\n");
    rados_ioctx_destroy(rbd->io_ctx);
    rbd->io_ctx = NULL;
failed_shutdown:
    log_err("failed_shutdown\n");
    rados_shutdown(cluster);
    cluster = NULL;
    return r;
}

int BackendStore::_close( std::string rbd_name ){
    std::map<std::string, rbd_data*>::iterator it = rbd_info_map.find(rbd_name);
    if(it==rbd_info_map.end())
        return 0;
    rbd_data* rbd = it->second;
    int ret = _close( rbd );
    if( ret == 0 ) delete rbd;
    return ret;
}

int BackendStore::_close( rbd_data* rbd ){
    rados_ioctx_destroy(rbd->io_ctx);
    //rbd_close(rbd->io_ctx);
    rbd->io_ctx = NULL;
    return 0;
}

BackendStore::rbd_data* BackendStore::find_rbd_data( std::string rbd_name, std::string pool_name,int &error_code ){
    int r = 0;
    rbd_info_map_lock.lock();
    std::map<std::string, rbd_data*>::iterator it = rbd_info_map.find(rbd_name);
    if( it == rbd_info_map.end() ){
        //printf("%s not open, open now\n", rbd_name.c_str());
        r = _open( rbd_name, pool_name );
        if( r < 0 ){
            rbd_info_map_lock.unlock();
	    error_code=r;
            return NULL;
        }
        it = rbd_info_map.find(rbd_name);
    }
    rbd_info_map_lock.unlock();
    return it->second;

}

int BackendStore::write( std::string rbd_name, uint64_t offset, uint64_t length, const char* data,
        std::string pool_name ){
    int r = 0;
    rbd_data* rbd = find_rbd_data( rbd_name, pool_name,r);
    if( !rbd )
        return r;
    r = _write( rbd,  offset, length, data );
    return r;
}

int BackendStore::aio_write( std::string rbd_name, uint64_t offset, uint64_t length, const char* data,
        std::string pool_name, C_AioBackendCompletion* onfinish ){
    int r = 0;
    rbd_data* rbd = find_rbd_data( rbd_name, pool_name,r );
    if( !rbd )
        return r;
    r = _aio_write( rbd,  offset, length, data, onfinish );
    return r;
}

int BackendStore::read( std::string rbd_name, uint64_t offset, uint64_t length, char* data,
        std::string pool_name ){
    int r = 0;
    rbd_data* rbd = find_rbd_data( rbd_name, pool_name,r );
    if( !rbd )
        return r;
    r = _read( rbd, offset, length, data );
    return r;
}

int BackendStore::aio_read( std::string rbd_name, uint64_t offset, uint64_t length, char* data,
        std::string pool_name, C_AioBackendCompletion* onfinish){
    int r = 0;
    rbd_data* rbd = find_rbd_data( rbd_name, pool_name,r );
    if( !rbd )
        return r;
    r = _aio_read( rbd, offset, length, data, onfinish );
    return r;
}

int BackendStore::_aio_write( rbd_data* rbd, uint64_t offset, uint64_t length, const char* data,
       C_AioBackendCompletion* onfinish ){
    rbd_aio_unit *io_u = new rbd_aio_unit( onfinish );
    int r = rbd_aio_create_completion(io_u, rbc_backend_finish_aiocb, &io_u->completion);
    if(r<0){
	failover_handler(BACKEND_RADOS_AIO_CREATE_COMPLETE,NULL);
	return BACKEND_RADOS_AIO_CREATE_COMPLETE;
    }
    //std::cerr << "rbd_aio_write: comp: " << io_u->completion << " offset: " << offset << " length: " << length<< std::endl;
    r = rbd_aio_write(rbd->image, offset, length, data, io_u->completion);
    if (r < 0) {
	failover_handler(BACKEND_RADOS_AIO_WEITE,NULL);
        log_err("queue rbd_aio_write failed.\n");
        return BACKEND_RADOS_AIO_WRITE;
    }
    return 0;
}

int BackendStore::_write( rbd_data* rbd, uint64_t offset, uint64_t length, const char* data ){
    //log_print("rbd_write: offset:%lu, length: %lu\n", offset, length);
    int r = rbd_write(rbd->image, offset, length, data);
    if (r < 0) {
	failover_handler(BACKEND_RADOS_WRITE,NULL);
	//assert(0);
        log_err("rbd_write failed.\n");
        return BACKEND_RADOS_WRITE;
    }
    return r;
}

ssize_t BackendStore::_aio_read( rbd_data* rbd, uint64_t offset, uint64_t length,
        char* data, C_AioBackendCompletion* onfinish ){
    //log_print("rbd_aio_read: offset:%lu, length: %lu\n", offset, length);
    rbd_aio_unit *io_u = new rbd_aio_unit( onfinish );
    ssize_t r = rbd_aio_create_completion(io_u, rbc_backend_finish_aiocb, &io_u->completion);
    if(r < 0){
	failover_handler(BACKEND_RADOS_AIO_CREATE_COMPLETE,NULL);
        log_err("rbd_read failed create completion.\n");
        return BACKEND_RADOS_AIO_CREATE_COMPLETE;
    }
    //std::cerr << "rbd_aio_read: comp: " << io_u->completion << " offset: " << offset << " length: " << length<< std::endl;
    r = rbd_aio_read(rbd->image, offset, length, data, io_u->completion);
    if (r < 0) {
	failover_handler(BACKEND_RADOS_AIO_READ,NULL);
	//assert(0);
        log_err("rbd_aio_read failed.\n");
        return BACKEND_RADOS_AIO_READ;
    }
    return r;
}

ssize_t BackendStore::_read( rbd_data* rbd, uint64_t offset, uint64_t length, char* data ){
    //log_print("rbd_read: offset:%lu, length: %lu\n", offset, length);
    ssize_t r = rbd_read(rbd->image, offset, length, data);
    if (r < 0) {
	failover_handler(BACKEND_RADOS_READ,NULL);
	//assert(0);
        log_err("rbd_read failed.\n");
        return BACKEND_RADOS_READ;
    }
    return r;
}
}
