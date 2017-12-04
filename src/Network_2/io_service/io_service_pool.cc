#include "io_service_pool.h"

namespace hdcs {
namespace networking {

IOServicePool::IOServicePool(std::size_t pool_size, 
        size_t pool_thread_num) 
    : _next_service(0)
{
    assert(pool_size > 0);

    for (size_t i = 0; i < pool_size; ++i)
    {
        ThreadGroupImplPtr service(new ThreadGroupImpl(
                pool_thread_num, "io_service worker thread"));
        _pool.push_back(service);
    }
}

bool IOServicePool::Run()
{
    size_t pool_size = _pool.size();
    for (size_t i = 0; i < pool_size; ++i)
    {
        if (!_pool[i]->start())
        {
            std::cout<<"Start(): start work thread group failed"<<std::endl;
            return false;
        }
    }
    return true;
}

void IOServicePool::Stop()
{
    size_t pool_size = _pool.size();
    for (size_t i = 0; i < pool_size; ++i)
    {
        _pool[i]->stop();
        _pool[i].reset();
    }
}

IOService& IOServicePool::GetIOService()
{
    IOService& io_service = _pool[_next_service]->io_service();
    ++_next_service;
    if (_next_service == _pool.size())
    {
        _next_service = 0;
    }
    return io_service;
}

} 
}
