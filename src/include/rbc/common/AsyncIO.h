#ifndef ASYNCIO_H
#define ASYNCIO_H
#include <cstdlib>
#include <iostream>
//#include <boost/bind.hpp>
//#include <boost/asio.hpp>
#include "rbc/Message.h"
#include "rbc/Messenger/Messenger.h"
namespace rbc{
//using boost::asio::ip::tcp;
struct async_io_unit{
    Messenger* msg_session;
    Msg *msg;
    async_io_unit( Msg* src_msg, Messenger* msg_session ):
        msg_session(msg_session){
            msg = src_msg;
    }
    ~async_io_unit(){
    }

    int reply_request(Msg* reply_msg){
        return msg_session->send_request(reply_msg);
    }
};
}
#endif
