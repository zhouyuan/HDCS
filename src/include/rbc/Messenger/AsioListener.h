#ifndef RBC_ASIO_LISTENER_H
#define ASIO_LISTENER_H

#define MAX_SESSION_NUM 32
#include <boost/asio.hpp>
#include <boost/bind.hpp>
#include "rbc/common/WorkQueue.h"
#include "rbc/common/ThreadPool.h"
#include "rbc/Messenger/mqueueMessenger/MqueueSession.h"
#include "rbc/Messenger/asioMessenger/AsioSession.h"
#include "rbc/common/FailoverHandler.h"

namespace rbc{
using boost::asio::ip::tcp;
class AsioListener{
private:
    short port;
    ThreadPool *listener = new ThreadPool(1);
    tcp::acceptor* acceptor_ptr;
    boost::asio::io_service io_service;
    std::vector<Session*> session_vector;
    WorkQueue<void*>* request_queue;
    tcp::socket* accepted_socket;

public:
    AsioListener( short port, WorkQueue<void*>* request_queue ):port(port), request_queue(request_queue){
        listener->schedule( boost::bind(&AsioListener::start_listen, this) );
    }

    ~AsioListener(){
        for(std::vector<Session*>::iterator it = session_vector.begin(); it != session_vector.end(); it++){
            delete *it;
        }
        acceptor_ptr->close();
        io_service.stop();
        delete acceptor_ptr;
        delete listener;
    }

    void start_listen(){
        acceptor_ptr = new tcp::acceptor(io_service, tcp::endpoint(tcp::v4(), port));
        acceptor_ptr->listen(MAX_SESSION_NUM);
        start_accept();
        io_service.run();
    }

    void start_accept(){
        accepted_socket = new tcp::socket(io_service);
        acceptor_ptr->async_accept(
            *accepted_socket,
            boost::bind(
                &AsioListener::handle_accept,
                this,
                boost::asio::placeholders::error
            )
        );
    }

    void handle_accept(const boost::system::error_code& error){
        log_print("AsioListener::handle_accept got new connection\n");;
        if (!error){
            /* check the source, if local, using shm, remote using asio*/
            std::string source_ip = accepted_socket->remote_endpoint().address().to_string();
            uint32_t source_port = accepted_socket->remote_endpoint().port();
            if( source_ip == "127.0.0.1" ){
                //std::cout << "source ip is: " << source_ip << ", port is:" << source_port << std::endl;
                MqueueSession* new_session = new MqueueSession( source_port, request_queue );
                session_vector.push_back( (Session*)new_session );
                accepted_socket->close();    
            }else{
                AsioSession* new_session = new AsioSession( io_service, accepted_socket, request_queue );
                session_vector.push_back( (Session*)new_session );
            }

            start_accept();
        }else{
	    failover_handler(ASIO_SOCKET_CONNECTION,NULL);
            log_print("AsioListener::handle_accept failed to accept new connection\n");;
        }
    }

};
}
#endif
