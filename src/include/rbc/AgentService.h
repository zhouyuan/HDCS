#ifndef AGENTSERVICE_H
#define AGENTSERVICE_H

#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <iostream>
#include <condition_variable>
#include <thread>

#include "rbc/common/Request.h"
#include "rbc/common/WorkQueue.h"
#include "rbc/common/Op.h"
#include "rbc/common/LRU_Linklist.h"
#include "rbc/common/Context.h"
#include "rbc/CacheEntry.h"
#include "rbc/C_AioBackendCompletionImp.h"


namespace rbc {

class AgentService{

private:
    Context *cct;
    ThreadPool *threadpool;
    ThreadPool *process_tp;

    int cache_evict_interval;
    int cache_flush_interval;
    uint64_t cache_total_size;
    uint64_t object_size;
    float cache_free_ratio;
    float cache_dirty_ratio_min;
    float cache_ratio_max;
    float cache_ratio_health;

    void _process_evict();
    void _process_flush();
    void flush( CacheEntry** c_entry_list );
    void evict( CacheEntry** c_entry_list );

public:
    AgentService( Context* cct );
    ~AgentService();

    void do_flush( CacheEntry* c_entry );
    void flush_all();
    void do_evict( CacheEntry* c_entry );

    void flush_by_ratio( float target_ratio );
    void evict_by_ratio();
};


}
#endif
