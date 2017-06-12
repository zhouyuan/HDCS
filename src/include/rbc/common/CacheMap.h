#ifndef CACHEMAP_H
#define CACHEMAP_H

#include <cassert>
#include <mutex>
#include <map>
#include <boost/unordered_map.hpp>

#include "Mempool.h"

namespace rbc {
class CacheMap{
public:
    typedef std::string key_type;
    typedef char* value_type;

    typedef boost::unordered::unordered_map< key_type, value_type > key_to_value_type;

    CacheMap( Mempool *mempool ):mempool(mempool){
        assert(mempool != NULL);
        _key_to_value_size = 0;
    }

    ~CacheMap(){
        mempool->rm( "CacheMap", _key_to_value_size );
    }

    // Record a fresh key-value pair in the cache
    void insert(const key_type& k,const value_type& v) {
      _lock.lock();
      _key_to_value.insert( std::make_pair(k, v) );
      mempool->update( "CacheMap", _key_to_value_size, _key_to_value.size() );
      _key_to_value_size = _key_to_value.size();
      _lock.unlock();
    }

    void evict(const key_type& k) {
      // Identify least recently used key
      _lock.lock();
      const typename key_to_value_type::iterator it =_key_to_value.find(k);
      if(it!=_key_to_value.end()){
          _key_to_value.erase(it);
          mempool->update( "CacheMap", _key_to_value_size, _key_to_value.size() );
          _key_to_value_size = _key_to_value.size();
      }
      _lock.unlock();
    }

    void get_values( value_type* dst ){
        _lock.lock();
        typename key_to_value_type::iterator it = _key_to_value.begin();
        for(; it != _key_to_value.end(); it++){
            *dst++ = it->second;
        }
        _lock.unlock();
    }

    ssize_t size(){
        _lock.lock();
        ssize_t size = _key_to_value.size();
        _lock.unlock();
        return size;
    }

    // Obtain value of the cached function for k
    value_type find_key(const key_type& k) {
      value_type v;
      _lock.lock();
      // Attempt to find existing record
      const typename key_to_value_type::iterator it =_key_to_value.find(k);

      if (it==_key_to_value.end()) {
        v = NULL;
      } else {
        v = it->second;
      }
      _lock.unlock();
      return v;
    }
private:

    // mutex lock of LRU list
    std::mutex _lock;
    // Key-to-value lookup
    key_to_value_type _key_to_value;
    ssize_t _key_to_value_size;
    Mempool* mempool;
};
}
#endif
