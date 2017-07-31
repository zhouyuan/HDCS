#ifndef C_AIOREPLICATIONCOMPLETIONIMP_H
#define C_AIOREPLICATIONCOMPLETIONIMP_H

#include "rbc/common/AioCompletion.h"
#include "rbc/common/Op.h"
#include "rbc/common/FailoverHandler.h"

namespace rbc{
class C_AioReplicationCompletion : public AioCompletion{
public:
    Op *op;
    C_AioReplicationCompletion(Op *op): op(op){
        type = COMP_REPLICA;
        assert(op->req != NULL);
        op->req->req_lock.lock();
        op->req->uncomplete_count++;
        op->req->req_lock.unlock();
    }
    ~C_AioReplicationCompletion(){}

    void complete(ssize_t r){
        //printf("C_AioReplicationCompletion\n");
        if( r < 0 ){
	    failover_handler(REPLICATE_FAILURE,NULL );
            log_err("C_AioReplicationCompletion finish failed, ret=%ld\n", r);
            delete op;
            assert(0);
        }
        op->commit(r);
    }

    std::string get_type(){
        std::string type("C_AioReplicationCompletion");
        return type;
    }
};

}

#endif
