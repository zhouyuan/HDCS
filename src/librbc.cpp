#include "rbc/librbc.h"

namespace rbc {

librbc::librbc(const char* rbd_name) {
    csd = new CacheService(rbd_name);
}

librbc::~librbc() {
    if (csd)
        delete csd;
}

int librbc::rbc_aio_read( const char* location, uint64_t offset, uint64_t length, char* data, rbc_completion_t c ){
    void* arg = (void*)c;
    Msg* msg = new Msg( location, offset, data, length, MSG_READ );
    Request *req = new Request( msg, REQ_LIBRARY_AIO, arg );
    csd->queue_io(req);
    return 0;
}

int librbc::rbc_aio_write( const char* location, uint64_t offset, uint64_t length, const char* data, rbc_completion_t c ){
    /*
    AioCompletion* comp = (AioCompletion*) c;
    comp->complete(0);
    return 0;
    */
    void* arg = (void*)c;
    Msg *msg = new Msg( location, offset, data, length, MSG_WRITE );
    Request *req = new Request( msg, REQ_LIBRARY_AIO, arg );
    csd->queue_io(req);

    return 0;
}

int librbc::rbc_aio_flush(const char* location, rbc_completion_t c)
{
    void* arg = (void*)c;
    Msg *msg = new Msg( location, 0, nullptr, 0, MSG_FLUSH );
    Request *req = new Request( msg, REQ_LIBRARY_AIO, arg );
    csd->queue_io(req);

    return 0;
}

int librbc::rbc_aio_discard(const char* location, uint64_t offset, uint64_t length, rbc_completion_t c)
{
    void* arg = (void*)c;
    Msg *msg = new Msg( location, offset, nullptr, length, MSG_DISCARD );
    Request *req = new Request( msg, REQ_LIBRARY_AIO, arg );
    csd->queue_io(req);

    return 0;
}

int librbc::rbc_read( const char* location, uint64_t offset, uint64_t length, char* data ){
    SafeCond* cond = new SafeCond();
    void* arg = (void*)cond;
    Msg* msg = new Msg( location, offset, data, length, MSG_READ );
    Request *req = new Request( msg, REQ_LIBRARY, arg );
    csd->queue_io(req);

    cond->wait();
    if(req->msg->header.type==MSG_FAIL){
	return req->msg->header.reserve;
    }else if(req->msg->header.type==MSG_SUCCESS){
        uint64_t len = req->msg->header.content_length;
        memcpy(data, req->msg->content, len);
        delete req;
        return len;
    }
}

int librbc::rbc_write( const char* location, uint64_t offset, uint64_t length, const char* data ){
    SafeCond* cond = new SafeCond();
    void* arg = (void*)cond;
    Msg *msg = new Msg( location, offset, data, length, MSG_WRITE );
    Request *req = new Request( msg, REQ_LIBRARY, arg );
    csd->queue_io(req);

    cond->wait();
    ssize_t ret=req->msg->header.reserve;
    delete req;
    return ret;
}

int librbc::rbc_aio_write_around( const char* location, uint64_t offset, uint64_t length, const char* data, rbc_completion_t c ){
    std::string rbd_name(location);
    C_AioBackendCompletion *onfinish = new C_AioBackendWriteAround( (void*)c );
    int ret = csd->cct->backendstore->aio_write( rbd_name, offset, length, data, "rbd", onfinish );

    return ret;
}

int librbc::rbc_aio_read_around( const char* location, uint64_t offset, uint64_t length, char* data, rbc_completion_t c ){
    std::string rbd_name(location);
    C_AioBackendCompletion *onfinish = new C_AioBackendReadAround( (void*)c );
    int ret = csd->cct->backendstore->aio_write( rbd_name, offset, length, data, "rbd", onfinish );

    return ret;
}
}
