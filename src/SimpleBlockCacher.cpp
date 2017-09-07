#include "rbc/SimpleBlockCacher.h"
#include "rbc/common/FailoverHandler.h"
// MAKK

namespace rbc {

SimpleBlockCacher::SimpleBlockCacher(std::string device_name, std::string metastore_dir, uint64_t cache_total_size,
                                     uint64_t p_object_size, Mempool *mempool ): mempool(mempool), device_name(device_name), object_size(p_object_size), _total_size(cache_total_size){

    metastore = new MetaStore(metastore_dir);

    if (metastore == NULL) {
        assert(0);
    }


    cache_block_size = cache_total_size/object_size;

    //TODO: get free list from cache entry array, remove all metadata
    bool *cached_array = (bool*)mempool->malloc( sizeof(bool) * cache_block_size );
    metastore->get_all( &cache_index, cached_array, object_size );
    mempool->update( "SimpleBlockCacher", cache_index_size, cache_index.size() );
    cache_index_size = cache_index.size();

    // add new free node into the final position.
    free_node_head = (free_node*)mempool->malloc(sizeof(free_node));
    free_node* tmp = free_node_head;
    free_node* cur_tmp = tmp;
    for(uint64_t i = 0 ; i < cache_block_size; i++ ){
        if( cached_array[i] )
            continue;
        tmp->index = i;
        if( i < (cache_block_size - 1) ){
            free_node* next_tmp = (free_node*)mempool->malloc(sizeof(free_node));
            tmp->next = next_tmp;
            tmp = tmp->next;
        }else{
            tmp->next = NULL;
        }
        cur_tmp = tmp;
    }
    free_node_tail = cur_tmp;

    mempool->free( (void*)cached_array, sizeof(bool) * cache_block_size );

    device_fd = _open( device_name );

    if (device_fd < 0) {
        assert(0);
    }
}

SimpleBlockCacher::~SimpleBlockCacher(){
    mempool->rm( "SimpleBlockCacher",cache_index_size );
    free_node* tmp_node = free_node_head;
    while(tmp_node!=NULL){
        free_node* tmp_next = tmp_node->next;
        mempool->free( (void*)tmp_node, sizeof(free_node) );
        tmp_node = tmp_next;
    }

    delete metastore;

    _close( device_fd );
}

int SimpleBlockCacher::_open( std::string Device_Name ){
    int mode = O_CREAT | O_RDWR | O_SYNC, permission = S_IRUSR | S_IWUSR;
    int fd = ::open( Device_Name.c_str(), mode, permission );
    if ( fd <= 0 ) {
	failover_handler(SIMPLEBLOCKCACHE_FS_OPEN, NULL);
        log_err( "[ERROR] SimpleBlockCacher::SimpleBlockCacher, unable to open %s, error code: %d ", Device_Name.c_str(), fd );
        close(fd);
        return SIMPLEBLOCKCACHE_FS_OPEN;
    }

    struct stat file_st;
    memset(&file_st, 0, sizeof(file_st));
    if(-1==fstat(fd, &file_st)){
	failover_handler(SIMPLEBLOCKCACHE_FS_FSTAT,NULL);
	close(fd);
	return SIMPLEBLOCKCACHE_FS_FSTAT;
    }
    
    if (file_st.st_size < _total_size) {
        if (-1 == ftruncate(fd, _total_size)) {
            failover_handler(SIMPLEBLOCKCACHE_FS_FTRUNCATE, NULL);
            close(fd);
            return SIMPLEBLOCKCACHE_FS_FTRUNCATE;
        }
    }

    return fd;
}

int64_t SimpleBlockCacher::read_index_lookup( uint64_t cache_id ){
    int64_t off;
    cache_index_lock.lock();
    const typename BLOCK_INDEX::iterator it = cache_index.find( cache_id );
    if( it == cache_index.end() ){
        log_err("SimpleBlockCacher::read_index_lookup_can't find cache_id=%lu\n", cache_id);
        off = -1;
    }else{
        off = it->second.first;
    }
    cache_index_lock.unlock();
    return off;
}

int64_t SimpleBlockCacher::write_index_lookup( uint64_t cache_id, std::time_t ts, bool no_update=false ){
    cache_index_lock.lock();
    const typename BLOCK_INDEX::iterator it = cache_index.find( cache_id );

    //when io is small than object_size(let's say 4k here), we should do in-place write
    if( no_update && it!= cache_index.end() ){
        cache_index_lock.unlock();
        return it->second.first;
    }

    /*
    if (it!= cache_index.end() && (ts < it->second.second)) {
        cache_index_lock.unlock();
        log_print("SimpleBlockCacher::write_index_lookup: ignore old writes\n");
        return -1;
    }
    */

    int64_t free_index;
    free_index = free_lookup();
    if( free_index < 0 ){
        cache_index_lock.unlock();
        return free_index;
    }
    /*
    if( it != cache_index.end() ){
        update_cache_index(it, free_index, ts);
    }else{
        index_insert( cache_id, free_index, ts);
    }
    */
    cache_index_lock.unlock();
    return free_index;
}

int64_t SimpleBlockCacher::index_insert( uint64_t cache_id, uint64_t free_index, std::time_t ts ){
    cache_index.insert( std::make_pair( cache_id, std::make_pair(free_index, ts) ) );
    mempool->update( "SimpleBlockCacher", cache_index_size, cache_index.size() );
    cache_index_size = cache_index.size();
    return free_index;
}

int64_t SimpleBlockCacher::free_lookup(){
    int64_t free_index;
    if ( free_node_head != NULL ){
        free_node* this_node = free_node_head;
        free_index = this_node->index;
        free_node_head = this_node->next;
        mempool->free( (void*)this_node, sizeof(free_node) );
        return free_index;
    }else{
	failover_handler(SIMPLEBLOCKCACHE_FS_NO_SSD_SPACE, NULL);
        log_err("SimpleBlockCacher::free_lookup can't find free node\n");
        return SIMPLEBLOCKCACHE_FS_NO_SSD_SPACE;
    }
}

int SimpleBlockCacher::_remove( uint64_t cache_id ){
    int ret = 0;
    cache_index_lock.lock();
    const typename BLOCK_INDEX::iterator it = cache_index.find( cache_id );
    if( it != cache_index.end() ){

        uint64_t block_id = it->second.first;
        free_node* new_free_node = (free_node*)mempool->malloc(sizeof(free_node));
        new_free_node->index = block_id;
        new_free_node->next = NULL;
        free_node_tail->next = new_free_node;
        free_node_tail = new_free_node;

        cache_index.erase( it );
        mempool->update( "SimpleBlockCacher", cache_index_size, cache_index.size() );
        cache_index_size = cache_index.size();
        ret = metastore->remove(std::to_string(cache_id));// rocksdb's delete operation could fails.
    }
    cache_index_lock.unlock();
    return ret;
}

int SimpleBlockCacher::update_cache_index( const typename BLOCK_INDEX::iterator it, uint64_t free_index, std::time_t ts ){
    uint64_t block_id = it->second.first;
    free_node* new_free_node = (free_node*)mempool->malloc(sizeof(free_node));
    new_free_node->index = block_id;
    new_free_node->next = NULL;
    free_node_tail->next = new_free_node;
    free_node_tail = new_free_node;

    it->second = std::make_pair(free_index, ts);
    return 0;

}
int SimpleBlockCacher::update_index( uint64_t cache_id, uint64_t block_id, std::time_t ts ){

    cache_index_lock.lock();

    const typename BLOCK_INDEX::iterator it = cache_index.find( cache_id );

    if (it != cache_index.end() && ts < it->second.second) {
        //log_print("SimpleBlockCacher::update_index: ignore old writes\n");
        cache_index_lock.unlock();
        return 0;
    }

    if( it != cache_index.end() ){
        update_cache_index(it, block_id, ts);
    }else{
        index_insert( cache_id, block_id, ts);
    }

    cache_index_lock.unlock();

    return 0;

}


int SimpleBlockCacher::_close( int block_fd ){
    int ret = ::close(block_fd);
    if(ret < 0){
	failover_handler(SIMPLEBLOCKCACHE_FS_CLOSE, NULL);
        perror( "close block_fd failed" );
        return SIMPLEBLOCKCACHE_FS_CLOSE;
    }
    return 0;

}

uint64_t SimpleBlockCacher::get_block_index( uint64_t* index, uint64_t offset ){
  *index = offset / object_size;
  return offset % object_size;
}

int SimpleBlockCacher::_write( uint64_t cache_id, const char *buf, uint64_t offset, uint64_t length, std::time_t ts ){
    uint64_t block_id;
    if( length < object_size )
        block_id = write_index_lookup( cache_id, ts, true );
    else
        block_id = write_index_lookup( cache_id, ts );

    if(block_id < 0) {
        log_err( "[ERROR] SimpleBlockCacher::write_fd, unable to write data, block_id: %lu\n", cache_id );
        return block_id;
    }

    uint64_t index = 0;
    uint64_t off_by_block = get_block_index( &index, offset );
    int ret;
    uint64_t ondisk_off;

    ondisk_off = block_id * object_size + index * object_size;
    ret = pwrite( device_fd, buf, object_size, ondisk_off );
    //ret = 0;
    if (ret < 0) {
        log_err( "[ERROR] SimpleBlockCacher::write_fd, unable to write data, block_id: %lu\n", block_id );
	failover_handler(SIMPLEBLOCKCACHE_FS_WRITE, NULL); 
        return SIMPLEBLOCKCACHE_FS_WRITE;
    }
    // update cache index
    
    update_index(cache_id, block_id, ts);
    if(0!=posix_fadvise(device_fd, ondisk_off, length, POSIX_FADV_DONTNEED)){
	failover_handler(SIMPLEBLOCKCACHE_FS_POSIX_FADIVSE, NULL);
	return SIMPLEBLOCKCACHE_FS_POSIX_FADIVSE;
    }

    ret = metastore->put(std::to_string(cache_id), std::to_string(ondisk_off));
    if (ret < 0) {
        log_err( "[ERROR] SimpleBlockCacher::write_fd, unable to write metadata, block_id: %lu\n", block_id );
        return ret;
    }

    return 0;

}

ssize_t SimpleBlockCacher::_read( uint64_t cache_id, char *buf, uint64_t offset, uint64_t length ){
    uint64_t index = 0;
    int64_t block_id = read_index_lookup( cache_id );
    if(block_id < 0)
        return -1;
    uint64_t off_by_block = get_block_index( &index, offset );
    int ret;


    ret = pread( device_fd, buf, object_size, block_id * object_size + index * object_size );
    if ( ret < 0 ){
        log_err( "[ERROR] SimpleBlockCacher::read_fd, unable to read data, error code: %d ", ret );
	failover_handler(SIMPLEBLOCKCACHE_FS_READ, NULL);
        return SIMPLEBLOCKCACHE_FS_READ;
    }

    return length;
}

}
