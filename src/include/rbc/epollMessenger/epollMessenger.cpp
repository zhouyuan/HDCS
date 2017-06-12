#include "Messenger.h"

namespace rbc{
Messenger::Messenger( const char* port, WorkQueue<void*> *request_queue ):port(port),request_queue(request_queue){
    int ret;
    sfd = create_socket(port);
    assert( sfd != -1 );

    ret = make_socket_non_blocking( sfd );
    assert( ret == 0 );

    ret = listen( sfd, SOMAXCONN );
    assert( ret == 0 );

    ret = prepare_epoll();
    assert( ret != -1 );

    ret = add_to_epoll( sfd );
    assert( ret == 0 );

    go = true;
    listener = new ThreadPool(1);
    listener->schedule(boost::bind(&Messenger::start_listen, this));
}

Messenger::~Messenger(){
  go = false;
  free(events);
  close(sfd);
  delete listener;
}

int Messenger::accept_connection(int* infd){
    struct sockaddr in_addr;
    socklen_t in_len;
    char hbuf[NI_MAXHOST], sbuf[NI_MAXSERV];

    int ret;
    in_len = sizeof(in_addr);
    *infd = accept(sfd, &in_addr, &in_len);
    if(*infd == -1){
        if((errno == EAGAIN) ||
           (errno == EWOULDBLOCK)){
            /* We have processed all incoming
               connections. */
            return -2;
        }else{
            perror ("accept connection failed");
            return -1;
        }
    }

    /*ret = getnameinfo(&in_addr, in_len,
                    hbuf, sizeof hbuf,
                    sbuf, sizeof sbuf,
                    NI_NUMERICHOST | NI_NUMERICSERV);
    */
    return 0;
}

 int Messenger::add_to_epoll(int fd){
     int ret;
     event.data.fd = fd;
     event.events = EPOLLIN | EPOLLET;
     ret = epoll_ctl( efd, EPOLL_CTL_ADD, fd, &event );
     if( ret == -1 ){
         perror ("epoll_ctl failed");
         return -1;
     }
     return 0;
}

int Messenger::create_socket(const char *port){
    struct addrinfo hints;
    struct addrinfo *result, *rp;
    int s, sfd;

    memset(&hints, 0, sizeof (struct addrinfo));
    hints.ai_family = AF_UNSPEC;     /* Return IPv4 and IPv6 choices */
    hints.ai_socktype = SOCK_STREAM; /* We want a TCP socket */
    hints.ai_flags = AI_PASSIVE;     /* All interfaces */

    s = getaddrinfo(NULL, port, &hints, &result);
    if(s != 0){
        fprintf (stderr, "getaddrinfo: %s\n", gai_strerror (s));
        return -1;
    }

    for(rp = result; rp != NULL; rp = rp->ai_next){
        //set server info at cct
        sfd = socket(rp->ai_family, rp->ai_socktype, rp->ai_protocol);
        if (sfd == -1)
            continue;

        s = bind(sfd, rp->ai_addr, rp->ai_addrlen);
        if(s == 0){
            /* We managed to bind successfully! */
            break;
        close(sfd);
        }
    }

    if(rp == NULL){
        fprintf (stderr, "Could not bind\n");
        return -1;
    }

    freeaddrinfo (result);
    return sfd;
}

 int Messenger::start_listen(){
    int ret;
    /* The event loop */
    while (go){
        uint64_t received_req_count;

        //std::cout << "epoll wait start" << std::endl;
        received_req_count = epoll_wait(efd, events, MAXEVENTS, -1);
        //std::cout << "epoll wait stop" << std::endl;
        if( received_req_count <= 0 ){
            continue;
        }
        for(int i = 0; i < received_req_count; i++){
            if ((events[i].events & EPOLLERR) ||
                (events[i].events & EPOLLHUP) ||
                !(events[i].events & EPOLLIN)){
                /* An error has occured on this fd, or the socket is not
                   ready for reading (why were we notified then?) */
                int error = 0;
                socklen_t errlen = sizeof(error);
                if (getsockopt(events[i].data.fd, SOL_SOCKET, SO_ERROR, (void *)&error, &errlen) == 0)
                    printf ("epoll error = %s\n",strerror(error));
                else
                    printf ("epoll error, unknown reason\n");
                close (events[i].data.fd);
                continue;
            }else if(sfd == events[i].data.fd){
                /* We have a notification on the listening socket, which
                 means one or more incoming connections. */
                while (1){
                   int infd;
                   ret = accept_connection(&infd);
                   if( ret != 0 )
                       break;
                   if( ret == 0 )
                   /* Make the incoming socket non-blocking and add it to the
                      list of fds to monitor. */
                   ret = make_socket_non_blocking( infd );
                   if( ret != 0 )
                       return -1;
                    
                   int one = 1;
                   setsockopt(infd, SOL_TCP, TCP_NODELAY, &one, sizeof(one));
                   ret = add_to_epoll( infd );
                   if( ret != 0 )
                       return -1;
                   //std::cout << "receive socket fd" << infd  << std::endl;
                }
                continue;
            }else{
                int ret = 0;
                do{
                    ret = receive_msg( events[i].data.fd );
                }while( ret == 0 );
            }
        }
    }
}

void Messenger::receive_content( int socket_, char* data, ssize_t bytes_to_recv ){
    ssize_t exact_bytes_received = 0;
    ssize_t left = bytes_to_recv;
    ssize_t offset = 0;
    while( left ){
        exact_bytes_received = recv(socket_, &data[offset], left, 0);
        left -= exact_bytes_received;
        offset += exact_bytes_received;
    }
}

int Messenger::receive_msg( int socket_ ){
    char msg_header[MSG_HEADER_LEN];
    ssize_t exact_bytes_received = recv(socket_, msg_header, MSG_HEADER_LEN, MSG_DONTWAIT);
    if(exact_bytes_received <= 0){
        return -1;
    }
    std::string data(msg_header, MSG_HEADER_LEN);
    Msg *msg = new Msg(data);
    
    char* content_data = new char[ msg->length() ];
    receive_content( socket_, content_data, msg->length() );
    msg->set_content( content_data );
    delete[] content_data;

    async_io_unit *io_u = new async_io_unit( socket_, msg );
    Request *req = new Request( io_u->msg, REQ_MESSENGER, (void*)io_u );
    request_queue->enqueue((void*)req);
    /*req->complete();
    delete req;*/
    return 0;
}

int Messenger::prepare_epoll(){
    int ret;
    efd = epoll_create1(0);
    /* Buffer where events are returned */
    events = (epoll_event*)calloc(MAXEVENTS, sizeof(event));
    return efd;
}


 int Messenger::make_socket_non_blocking(int fd){
    int flags, s;

    flags = fcntl(fd, F_GETFL, 0);
    if(flags == -1){
        perror( "fcntl Get Flags Failed" );
        return -1;
    }

    flags |= O_NONBLOCK;
    s = fcntl (fd, F_SETFL, flags);
    if (s == -1){
        perror ("fcntl set flags Failed");
        return -1;
    }

    return 0;
}
}
