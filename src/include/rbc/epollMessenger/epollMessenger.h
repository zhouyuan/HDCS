#ifndef MESSENGER_H
#define MESSENGER_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <netinet/tcp.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/epoll.h>
#include <errno.h>
#include "rbc/Message.h"
#include "rbc/common/Request.h"
#include "rbc/common/WorkQueue.h"
#include "rbc/common/AsyncIO.h"
#include "rbc/common/ThreadPool.h"
#define MAXEVENTS 64
namespace rbc{
class Messenger{
public:
    Messenger( const char* port, WorkQueue<void*> *request_queue );
    ~Messenger();
    int start_listen();
private:
    int accept_connection(int* infd);
    int add_to_epoll(int fd);
    int prepare_epoll();
    int make_socket_non_blocking(int fd);
    int create_socket(const char *port);
    void receive_content( int socket_, char* data, ssize_t bytes_to_recv );
    int receive_msg( int socket_ );

    int sfd, efd;
    struct epoll_event event;
    struct epoll_event *events;
    const char* port;
    WorkQueue<void*>* request_queue;
    bool go;
    ThreadPool* listener;
};
}
#endif
