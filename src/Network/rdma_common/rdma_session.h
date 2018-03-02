#ifndef RDMA_SESSION
#define RDMA_SESSION

#include "../common/Message.h"
#include "../common/session.h"

namespace hdcs{
namespace networking{

class rdma_session : public Session
{
private:
    RDMAConnection* rdma_connection;

public:
    rdma_session(RDMAConnection* conn)
    {
        rdma_connection = conn;
    } 

    ~rdma_session()
    {}

    void stop()
    {
        rdma_connection->fin();
    }

    void cancel()
    {
        // TODO
    }

    bool start()
    {
        return true;
    }

    int async_send(std::string send_buffer, uint64_t _seq_id)
    {
        rdma_connection->async_send(send_buffer.c_str(), send_buffer.size());
        return 0;
    }

    ssize_t communicate(std::string send_buffer, uint64_t _seq_id)
    {
        rdma_connection->async_send(send_buffer.c_str(), send_buffer.size());
        // TODO TODO TODO TODO 
        // waiting for sync send interface which shoud be offerd by rdma_messenger.
        sleep(1); 
        return 0;
    }

    void aio_communicate(std::string& send_buffer, uint64_t _seq_id)
    {
        rdma_connection->async_send(send_buffer.c_str(), send_buffer.size());
    }

    // timeout 
    bool if_timeout()
    {
        // TODO
        return true;
    }

    COMMUNICATION_TYPE communication_type()
    {
        return (COMMUNICATION_TYPE)1;
    }


};//class rdma_session

}//networking
}//hdcs
#endif
