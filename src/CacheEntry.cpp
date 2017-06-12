#include "rbc/CacheEntry.h"


namespace rbc {
CacheEntry::CacheEntry( Mempool *mempool ):mempool(mempool){
    cache_entry = NULL;
    inflight_flush = false;
    dirty = false;
}

CacheEntry::~CacheEntry(){
    if( cache_entry ){
        delete cache_entry->data_map;
        delete cache_entry;
        mempool->rm( "CacheEntry", sizeof(CacheEntry_t) );
    }
}

void CacheEntry::init( uint64_t object_size, std::string name, std::string location_id, uint64_t offset){
    entry_lock.lock();

    cache_entry = new CacheEntry_t();
    mempool->add( "CacheEntry",sizeof(CacheEntry_t) );
    cache_entry->name = name;
    cache_entry->location_id = location_id;
    cache_entry->offset = offset;
    cache_entry->if_dirty = false;
    cache_entry->ts = 0; // Thu Jan  1 00:00:00 1970

    cache_entry->data_map = new AllocateMap( mempool );

    entry_lock.unlock();
}

void CacheEntry::reset(){
    entry_lock.lock();
    if(cache_entry && (std::time(nullptr) > cache_entry->ts)){
        delete cache_entry->data_map;
        delete cache_entry;
        cache_entry = NULL;
        mempool->rm( "CacheEntry",sizeof(CacheEntry_t) );
    }
    entry_lock.unlock();
}

bool CacheEntry::data_map_lookup( uint64_t offset, uint64_t length ){
    bool if_exists = false;
    entry_lock.lock();
    if_exists = cache_entry->data_map->lookup( offset, length );
    entry_lock.unlock();
    return if_exists;

}

void CacheEntry::data_map_update( uint64_t offset, uint64_t length ){
    entry_lock.lock();
    auto in_time_t = std::time(nullptr);
    cache_entry->ts = in_time_t;
    cache_entry->data_map->update( offset, length );
    entry_lock.unlock();
}

DATAMAP_T CacheEntry::get_data_map(){
    DATAMAP_T tmp_map;
    entry_lock.lock();
    tmp_map = cache_entry->data_map->get();
    entry_lock.unlock();
    return tmp_map;
}

std::string CacheEntry::get_name(){
    std::string name;
    entry_lock.lock();
    name = cache_entry->name;
    entry_lock.unlock();
    return name;
}

std::string CacheEntry::get_location_id(){
    std::string location_id;
    entry_lock.lock();
    location_id = cache_entry->location_id;
    entry_lock.unlock();
    return location_id;

}

std::time_t CacheEntry::get_ts() {
    std::lock_guard<std::mutex> guard(entry_lock);
    return cache_entry->ts;
}

uint64_t CacheEntry::get_offset(){
    uint64_t offset = 0;
    entry_lock.lock();
    offset = cache_entry->offset;
    entry_lock.unlock();
    return offset;
}

void CacheEntry::set_cache_dirty(){
    dirty = true;
}

void CacheEntry::set_cache_clean(){
    dirty = false;
}

bool CacheEntry::get_if_dirty(){
    return dirty;
}

bool CacheEntry::is_null(){
    bool is_null = false;
    entry_lock.lock();
    if( !cache_entry )
        is_null = true;
    entry_lock.unlock();
    return is_null;
}

std::string CacheEntry::toString(){
    std::stringstream ss;
    boost::archive::binary_oarchive oa(ss);
    entry_lock.lock();
    cache_entry->if_dirty = dirty.load();
    DATAMAP_T tmp_map = cache_entry->data_map->get();
    oa << cache_entry->location_id;
    oa << cache_entry->offset;
    oa << cache_entry->if_dirty;
    oa << cache_entry->ts;
    oa << tmp_map;
    entry_lock.unlock();
    return ss.str();
}

void CacheEntry::load_from_string( std::string s ){
    std::stringstream ss(s);
    DATAMAP_T tmp_map;
    std::stringstream ss_name;
    boost::archive::binary_iarchive ia(ss);

    entry_lock.lock();
    cache_entry = new CacheEntry_t();
    mempool->add( "CacheEntry", sizeof(CacheEntry_t) );

    ia >> cache_entry->location_id;
    ia >> cache_entry->offset;
    ia >> cache_entry->if_dirty;
    ia >> cache_entry->ts;
    ia >> tmp_map;
    ss_name << cache_entry->location_id << "-" << cache_entry->offset;
    cache_entry->name = ss_name.str();
    dirty = cache_entry->if_dirty;
    cache_entry->data_map = new AllocateMap( mempool );
    cache_entry->data_map->set( tmp_map );
    entry_lock.unlock();
}
}
