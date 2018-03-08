#ifndef THREAD_GROUP_H_
#define THREAD_GROUP_H_

#include <boost/bind.hpp>

#include "thread_group_impl.h"

namespace hdcs {
namespace networking {

class ThreadGroup{
public:
    ThreadGroup(int thread_num)
    {
        _imp.reset(new ThreadGroupImpl(thread_num));
        _imp->start();
    }

    ~ThreadGroup()
    {
        _imp->stop();
        _imp.reset();
    }

    // Get the number of threads in this thread group.
    int thread_num() const
    {
        return _imp->thread_num();
    }

    // Request the thread group to invoke the given handler.
    // and block here.
    template< typename _callback>
    void dispatch(_callback handler)
    {
        _imp->dispatch(handler);
    }

    // Request the thread group to invoke the given handler and return immediately.
    template< typename _callback>
    void post(_callback handler)
    {
        _imp->post(handler);
    }

private:
    std::shared_ptr<ThreadGroupImpl> _imp;

};

}
} 

#endif
