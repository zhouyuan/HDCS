#ifndef AIOCOMPLETION_H
#define AIOCOMPLETION_H

#define COMP_CLIENT  0x0001
#define COMP_REPLICA 0x0002

namespace rbc{

typedef void *completion_t;
typedef void (*callback_t)(int r, void *arg);

class AioCompletion{
public:
    AioCompletion():type(0){
    }
    ~AioCompletion(){
    }
    virtual void complete(ssize_t r) = 0;
    virtual std::string get_type() = 0;
    uint64_t type; 

};

}
#endif
