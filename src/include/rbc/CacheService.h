#ifndef CACHESERVICE_H
#define CACHESERVICE_H

#include <stdio.h>
#include <string.h>
#include <sstream>
#include <signal.h>

#include "rbc/Message.h"
#include "rbc/CacheEntry.h"
#include "rbc/common/Request.h"
#include "rbc/common/WorkQueue.h"
#include "rbc/common/Context.h"
#include "rbc/common/Op.h"
#include "rbc/common/Cond.h"
#include "rbc/C_AioBackendCompletionImp.h"
#include "rbc/C_AioReplicationCompletion.h"
#include "rbc/AgentService.h"

#define BUFSIZE 256

namespace rbc {
class CacheService{

private:
    ThreadPool *threadpool;
    ThreadPool *process_tp;
    void do_op(Op *op);
    int do_read_op(Op *op);
    int do_write_op(Op *op);
    int do_flush_op(Op* op);
    int do_discard_op(Op* op);
    bool cache_lookup(Op *op, const char* oid);
    void dequeue_op();
    void _process();
    std::string get_index( std::string location_id, uint64_t offset );
    int do_promote(Op* orig_op);
    int write_hit( Op *op );
    int write_miss( Op *op );
    ssize_t read_hit( Op *op );
    ssize_t read_miss( Op* op );
    int metastore_update(const char* oid, const char* data_oid);
    std::list<Op*> map_request_by_entry( Request* req );
    AgentService *agentservice;

public:
    CacheService(const char* rbd_name, bool process_mode=false, bool if_master = false);
    Context *cct;
    ~CacheService();
    int queue_io( Request* req ) ;
};
}

#endif
