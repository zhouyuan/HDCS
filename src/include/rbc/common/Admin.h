#ifndef ADMIN_H
#define ADMIN_H

#include "rbc/Message.h"
#include "rbc/common/LRU_Linklist.h"

#define ADMIN_GET 0X0001
#define ADMIN_SET 0X0002
#define CACHE_CACHE 0X0010
#define CACHE_DIRTY 0X0011
#define CACHE_CLEAN 0X0012

namespace rbc{

class Admin{
public:
    Admin(LRU_LIST<char*> *lru_dirty, LRU_LIST<char*> *lru_clean, uint64_t object_size):
        lru_dirty(lru_dirty),lru_clean(lru_clean),object_size(object_size){}

    ~Admin(){}

    std::string exec( std::vector<std::string> requestv ){
        uint64_t ret = 0;
        if( requestv[0].compare("get") == 0 ){
            uint64_t dirty_block_count = lru_dirty->get_length();
            uint64_t clean_block_count = lru_clean->get_length();
            uint64_t object_size = object_size; 
            uint64_t total_cached_block = dirty_block_count + clean_block_count;
            if( requestv[1].compare("cache_size") == 0 ){
                ret = total_cached_block * object_size;
            }else if( requestv[1].compare("cache_dirty") == 0 ){
                ret = dirty_block_count * object_size;
            }else if( requestv[1].compare("cache_clean") == 0 ){
                ret = clean_block_count * object_size;
            }else{
                std::string ret_str("Unrecognized request");
                return ret_str;
            }
        }else if( requestv[0].compare("set") == 0 ){

        }else{
            std::string ret_str("Unrecognized request");
            return ret_str;
        }
        std::string ret_str = std::to_string(ret);
        return ret_str;
    }    

private:
    LRU_LIST<char*> *lru_dirty;
    LRU_LIST<char*> *lru_clean;
    uint64_t object_size;



};

}

#endif
