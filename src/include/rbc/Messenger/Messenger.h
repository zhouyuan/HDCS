#ifndef RBC_MESSENGER_H
#define RBC_MESSENGER_H
#include "rbc/Message.h"

namespace rbc{
class Messenger{
public:
    virtual int send_request( Msg *msg, void* arg = NULL ) = 0;
};
}

#endif
