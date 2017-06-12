#ifndef RBC_MQUEUECLIENT_H
#define RBC_MQUEUECLIENT_H

#include "MqueueSession.h"

namespace rbc{
class MqueueClient{
public:
    MqueueSession* session;
    MqueueClient(){
        session = new MqueueSession(); 
    }
    ~MqueueClient(){
        delete session;
    }
    int send_request( Msg* msg, void* arg ){
        return session->send_request( msg, arg );
    }
};
}
#endif
