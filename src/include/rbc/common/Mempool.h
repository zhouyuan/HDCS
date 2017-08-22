#ifndef MEMPOOL_H
#define MEMPOOL_H

#include <mutex>

#include "MemoryUsageTracker.h"
#include "FailoverHandler.h"

namespace rbc{
class Mempool{
public:
    Mempool( bool enable_mem_tracker = false ){
        if( enable_mem_tracker ){
            mem_tracker = new MemoryUsageTracker();
        }else{
            mem_tracker = NULL;
        }
    }
    ~Mempool(){
        if(mem_tracker)
            delete mem_tracker;
    }

    void* malloc( ssize_t len ){
        if(mem_tracker)
            mem_tracker->add( "Mempool", len);// if malloc fails?
        void* p = std::malloc( len );
	if(NULL==p){
		failover_handler(MEMORY_MALLOC,NULL);
	}
        memset(p, 0, len);
        return p;
    }

    void free( void* p, ssize_t len ){
        if(mem_tracker)
            mem_tracker->rm( "Mempool", len);
        std::free(p);
    }

    void add( std::string type, ssize_t len ){
        if(mem_tracker)
            mem_tracker->add( type, len );
    }

    void rm( std::string type, ssize_t len ){
        if(mem_tracker)
            mem_tracker->rm( type, len );
    }

    void update( std::string type, ssize_t orig_len, ssize_t new_len ){
        if(mem_tracker)
            mem_tracker->update( type, orig_len, new_len );
    }

    void print_total(){
        if(mem_tracker)
            mem_tracker->print_total();
    }
private:
    MemoryUsageTracker* mem_tracker;

};
}
#endif
