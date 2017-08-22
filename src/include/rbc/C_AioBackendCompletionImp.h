#ifndef C_AIOBACKENDCOMPLETIONIMP_H #define C_AIOBACKENDCOMPLETIONIMP_H 
#include "rbc/C_AioBackendCompletion.h"
#include "FailoverHandler.h"

namespace rbc{
struct C_AioBackendWrite : C_AioBackendCompletion{
    Op* op;

    C_AioBackendWrite( Op *op ) : op(op){
        op->cache_entry->inflight_flush = true;
    }
    void finish( ssize_t r ){
        //TODO: if rbd_aio_write fails, will be flushed in the next round
        op->mempool->free( (void*)op->data, sizeof(char) * op->length );
        if( r < 0 ){
            log_err("C_AioBackendCompletion finish failed, ret=%ld\n", r);
            op->cache_entry->inflight_flush = false;
            delete op;
	    failover_handler(BACKEND_RADOS_AIO_WRITE);
            return;
        }

        op->cct->flush_op_count--;
        if(op->cct->flush_op_count < op->cct->cache_flush_queue_depth)
            op->cct->flush_qd_cond.notify_one();
        if(op->cct->flush_op_count == 0)
            op->cct->flush_stop_cond.notify_one();
        WriteLock cache_entry_w_lock(op->cache_entry->rwlock);
        if (op->ts < op->cache_entry->get_ts()) {
            //TODO:
            // ts0: flush_op_0
            // ts1: write_op_1
            // write_op_1 happens before flush_op_0
            log_print("C_AioBackendCompletion finish ignore old flush\n");
            op->cache_entry->inflight_flush = false;
            delete op;
            return;
        }
        op->cache_entry->set_cache_clean();
        op->cache_entry->inflight_flush = false;
        op->metastore_update();
        op->cct->lru_dirty->remove( (char*)op->cache_entry );
        op->cct->lru_clean->touch_key( (char*)op->cache_entry );

        delete op;
    }
};

struct C_AioBackendRead : C_AioBackendCompletion{

    Op *op;
    C_AioBackendRead( Op *op ): op(op){}

    void finish( ssize_t r ){
        //log_print("C_AioBackendRead::finish ret=%ld\n", r);
        op->cct->backend_aio_read_count--;
        if( r < 0 ){
            //TODO: read failed
            op->commit(r);
	    failover_handler(BACKEND_RADOS_AIO_READ);
            return;
        }
        assert( r == op->length );
        int ret = op->datastore_write();
        if( ret == 0 ){
            op->cache_entry->data_map_update( op->offset % op->cct->object_size, op->length );
        }
        op->commit(r);

    }
};

struct C_AioBackendWriteAround : C_AioBackendCompletion{

    AioCompletion* comp;
    C_AioBackendWriteAround( void* c ){
        comp = (AioCompletion*)c;
    }

    void finish( ssize_t r ){
        //log_print("C_AioBackendWriteAround::finish ret=%ld\n", r);
        comp->complete(r);
    }

};

struct C_AioBackendReadAround : C_AioBackendCompletion{

    AioCompletion* comp;
    C_AioBackendReadAround( void* c ){
        comp = (AioCompletion*)c;
    }

    void finish( ssize_t r ){
        //log_print("C_AioBackendReadAround::finish ret=%ld\n", r);
        comp->complete(r);
    }

};
}
#endif
