#ifndef HEADERQUEUE_H
#define HEADERQUEUE_H

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <errno.h>
#include <mqueue.h>
#define HEADER_SIZE 97
#define MQUEUE_STOP "Exit"
#include "rbc/Message.h"
#include "rbc/Messenger/Messenger.h"
#include "rbc/Messenger/mqueueMessenger/ContentSegment.h"
#include "rbc/common/FailoverHandler.h"

namespace rbc{
class HeaderQueue: public Messenger{
public:
    struct mq_attr attr;
    mqd_t mq_id = -1;
    char* mqueue_name;
    bool init;
    ContentSegment *content_segment;

    HeaderQueue( char* mqueue, int type, void* content_segment, bool init = false):
        mqueue_name(mqueue),init(init),content_segment((ContentSegment*)content_segment){
        /* initialize the queue attributes */
        //std::cout << "mqueue name: " << mqueue << std::endl;
        attr.mq_flags = 0;
        attr.mq_maxmsg = 128;
        attr.mq_msgsize = HEADER_SIZE;
        attr.mq_curmsgs = 0;
        mq_id = mq_open(mqueue, type, 0666,  &attr);
        if( mq_id == -1 ){
            fprintf( stdout, "Open MSG QUEUE %s failed, error no: %s\n", mqueue, strerror(errno) );
            failover_handler(MQ_OPEN, NULL);
        }
    }

    ~HeaderQueue(){
        if(init){
            int ret = mq_close(mq_id);
            if( ret != 0 ){
		failover_handler(MQ_CLOSE,NULL);
                fprintf( stdout, "Close MSG QUEUE ID %d failed, error no: %s\n", mq_id, strerror(errno) );
            }
            ret = mq_unlink(mqueue_name);
            if( ret != 0 ){
		failover_handler(MQ_UNLINK,NULL);
                fprintf( stdout, "Remove MSG QUEUE %s failed, error no: %s\n", mqueue_name, strerror(errno) );
            }
        }
    }

    Msg* receive_msg(){
        char* msg_header = new char[HEADER_SIZE+1]();
        ssize_t exact_bytes_received;
        exact_bytes_received = mq_receive(mq_id, msg_header, HEADER_SIZE, NULL);

        if(exact_bytes_received == -1){
            fprintf( stdout, "MSG QUEUE %s RECEIVE failed, error no: %s\n", mqueue_name, strerror(errno) );
            failover_handler(MQ_RECEIVE,NULL);
            return NULL;
        }
        if( strcmp( msg_header, MQUEUE_STOP) == 0 ){
            return NULL;
        }
        std::string data(msg_header, HEADER_SIZE);
        Msg *msg = new Msg(data, content_segment->get_shm_ptr());
        //std::cout << "location_id:" << msg->location_id << std::endl;

        delete[] msg_header;

        return msg;
    }

    int send_request( Msg* msg, void* arg = NULL ){
        uint64_t shm_content_offset = 0;
        int ret = 0;
        if(msg->header.type == MSG_REPLY_STAT || msg->header.type == MSG_REPLY_DATA ){
            ret = start_send( msg->toString_shm() );
        }else if(msg->header.type == MSG_WRITE || msg->header.type == MSG_READ){
            shm_content_offset = content_segment->get_free_trunk_offset( msg->content_length() );
            if( shm_content_offset == -1 ){
                std::cout << "can't find free chunk in shm" << std::endl;
                assert(0);
            }
            msg->set_reserve(shm_content_offset);
            char* content_ptr = content_segment->get_shm_ptr() + shm_content_offset;
            if(msg->header.type == MSG_WRITE){
                msg->cp_content_to_shm( content_ptr );
            }
            if( arg != NULL ) msg->set_callback( arg );
            ret = start_send( msg->toString_shm() );
        }
        return ret;
    }

    int start_send(const char* data, ssize_t length){
        //std::cout << "start_send: " << length << "bytes" << std::endl;
        int ret = mq_send( mq_id, data, length, 0 );   //
        if( ret == -1 ){
            fprintf( stdout, "MSG QUEUE %s SEND failed, error no: %s\n", mqueue_name, strerror(errno) );
            failover_handler(MQ_SEND,NULL);
            return -1;
        }
        return 0;
    }

    int start_send(std::string data){
        return start_send( data.c_str(), data.length() );
    }

    void stop(){
        mq_send( mq_id, MQUEUE_STOP, strlen(MQUEUE_STOP), 0 );
    }
};
}
#endif
