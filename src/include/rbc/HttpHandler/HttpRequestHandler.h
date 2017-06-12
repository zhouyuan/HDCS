#ifndef HTTPREQUESTHANDLER_H
#define HTTPREQUESTHANDLER_H

#include <iostream>
#include <string>
#include <boost/asio.hpp>
#include <boost/bind.hpp>
#include "rbc/common/ThreadPool.h"
#include "rbc/common/Admin.h"

namespace rbc{
class HttpRequestHandler{
 
public:
    HttpRequestHandler( Admin* admin );

    ~HttpRequestHandler();

    void start();
private:
    ThreadPool *listener = new ThreadPool(1);
    Admin* admin;
    void* server;
};
}
#endif
