#ifndef C_AIOCLIENTCOMPLETION_H
#define C_AIOCLIENTCOMPLETION_H

namespace rbc{

class C_AioClientCompletion : public AioCompletion{
private:
    callback_t complete_cb;
    void *complete_arg;

public:
    C_AioClientCompletion( void *cb_arg, callback_t cb ):complete_arg(cb_arg),complete_cb(cb){
        type = COMP_CLIENT;
        assert(complete_cb != NULL);
        assert(complete_arg != NULL);
    }
    ~C_AioClientCompletion(){
    }

    void complete(ssize_t r){
        //printf("C_AioClientCompletion\n");
        if (complete_cb) {
            complete_cb(r, complete_arg);
        }
    }

    std::string get_type(){
        std::string type("C_AioClientCompletion");
        return type;
    }

};

}
#endif
