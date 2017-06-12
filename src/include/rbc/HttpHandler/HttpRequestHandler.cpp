#include "HttpRequestHandler.h"
#include "server.hpp"

namespace rbc{
HttpRequestHandler::HttpRequestHandler( Admin* admin ):admin(admin){
    listener->schedule( boost::bind(&HttpRequestHandler::start, this) );
}

HttpRequestHandler::~HttpRequestHandler(){
    std::cout << "delete server" << std::endl;
    http::server::server* s = (http::server::server*)server;
    s->stop();
    delete listener;
}

void HttpRequestHandler::start(){
    try{
        // Initialise the server.
        http::server::server s("0.0.0.0","80",admin);
        // Run the server until stopped.
        server = &s;
        s.run();
    }catch (std::exception& e){
        std::cerr << "exception: " << e.what() << "\n";
    }
}
}
