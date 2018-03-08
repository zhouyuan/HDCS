#ifndef RDMA_INTERNAL_CALLBACK
#define RDMA_INTERNAL_CALLBACK

/* wrapper for rdma callback function 
 *
 * hdcs_handle_msg can be posted to thread_group 
 */
#include <string>

#include "../common/counter.h"
#include "../common/Message.h"
#include "../common/session_arg.h"
#include "rdma_session.h"

namespace hdcs{
namespace networking{

// reading of callback.
class InternalProcessMsg : public Callback 
{
public:
    enum 
    {
        READING_HEADER = 0,
        READING_CONTENT = 1,
    };
    
    // 0--server, 1--client
    InternalProcessMsg(ProcessMsg _process_msg, const int _role)  
        : hdcs_handle_msg(_process_msg)
        , msg_header(new char[sizeof(MsgHeader)]) 
        , read_status(READING_HEADER)
        , hdcs_handle_msg_param(NULL)
        , role(_role)
    {}

    ~InternalProcessMsg()
    {
        delete[] msg_header;
    }
    
    // callback 
    virtual void entry(void *param, void* msg = nullptr) override 
    {
        RDMAConnection *con = static_cast<RDMAConnection*>(param); 
        Chunk *ck = static_cast<Chunk*>(msg);

        // configurable array size TODO
        // must ensure : (block_size + msg_header_size) < 8192 
        char* buf_ptr = new char[8192];
        uint64_t buf_size = ck->chk_size;

        memcpy(buf_ptr, ck->chk_buf, ck->chk_size);

        if(role == 0)
        {
            // server side
            if(rdmaconn_to_session.find(con) == rdmaconn_to_session.end())
            {
                std::cout<<"rdma_InternalProcessMsg: can't find session.."<<std::endl;
                assert(0);
            }
            SessionArg* temp_session_arg = new SessionArg(rdmaconn_to_session[con]);
            hdcs_handle_msg(temp_session_arg, std::string(buf_ptr, buf_size));
        }
        else
        {
            // client side
            hdcs_handle_msg(hdcs_arg, std::string(buf_ptr, buf_size));
        }

        delete[] buf_ptr;

        return;
    }

    // for client
    void set_hdcs_arg(void* arg)
    {
        hdcs_arg = arg;
    }

    void insert_new_session(RDMAConnection* _conn, void* session_id)
    {
        if(rdmaconn_to_session.find(_conn) == rdmaconn_to_session.end())
        {
            rdmaconn_to_session[_conn] = session_id;
        }
    }

private:
    ProcessMsg hdcs_handle_msg;
    void* hdcs_handle_msg_param;
    volatile int read_status;
    char* msg_header;
    char* msg_content;
    uint32_t msg_header_size;
    uint32_t msg_content_size;
    std::map<RDMAConnection*, void*> rdmaconn_to_session;
    const int role;
    void* hdcs_arg;
};

// callback of connection
// when this function be called, express that connection action success
// So, create a session
class InternalOnConnection : public Callback 
{
public:
    InternalOnConnection(std::vector<Session*>& _s_v, const int _s_n, WaitEvent& _wait_event)
        : session_vec(_s_v)
        , session_num(_s_n)
        , wait_event(_wait_event)
    {}

    virtual ~InternalOnConnection()
    {}

    virtual void entry(void *param, void* msg = nullptr) override 
    {
        // obtain new RDMAConnection
        RDMAConnection *con = static_cast<RDMAConnection*>(param); 
        assert(_internal_process_msg_ptr);
        // set msg handing function for new rdma connection
        con->set_read_callback(_internal_process_msg_ptr.get());
        // use session to wrap new rdma connection 
        Session* new_session = new rdma_session(con);
        session_vec.push_back(new_session);
        if(session_vec.size() == session_num)
        {
            // connection have been finished, namely all sessions have been created.
            wait_event.Signal();
        }
    }

    void set_process_msg(std::shared_ptr<InternalProcessMsg> _p_m)
    {
       _internal_process_msg_ptr = _p_m;
  
    }

private:
    std::shared_ptr<InternalProcessMsg> _internal_process_msg_ptr;
    std::vector<Session*>& session_vec;
    const int session_num;
    WaitEvent& wait_event;
};

// callback of accept
// when this function be called, express that a connection request have arrived.
class InternalOnAccept : public Callback
{
public:
    InternalOnAccept(SessionSet& s_s)
        : session_set(s_s)
    {}

    ~InternalOnAccept()
    {
        // TODO delete session. 
    }

    virtual void entry(void *param, void* msg = nullptr) override 
    {
        RDMAConnection* conn = static_cast<RDMAConnection*>(param);
        assert(_internal_process_msg_ptr);
        conn->set_read_callback(_internal_process_msg_ptr.get());

        new_session = new rdma_session(conn);

        session_set.insert(new_session);

        _internal_process_msg_ptr->insert_new_session(conn, (void*)new_session);

    }

    void set_process_msg(std::shared_ptr<InternalProcessMsg> _p_m)
    {
        _internal_process_msg_ptr = _p_m;
    }

private:
    SessionPtr new_session;
    SessionSet& session_set;
    std::shared_ptr<InternalProcessMsg> _internal_process_msg_ptr;

};

}// namespace networking
}// namespace hdcs

#endif
