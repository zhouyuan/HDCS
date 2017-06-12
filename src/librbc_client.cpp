#include "rbc/librbc_client.h"

namespace rbc {

librbc::librbc(const char* rbd_name) {
    Config config(rbd_name);
    /*std::string target_ip("10.10.5.13");
    std::string target_port("9090");*/
    std::string target_ip = config.configValues["master_ip"];;
    std::string target_port = config.configValues["messenger_port"];
    async_msg_client = new AsioClient(target_ip, target_port);
}

librbc::~librbc() {
    if (async_msg_client)
        delete async_msg_client;
}

int librbc::rbc_aio_read( const char* location, uint64_t offset, uint64_t length, char* data, rbc_completion_t c ){
    void* arg = (void*)c;
    Msg* msg = new Msg( location, offset, data, length, MSG_READ );
    int ret = async_msg_client->send_request(msg, arg);
    return ret;
}

int librbc::rbc_aio_write( const char* location, uint64_t offset, uint64_t length, const char* data, rbc_completion_t c ){
    void* arg = (void*)c;
    Msg *msg = new Msg( location, offset, data, length, MSG_WRITE );
    int ret = async_msg_client->send_request(msg, arg);
    return ret;
}
}
