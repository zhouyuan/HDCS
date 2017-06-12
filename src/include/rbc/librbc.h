#ifndef LIBRBC_H
#define LIBRBC_H
#include "rbc/CacheService.h"
#include "rbc/C_AioClientCompletion.h"

namespace rbc {

typedef void *rbc_completion_t;
static void rbc_aio_release(rbc_completion_t c){
    AioCompletion *comp = (C_AioClientCompletion*) c;
    delete comp;
}

static int rbc_aio_create_completion(void *cb_arg, callback_t complete_cb, rbc_completion_t *c){
    AioCompletion *comp = new C_AioClientCompletion(cb_arg, complete_cb);
    *c = (rbc_completion_t) comp;
    return 0;
}

class librbc{
public:
    librbc(const char* rbd_name);
    ~librbc();
    int rbc_aio_read( const char* location, uint64_t offset, uint64_t length, char* data, rbc_completion_t comp );
    int rbc_aio_write( const char* location, uint64_t offset, uint64_t length, const char* data, rbc_completion_t comp );
    int rbc_read( const char* location, uint64_t offset, uint64_t length, char* data );
    int rbc_write( const char* location, uint64_t offset, uint64_t length, const char* data );
    int rbc_aio_flush(const char* location, rbc_completion_t c);
    int rbc_aio_discard(const char* location, uint64_t offset, uint64_t length, rbc_completion_t c);
    int rbc_aio_write_around( const char* location, uint64_t offset, uint64_t length, const char* data, rbc_completion_t c );
    int rbc_aio_read_around( const char* location, uint64_t offset, uint64_t length, char* data, rbc_completion_t c );
private:
    CacheService *csd;
};
}
#endif
