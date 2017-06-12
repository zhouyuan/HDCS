#ifndef MESSENGERSENDER
#define MESSENGERSENDER
#include "rbc/common/AsyncIO.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/epoll.h>
#include <errno.h>
namespace rbc{
class MessengerSender{
public:
    MessengerSender( int socket_ ):socket_(socket_){
    }

    
    void start_send( std::string data_ ){
        start_send( data_.c_str(), data_.length() );
    }
    
    void start_send( const char* data_, ssize_t length ){
            ssize_t offset = 0;
            ssize_t exact_send_bytes = 0;
            ssize_t left = length - offset;
    
            while( left ){
                try{
                    exact_send_bytes = send( socket_, &data_[offset], left, 0 );
                }catch (std::exception& e){
                    std::cout << "Client probably is down, Exception: " << e.what() << "\n";
                    return;
                }
                left -= exact_send_bytes;
                offset += exact_send_bytes;
            }
    }
private:
    int socket_;
};
}
#endif
