#ifndef MEMORYUSAGETRACKER_H
#define MEMORYUSAGETRACKER_H

#include <map>
#include <mutex>
#include <string.h>
#include <boost/algorithm/string.hpp>

#include "Log.h"

namespace rbc{
class MemoryUsageTracker{
public:
    MemoryUsageTracker(){
    }

    void add( std::string type, ssize_t len ){
        std::map<std::string, ssize_t>::iterator it = mem_map.find( type );
        total_use_lock.lock();
        if( it != mem_map.end() ){
            it->second += len;
        }else{
            mem_map.insert( std::make_pair( type, len) );
        }
        total_use_lock.unlock();
    }

    void rm( std::string type, ssize_t len ){
        std::map<std::string, ssize_t>::iterator it = mem_map.find( type );
        if( it != mem_map.end() ){
            total_use_lock.lock();
            it->second -= len;
            total_use_lock.unlock();
        }
    }

    void update( std::string type, ssize_t orig_len, ssize_t new_len ){
        std::map<std::string, ssize_t>::iterator it = mem_map.find( type );
        total_use_lock.lock();
        if( it != mem_map.end() ){
            it->second -= orig_len;
            it->second += new_len;
        }else{
            if( orig_len == 0 )
                mem_map.insert( std::make_pair( type, new_len) );
        }
        total_use_lock.unlock();
    }

    void print_total(){
        for( std::map<std::string, ssize_t>::iterator it = mem_map.begin(); it!=mem_map.end(); it++ ){
            log_print("%s memory usage: %.3lf MB\n", it->first.c_str(), (it->second*1.000)/1024/1024 );
        }
    }

    ssize_t get_value(std::string type){
        std::map<std::string, ssize_t>::iterator it = mem_map.find( type );
        if( it != mem_map.end() ){
            return it->second;
        }else{
            return 0;
        }
    }
private:
    std::map<std::string, ssize_t> mem_map;
    std::mutex total_use_lock;
};
}
#endif
