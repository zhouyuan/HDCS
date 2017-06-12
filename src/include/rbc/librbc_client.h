#include "rbc/common/Config.h"
#include "rbc/Messenger/asioMessenger/AsioClient.h"
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
private:
    AsioClient *async_msg_client;
};
}
