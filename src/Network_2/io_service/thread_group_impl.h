#ifndef _SOFA_PBRPC_THREAD_GROUP_IMPL_H_
#define _SOFA_PBRPC_THREAD_GROUP_IMPL_H_

#include <unistd.h>
#include <pthread.h>
#include <cstdio>
#include <atomic>
#include <memory>

#include <boost/bind.hpp>
#include <boost/asio.hpp>

#include "../common/networking_common.h"

namespace hdcs {
namespace networking {

// Defined in this file.
class ThreadGroupImpl;
//typedef hdcs::networking::shared_ptr<ThreadGroupImpl> ThreadGroupImplPtr;

class ThreadGroupImpl{
public:
    // baidu have this class implement.
    typedef std::atomic<int> AtomicCounter;

    struct ThreadParam{
        int id; // sequence id in the thread group, starting from 0
        IOService* io_service;
        AtomicCounter init_done;
        AtomicCounter init_fail;
        ThreadParam() : id(0), io_service(NULL){}
        ~ThreadParam() {}
    }; 

public:
    ThreadGroupImpl(int thread_num, const std::string& name = "")
        : _is_running(false)
        , _thread_num(std::max(thread_num, 1))
        , _name(name)
        , _io_service_work(NULL)
        , _threads(NULL)
        , _thread_params(NULL){
        if (_name.empty()){
            char tmp[20];
            sprintf(tmp, "%p", this);
            _name = tmp;
        }
    }

    ~ThreadGroupImpl(){
        stop();
    }

    int thread_num() const{
        return _thread_num;
    }

    std::string name() const{
        return _name;
    }

    IOService& io_service(){
        return _io_service;
    }

    bool start()
    {
        if (_is_running){
            return true;
        }
        _is_running = true;
        _io_service_work = new IOServiceWork(_io_service);
        _threads = new pthread_t[_thread_num];
        _thread_params = new ThreadParam[_thread_num];
        for (int i = 0; i < _thread_num; ++i)
        {
            _thread_params[i].id = i;
            _thread_params[i].io_service = &_io_service;
            int ret = pthread_create(&_threads[i], NULL, &ThreadGroupImpl::thread_run, &_thread_params[i]);
            if (ret != 0)
            {
                std::cout<<"ThreadGroupImp::start(): failed."<<std::endl;
                _thread_num = i;
                stop();
                return false;
            }
        }
        // wait for all threads successfully create. 
        bool init_fail = false;
       /*
        while (true){
            int done_num = 0;
            for (int i = 0; i < _thread_num; ++i){
                if (_thread_params[i].init_done == 1){
                    if (_thread_params[i].init_fail == 1){
                        init_fail = true;
                        break;
                    }else{
                        ++done_num;
                    }
                }
            }
            if (init_fail || done_num == _thread_num){
                break;
            }
            //wait for some times, then check every thread.
           // usleep(100000);
           assert(0);
        }
        */
        if (init_fail){
            std::cout<<"ThreadGroupImpl::start: start thread group failed."<<std::endl;
            stop();
            return false;
        }
        return true;
    }

    void stop(){
        if (!_is_running){
            return;
        }
        _is_running = false;

        delete _io_service_work;
        _io_service_work = NULL;

        for (int i = 0; i < _thread_num; ++i){
            int ret = pthread_join(_threads[i], NULL);
            if (ret != 0){
                std::cout<<"ThreadGroupImp::stop(): join thread failed."<<std::endl;
            }
        }
        delete []_thread_params;
        _thread_params = NULL;
        delete []_threads;
        _threads = NULL;
    }

    // Request the thread group to invoke the given handler.
    // The handler may be executed inside this function if the guarantee can be met.
    // The function signature of the handler must be:
    //   void handler();
    template< typename CompletionHandler >
    void dispatch(CompletionHandler handler){
        _io_service.dispatch(handler);
    }

    // Request the thread group to invoke the given handler and return immediately.
    // It guarantees that the handle will not be called from inside this function.
    // The function signature of the handler must be:
    //   void handler();
    template< typename CompletionHandler >
    void post(CompletionHandler handler){
        _io_service.post(handler);
    }

private:
    static void* thread_run(void* param){
        ThreadParam* thread_param = reinterpret_cast<ThreadParam*>(param);
        // to do some init things;
        ++thread_param->init_done;
        // run asio
        if (thread_param->init_fail == 0){
            thread_param->io_service->run();
        }
        return NULL;
    }

private:
    volatile bool _is_running;
    int _thread_num;
    std::string _name;

    IOService _io_service;   // just one io service.
    IOServiceWork* _io_service_work;
    pthread_t* _threads; // thread vector.
    ThreadParam* _thread_params;
};

} 
} 

#endif 
