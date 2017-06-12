//
// server.hpp
// ~~~~~~~~~~
//
// Copyright (c) 2003-2013 Christopher M. Kohlhoff (chris at kohlhoff dot com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//

#ifndef HTTP_SERVER_HPP
#define HTTP_SERVER_HPP

#include <boost/asio.hpp>
#include <string>
#include <signal.h>
#include <utility>
#include "connection_manager.hpp"

namespace rbc {
namespace http {
namespace server {

/// The top-level class of the HTTP server.
class server
{
public:
    server(const char* address_char, const char* port_char, Admin* admin):
        io_service_(),
        signals_(io_service_),
        acceptor_(io_service_),
        connection_manager_(),
        socket_(io_service_),
        request_handler_(admin){
            std::string address(address_char);
            std::string port(port_char);
  
            boost::asio::ip::tcp::resolver resolver(io_service_);
            boost::asio::ip::tcp::endpoint endpoint = *resolver.resolve({address, port});
            acceptor_.open(endpoint.protocol());
            acceptor_.set_option(boost::asio::ip::tcp::acceptor::reuse_address(true));
            acceptor_.bind(endpoint);
            acceptor_.listen();
  
            do_accept();
    }

    ~server(){
        acceptor_.close();
        connection_manager_.stop_all();
    }
  /// Run the server's io_service loop.
    void run(){
        io_service_.run();
    }

    void stop(){
        io_service_.stop();
    }

private:
  /// Perform an asynchronous accept operation.
  void do_accept(){
      acceptor_.async_accept(socket_,[this](boost::system::error_code ec){
          // Check whether the server was stopped by a signal before this
          // completion handler had a chance to run.
          if (!acceptor_.is_open())
          {
            return;
          }
  
          if (!ec)
          {
            connection_manager_.start(std::make_shared<connection>(
                std::move(socket_), connection_manager_, request_handler_));
          }
  
          do_accept();
      });
  }

  /// Wait for a request to stop the server.
  boost::asio::io_service io_service_;
  boost::asio::signal_set signals_;
  boost::asio::ip::tcp::acceptor acceptor_;
  connection_manager connection_manager_;
  boost::asio::ip::tcp::socket socket_;
  request_handler request_handler_;
};

} // namespace server
} // namespace http
}

#endif // HTTP_SERVER_HPP
