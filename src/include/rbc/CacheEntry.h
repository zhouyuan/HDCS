#ifndef CACHEENTRY_H
#define CACHEENTRY_H

#include <mutex>
#include <sstream>
#include <atomic>
#include <chrono>

#include <boost/archive/binary_oarchive.hpp>
#include <boost/archive/binary_iarchive.hpp>
#include <boost/serialization/string.hpp>
#include <boost/serialization/map.hpp>

#include "rbc/common/List.h"
#include "rbc/common/AllocateMap.h"
#include "rbc/common/RWLock.hpp"

namespace rbc {

class CacheEntry{
public:
    Mempool *mempool;

    CacheEntry( Mempool *mempool = NULL );
    ~CacheEntry();

    void reset();
    void init( uint64_t object_size, std::string name, std::string location_id, uint64_t offset);
    bool is_null();

    std::string get_name();
    std::string get_location_id();

    uint64_t get_offset();

    DATAMAP_T get_data_map();
    bool data_map_lookup( uint64_t offset, uint64_t length );
    void data_map_update( uint64_t offset, uint64_t length );

    bool get_if_dirty();
    void set_cache_dirty();
    void set_cache_clean();
    std::time_t get_ts();

    std::string toString();
    void load_from_string( std::string s );

    std::atomic<bool> inflight_flush;
    std::atomic<bool> dirty;

    smutex rwlock;

private:
    struct CacheEntry_t {
        std::string name; // RBD image name + offset
        std::string location_id; //RBD image name
        uint64_t offset;
        bool if_dirty;
        AllocateMap *data_map;
        std::time_t ts; // last update timestamp
    };
    std::mutex  entry_lock;
    CacheEntry_t *cache_entry;
};
}

#endif
