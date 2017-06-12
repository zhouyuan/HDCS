#ifndef ALLOCATEMAP_H
#define ALLOCATEMAP_H

#include <mutex>
#include <map>
#include "Mempool.h"

namespace rbc{
    typedef std::map<uint64_t, uint64_t> DATAMAP_T;

class AllocateMap {
public:
    AllocateMap( Mempool *mempool ):mempool(mempool){
        assert(mempool != NULL);
        data_map_size = data_map.size();
    }

    ~AllocateMap(){
        mempool->rm("AllocateMap", data_map_size);
    }

    bool lookup( uint64_t offset, uint64_t length ){
        if( this->data_map.empty() ){
            return false;
        }
        DATAMAP_T::iterator it = this->data_map.lower_bound(offset);
        //check if the looking for offset is smaller than the first one
        if( it == data_map.begin() && offset < it->first ){
            return false;
        }
        if( it == data_map.end() ||  offset < it->first ) it--;
        if( it->first <= offset && (it->second + it->first) >= (offset + length) )
            return true;
        else
            return false;
    }

    void update( uint64_t offset, uint64_t length ){
        log_debug("AllocateMap::update start add off=%lu, len=%lu \n", offset, length );
        lock.lock();
        // return the biggest addr <= offset
        DATAMAP_T::iterator it_lower = data_map.lower_bound(offset);
        DATAMAP_T::iterator it_upper = data_map.lower_bound(offset+length);
        uint64_t tmp;
        bool go_break = false;

        //case 1: data_map is empty
        if( data_map.empty() ){
            data_map[ offset ] = length;
            log_debug("[empty]data_map offset:%lu, length:%lu\n", offset, length);
        }else if( it_lower == data_map.begin() && offset < it_lower->first ){
        //case 2: insert to head
            if( (offset + length) < it_lower->first ){
            //case 2.1: not overlap with right
                data_map[ offset ] = length;
                log_debug("[insert]data_map offset:%lu, length:%lu\n", offset, length);
            }else{
            //case 2.2: extend with right one
                if( it_upper != data_map.end() || it_upper->first > (offset + length) ) it_upper--;
                tmp =  ((offset + length) < (it_upper->first + it_upper->second)?(it_upper->first + it_upper->second):(offset+length)) - offset;
                data_map[ offset ] = tmp;
                //remove the blocks in the middle
                go_break = false;
                for( DATAMAP_T::iterator rm_it = it_lower; !go_break; rm_it++ ){
                    if( rm_it == it_upper )  go_break = true;
                    data_map.erase( rm_it );
                }
                log_debug("[update]data_map offset:%lu, length:%lu\n", offset, tmp);
            }
        }else{
        //case 3: insert to middle or end of map
            if(it_lower == data_map.end()){
            //case 3.1: insert at end of the map
                it_lower--;
                if((it_lower->first + it_lower->second) < offset){
                //case 3.1.1: no overlap with left one
                    data_map[offset] = length;
                    log_debug("[insert]data_map offset:%lu, length:%lu\n", offset, length);
                }else{
                //case 3.1.2: extend the left one or maybe inside the left one
                    if( (offset + length) > (it_lower->first + it_lower->second) ){
                    //case 3.1.2.1: to extend the last one
                        tmp = offset+length - it_lower->first;
                        data_map[ it_lower->first ] = tmp;
                        log_debug("[update]data_map offset:%lu, length:%lu\n", it_lower->first, tmp);
                    }
                }
            }else{
            //case 3.2: insert to middile
                if(it_lower == data_map.end() || it_lower->first > offset) it_lower--;
                if(it_upper == data_map.end() || it_upper->first > (offset+length)) it_upper--;
                if( it_lower == it_upper ){
                //case 3.2.1: only possibly overlap with left block
                    if( offset > (it_lower->first + it_lower->second) ){
                    //case 3.2.1.1: not overlap with left one
                        data_map[ offset ] = length;
                        log_debug("[insert]data_map offset:%lu, length:%lu\n", offset, length);
                    }else{
                    //case 3.2.1.2: to extend left one or maybe inside the left one
                        if( (offset + length) > (it_lower->first + it_lower->second) ){
                            tmp = offset+length - it_lower->first;
                            data_map[ it_lower->first ] = tmp;
                            log_debug("[update]data_map offset:%lu, length:%lu\n", it_lower->first, tmp);
                        }
                    }
                }else{
                //case 3.2.2: possibly overlap with more than one block, only need to consider the most left one and the most right one.
                    if( offset > (it_lower->first + it_lower->second) ){
                    //case 3.2.2.1: not overlap with left one
                        tmp =  (offset + length) < (it_upper->first + it_upper->second)?(it_upper->first + it_upper->second):(offset+length);
                        data_map[ offset ] = tmp;
                        log_debug("[update]data_map offset:%lu, length:%lu\n", offset, tmp);
                    }else{
                    //case 3.2.2.2: need to extend the left one
                        tmp =  ((offset + length) < (it_upper->first + it_upper->second)?(it_upper->first + it_upper->second):(offset+length)) - it_lower->first;
                        data_map[ it_lower->first ] = tmp;
                        //remove the blocks in the middle
                        go_break = false;
                        for( DATAMAP_T::iterator rm_it = ++it_lower; !go_break; rm_it++ ){
                            if( rm_it == it_upper )  go_break = true;
                            data_map.erase( rm_it );
                        }
                        log_debug("[update]data_map offset:%lu, length:%lu\n", it_lower->first, tmp);
                    }
                }
            }
        }
        mempool->update( "AllocateMap", data_map_size, data_map.size() );
        data_map_size = data_map.size();
        lock.unlock();
    }

    uint64_t get_size( uint64_t &bl_count ){
        uint64_t size = 0;
        bl_count = 0;
        for(DATAMAP_T::iterator it = this->data_map.begin(); it!=this->data_map.end(); it++){
            size += it->second;
            bl_count++;
        }
        return size;
    }

    DATAMAP_T get(){
        return data_map;
    }

    void set( DATAMAP_T tmp_map ){
        data_map.swap(tmp_map);
        mempool->update( "AllocateMap", data_map_size, data_map.size() );
        data_map_size = data_map.size();
    }

    void clear(){
        data_map.clear();
        mempool->update( "AllocateMap", data_map_size, data_map.size() );
        data_map_size = data_map.size();
    }

private:

    DATAMAP_T data_map;
    ssize_t data_map_size;
    std::mutex lock;
    Mempool *mempool;


};
}
#endif
