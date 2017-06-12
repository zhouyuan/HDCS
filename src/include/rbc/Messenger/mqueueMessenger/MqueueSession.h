#ifndef RBC_MQUEUE_SESSION_H
#define RBC_MQUEUE_SESSION_H

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <errno.h>
#include <mqueue.h>
#include "rbc/Messenger/mqueueMessenger/HeaderQueue.h"
#include "rbc/Messenger/mqueueMessenger/ContentSegment.h"
#include "rbc/Messenger/Session.h"

#include "rbc/common/AsyncIO.h"
#include "rbc/common/ThreadPool.h"
#include "rbc/common/WorkQueue.h"
#include "rbc/common/Request.h"
#include "rbc/common/AioCompletion.h"

namespace rbc{
class MqueueSession: public Session{
public:
    int type;
    bool go;
    ThreadPool* listener;
    HeaderQueue* header_queue_in;
    HeaderQueue* header_queue_out;
    ContentSegment* content_segment;
    WorkQueue<void*>* request_queue;
    char in_queue_name[128];
    char out_queue_name[128];

    MqueueSession(uint32_t port = 0, WorkQueue<void*>* request_queue = NULL ):
        request_queue(request_queue), go(true){
        if( !port ){
            perror("No port specified\n");
            assert(0);
        }
        /* initialize the queue attributes */
        sprintf( in_queue_name, "/%u_in", port );
        sprintf( out_queue_name, "/%u_out", port );
        if(request_queue){
            content_segment = new ContentSegment( port, false );
            header_queue_in = new HeaderQueue( in_queue_name, O_CREAT | O_RDWR, content_segment, false );
            header_queue_out = new HeaderQueue( out_queue_name, O_CREAT | O_WRONLY, content_segment, false );
        }else{
        // client mode
            content_segment = new ContentSegment( port, true );
            header_queue_out = new HeaderQueue( in_queue_name, O_CREAT | O_WRONLY, content_segment, true );
            header_queue_in = new HeaderQueue( out_queue_name, O_CREAT | O_RDWR, content_segment, true );
        }
        listener = new ThreadPool(1);
        listener->schedule(boost::bind(&MqueueSession::start_listen, this));
    }
    ~MqueueSession(){
        go = false;
        header_queue_in->stop();
        header_queue_out->stop();
        delete listener;
    }

    void stop_service(){
        delete header_queue_out;
        delete header_queue_in;
        delete content_segment;
    }
    
    int start_listen(){
        while(go){
            receive_msg();
        }
        return 0;
    }

    void receive_msg(){
        Msg* msg = header_queue_in->receive_msg();
        //std::cout << "new msg" << std::endl;
        if(!msg){
            go = false;
            stop_service();
            return;
        }
        if(request_queue){
            async_io_unit *io_u = new async_io_unit( msg, (Messenger*)header_queue_out );
            Request *req = new Request( io_u->msg, REQ_MESSENGER, (void*)io_u );
            request_queue->enqueue((void*)req);
            //req->complete();
            //delete req;
        }else{
            //client mode
            ssize_t r;
            AsyncInflightIO_u *io_u = (AsyncInflightIO_u*)msg->header.seq_id;
            if( msg->header.type == MSG_REPLY_STAT ){
                r =msg->get_reserve();
            }else if( msg->header.type == MSG_REPLY_DATA ){
                r = msg->content_length();
                memcpy(io_u->msg->content, msg->content, msg->content_length());
            }
            AioCompletion* comp = (AioCompletion*)io_u->comp;
            comp->complete(r);

             /*release shm trunk and delete msg*/
            delete msg;
            content_segment->release_trunk( io_u->msg->get_reserve(), io_u->msg->content_length() );
            delete io_u->msg;
            delete io_u;
        }
    }
    
    int send_request( Msg* msg, void* arg = NULL ){
        AsyncInflightIO_u *io_u = new AsyncInflightIO_u( arg, msg );
        //std::cout << "create io_u:" << io_u << std::endl;
        return header_queue_out->send_request( msg, io_u );
    }
};

}
#endif
