#include "MessengerClient.h"
namespace rbc{

MessengerClient::MessengerClient(const char* addr, const char* port){
    go = true;
    listener = new ThreadPool(1);
    int ret;
    sfd = create_client_socket(addr, port);
    assert( sfd != -1 );
    listener->schedule(boost::bind(&MessengerClient::start_listen, this, sfd));
    std::cout << "MessengerClient constructed" << std::endl;
}

MessengerClient::~MessengerClient(){
    std::cout << "MessengerClient destruction start" << std::endl;
    go = false;
    close(sfd);
    std::cout << "start to delete listener" << std::endl;
    delete listener;
    std::cout << "MessengerClient destruction done" << std::endl;
}

int MessengerClient::create_client_socket(const char*addr, const char* port){
    struct sockaddr_in server;
    int s, sfd;

    server.sin_addr.s_addr = inet_addr(addr);
    server.sin_family = AF_INET;
    server.sin_port = htons(atoi(port));

    //set server info at cct
    sfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sfd == -1)
        perror("Create Socket");

    int one = 1;
    setsockopt(sfd, SOL_TCP, TCP_NODELAY, &one, sizeof(one));
    s = connect( sfd, (struct sockaddr *)&server , sizeof(server) );
    if( s != 0 ){
        perror("Connect failed");
    }

    return sfd;
}

int MessengerClient::send_request( Msg* msg, void* arg ){
    uint64_t seq_id;
    AsyncInflightIO_u *io_u = new AsyncInflightIO_u(arg, msg);
    data_lock.lock();
    seq_id = cur_seq++;
    //AioCompletion *comp = (AioCompletion*)arg;
    //std::cout << "comp type: " << comp->get_type() << std::endl;
    std::pair<CallbackMap::iterator, bool> ret = call_map.insert(std::make_pair(seq_id, (void*)io_u));
    data_lock.unlock();
    assert( ret.second );
    msg->set_seq_id(seq_id);
    std::string msg_str = msg->toString();

    const char* msg_str_ptr = msg_str.c_str();
    ssize_t offset = 0;
    ssize_t exact_send_bytes = 0;
    ssize_t left = msg_str.length() - offset;

    while( left ){
        exact_send_bytes = send( sfd, &msg_str_ptr[offset], left, MSG_CONFIRM );
        if( !exact_send_bytes ){
            std::cerr << "MessengerClient::send_request failed" << std::endl;
            return -1;
        }
        left -= exact_send_bytes;
        offset += exact_send_bytes;
    }
    //deadline_watcher->schedule(boost::bind(&MessengerClient::timed_aio_wait, this, io_u, ret.first));
}

void MessengerClient::receive_content( int socket_, char* data, ssize_t bytes_to_recv ){
    ssize_t exact_bytes_received = 0;
    ssize_t left = bytes_to_recv;
    ssize_t offset = 0;
    while( left ){
        exact_bytes_received = recv(socket_, &data[offset], left, 0);
        left -= exact_bytes_received;
        offset += exact_bytes_received;
    }
}

void MessengerClient::receive_msg( int socket_ ){
    char msg_header[MSG_HEADER_LEN];
    ssize_t exact_bytes_received = recv(socket_, msg_header, MSG_HEADER_LEN, MSG_DONTWAIT);
    if( exact_bytes_received <= 0 )
        return;
    std::string data(msg_header, MSG_HEADER_LEN);
    Msg *msg = new Msg(data);
    
    char* content_data = new char[ msg->length() ];
    receive_content( sfd, content_data, msg->length() );
    msg->set_content( content_data );
    //std::cout << exact_bytes_received << " bytes received, content data: " << content_data << std::endl;
    delete[] content_data;
    handle_io(msg);
}

void MessengerClient::handle_io( AsyncInflightIO_u *io_u, Msg* msg ){
    ssize_t r;
    if(msg){
        if( msg->header.type == MSG_REPLY_STAT ){
            r = *(ssize_t*)msg->content;
        }else if( msg->header.type == MSG_REPLY_DATA ){
            r = msg->header.length;
            memcpy(io_u->msg->content, msg->content, msg->header.length);
        }
    }else{
        r = 0 - ETIME;
    }
    //std::cout << "call complete, r: " << r << std::endl;
    AioCompletion* comp = (AioCompletion*)io_u->comp;
    comp->complete(r);
    io_u->set_complete();
    if(msg)
        delete msg;
}

void MessengerClient::handle_io( Msg *msg ){
    uint64_t seq_id = msg->header.seq_id;
    data_lock.lock();
    const typename CallbackMap::iterator it = call_map.find(seq_id);
    if( it == call_map.end() ){
        data_lock.unlock();
        assert(false);
    }
    AsyncInflightIO_u* io_u = (AsyncInflightIO_u*)(it->second);
    call_map.erase(it);
    data_lock.unlock();
    Msg *orig_msg = io_u->msg;
    handle_io( io_u, msg );
    //io_u->m_cond.notify_all();
    //delete io_u;
}

/*void MessengerClient::start_listen( const char* port ){
    uint16_t listen_port = stoi(port) + 1;
    std::string listen_port_str(listen_port);
    int fd = create_socket( listen_port.c_str() );
    int ret = listen( fd, SOMAXCONN );
    start_listen( fd ); 
    
}*/

void MessengerClient::start_listen( int socket_ ){
    while(go){
        receive_msg( socket_ );
    }
}
}
