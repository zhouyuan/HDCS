#ifndef IO_SERVICE_POOL_H_
#define IO_SERVICE_POOL_H_

#include <vector>

#include "thread_group_impl.h"

namespace hdcs {
namespace networking {

class IOServicePool
{
public:
    IOServicePool(std::size_t pool_size, std::size_t pool_thread_num);

    bool Run();

    void Stop();

    IOService& GetIOService();

    void set_init_func(ThreadInitFunc init_func)
    {
        _init_func = init_func;
    }

    void set_dest_func(ThreadDestFunc dest_func)
    {
        _dest_func = dest_func;
    }

private:

    std::vector<ThreadGroupImplPtr> _pool;

};

} 
} 

#endif 
