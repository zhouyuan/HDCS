#ifndef MESSENGER_H
#define MESSENGER_H
#include <netinet/tcp.h>
#include <sys/socket.h>
#include "rbc/Message.h"
#include "rbc/common/ThreadPool.h"
#include "rbc/common/AioCompletion.h"
#include <arpa/inet.h>
#include <string.h>
#include <mutex>
#include <condition_variable>
#include <boost/unordered_map.hpp>

namespace rbc{
class AsyncInflightIO_u{
public:
    void* comp;
    Msg *msg;
    bool completed;
    std::mutex aio_lock;
    std::mutex llock;
    std::condition_variable m_cond;
    std::unique_lock<std::mutex> slock;
    AsyncInflightIO_u(void *comp, Msg* msg):comp(comp),msg(msg),slock(aio_lock), completed(false){}
    void set_complete(){
        std::unique_lock<std::mutex> ul(llock);
        completed = true;
        //m_cond.notify_all();
    }
    bool check_complete(){
        std::unique_lock<std::mutex> ul(llock);
        return completed?true:false;
    }
};
typedef boost::unordered::unordered_map<uint64_t,void*> CallbackMap;

class MessengerClient{
private:
    bool go;
    int sfd;
    CallbackMap call_map;
    uint64_t cur_seq;
    std::mutex data_lock;
    int create_client_socket(const char* addr, const char* port);
    char msg_header[MSG_HEADER_LEN];
    ThreadPool *listener;
public:
    MessengerClient(const char* addr, const char* port);
    ~MessengerClient();
    int send_request(Msg* msg, void* arg);
    void receive_content( int socket_, char* data, ssize_t bytes_to_recv );
    void receive_msg( int socket_ );
    void start_listen( int socket_ );
    void handle_io( Msg *msg );
    void handle_io( AsyncInflightIO_u *io_u, Msg* msg = NULL );
};
}
#endif
