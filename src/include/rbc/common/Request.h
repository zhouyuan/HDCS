#ifndef REQUEST_H
#define REQUEST_H

#define REQ_MESSENGER 0X0010
#define REQ_LIBRARY   0X0011
#define REQ_LIBRARY_AIO   0X0012

#include <mutex>
#include <atomic>
#include <cassert>
#include "rbc/Message.h"
#include "rbc/common/AsyncIO.h"
#include "rbc/common/AioCompletion.h"
#include "rbc/common/Cond.h"
#include "rbc/common/Log.h"
#include "rbc/Messenger/Messenger.h"
namespace rbc {
//class Request;
//typedef int (*callback_t)(const char* data, uint64_t length, Request* req);

class Request{
public:
    Msg* msg;
    std::mutex req_lock;
    async_io_unit *io_u;
    SafeCond* cond;
    AioCompletion* comp;

    int socket_fd;
    int source_type;

    std::time_t ts;
    std::atomic<std::uint64_t> uncomplete_count;

    Request( Msg* msg, int source_type, void* arg ):msg(msg), source_type(source_type){
        switch(source_type){
            case REQ_MESSENGER:
                io_u = (async_io_unit*)arg;
                cond = NULL;
                comp = NULL;
                break;
            case REQ_LIBRARY:
                cond = (SafeCond*)arg;
                io_u = NULL;
                comp = NULL;
                break;
            case REQ_LIBRARY_AIO:
                comp = (AioCompletion*)arg;
                io_u = NULL;
                cond = NULL;
                break;
            default:
                break;
        }
        req_status = 0;
        completed = false;
        ts = std::time(nullptr);
    }

    ~Request(){
        if(cond!=NULL)
            delete cond;
    }

    int complete(){
        int ret = 1;
        if( source_type == REQ_LIBRARY ){
	    if(req_status<0){
	        msg->set_type(MSG_FAIL);
	     }else{
	        msg->set_type(MSG_SUCCESS);	
	     }
	    msg->set_reserve(req_status);
            cond->Signal();
        }else if( source_type == REQ_LIBRARY_AIO ){
            comp->complete(req_status);
            ret = 0;
        }else if( source_type == REQ_MESSENGER ){
            if( msg->header.type == MSG_WRITE ){
                msg->set_type(MSG_REPLY_STAT);
                msg->set_length(0);
                msg->set_reserve(req_status);
            }else if( msg->header.type == MSG_READ ){
                msg->set_type(MSG_REPLY_DATA);
                msg->set_length(req_status);
            }

            io_u->reply_request( msg );
            ret = 0;
            delete io_u;
            delete msg;
        }
        return ret;
    }

    void update_status( ssize_t data ){
        if( data < 0 )
            req_status = data;
        else if( req_status >= 0 )
            req_status += data;
    }

    bool if_complete(){
        if( uncomplete_count == 0 )
            return true;
        return false;
    }
private:
    ssize_t req_status;
    bool completed;
};
}
#endif
