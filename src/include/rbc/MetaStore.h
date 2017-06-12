#ifndef METASTORE_H
#define METASTORE_H

#include <stdio.h>
#include <string>
#include <sstream>

#include <rocksdb/db.h>
#include <rocksdb/slice.h>
#include <rocksdb/options.h>
#include <boost/unordered_map.hpp>

#include "rbc/CacheEntry.h"
#include "rbc/common/Log.h"
#include "rbc/common/CacheMap.h"
#include "rbc/common/LRU_Linklist.h"
#include "rbc/common/Mempool.h"

namespace rbc {
class MetaStore {

public:
  MetaStore( std::string kDBPath );
  ~MetaStore();

  typedef boost::unordered::unordered_map<uint64_t, std::pair<uint64_t, std::time_t>> BLOCK_INDEX;
  int get(const char* oid, char* data);
  int put(std::string key, std::string val);
  int remove(std::string key);
  int get_all( CacheMap *cache_map, LRU_LIST<char*> *lru_dirty, LRU_LIST<char*> *lru_clean, Mempool* mempool = NULL );
  int get_all( BLOCK_INDEX *block_map, bool* cached_array, uint64_t object_size );

private:
  rocksdb::DB *db;
  rocksdb::Options options;
  std::string kDBPath;

};
}

#endif
