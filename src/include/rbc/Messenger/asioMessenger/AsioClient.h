#ifndef RBC_ASIOCLIENT_H
#define RBC_ASIOCLIENT_H

#include "rbc/Messenger/asioMessenger/AsioSession.h"
#include "rbc/Messenger/mqueueMessenger/MqueueSession.h"

namespace rbc{
class AsioClient{
public:
    AsioSession* asio_session;
    MqueueSession* mqueue_session;
    boost::asio::io_service io_service;
    ThreadPool *listener;
    AsioClient(std::string dest_ip, std::string port):asio_session(NULL),mqueue_session(NULL),listener(NULL){
        asio_session = new AsioSession(io_service, NULL, NULL, dest_ip.c_str(), port.c_str()); 
        if( dest_ip == "127.0.0.1" ){
            mqueue_session = new MqueueSession( asio_session->get_local_port() );
        }else{
            listener = new ThreadPool(1);
            listener->schedule( boost::bind(&AsioClient::start_listen, this) );
        }
    }
    ~AsioClient(){
        if(asio_session){
            io_service.stop();
            delete asio_session;
            delete listener;
        }
        if(mqueue_session) delete mqueue_session;
    }
    int send_request( Msg* msg, void* arg ){
        if(mqueue_session)
            return mqueue_session->send_request( msg, arg );
        if(asio_session)
            return asio_session->send_request( msg, arg );
    }
    void start_listen(){
        asio_session->start_listen();
        io_service.run();
    }
};
}
#endif
