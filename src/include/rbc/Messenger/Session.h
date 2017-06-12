#ifndef RBC_SESSION_H
#define RBC_SESSION_H

namespace rbc{
class AsyncInflightIO_u{
public:
    void* comp;
    Msg* msg;
    AsyncInflightIO_u(void* comp, Msg* msg):comp(comp), msg(msg){}
};
class Session{

};
}

#endif
