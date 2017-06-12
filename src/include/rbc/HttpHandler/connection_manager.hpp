//
// connection_manager.hpp
// ~~~~~~~~~~~~~~~~~~~~~~
//
// Copyright (c) 2003-2013 Christopher M. Kohlhoff (chris at kohlhoff dot com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//

#ifndef HTTP_CONNECTION_MANAGER_HPP
#define HTTP_CONNECTION_MANAGER_HPP

#include <set>
#include "request.hpp"

namespace rbc {
namespace http {
namespace server {

class connection_manager;
class connection : public std::enable_shared_from_this<connection>{
public:
    connection(boost::asio::ip::tcp::socket socket,connection_manager& manager, request_handler& handler)
    : socket_(std::move(socket)),connection_manager_(manager),request_handler_(handler){}

    /// Start the first asynchronous operation for the connection.
    void start(){
        do_read();
    }

    /// Stop all asynchronous operations associated with the connection.
    void stop(){
        socket_.close();
    }

private:
    /// Perform an asynchronous read operation.
    void do_read();

    /// Perform an asynchronous write operation.
    void do_write();

    /// Socket for the connection.
    boost::asio::ip::tcp::socket socket_;
    /// The manager for this connection.
    connection_manager& connection_manager_;
    /// The handler used to process the incoming request.
    request_handler& request_handler_;
    /// Buffer for incoming data.
    std::array<char, 8192> buffer_;
    /// The incoming request.
    request request_;
    /// The parser for the incoming request.
    request_parser request_parser_;

    /// The reply to be sent back to the client.
    reply reply_;
};
/// Manages open connections so that they may be cleanly stopped when the server
/// needs to shut down.
typedef std::shared_ptr<connection> connection_ptr;
class connection_manager{
public:
    connection_manager(){}
    void start(connection_ptr c){
        connections_.insert(c);
        c->start();
    }
    void stop(connection_ptr c){
        connections_.erase(c);
        c->stop();
    }
    void stop_all(){
        for (auto c: connections_)
            c->stop();
        connections_.clear();
    }
private:
    std::set<connection_ptr> connections_;
};

void connection::do_read(){
    auto self(shared_from_this());
    socket_.async_read_some(boost::asio::buffer(buffer_),
    [this, self](boost::system::error_code ec, std::size_t bytes_transferred){
        if(!ec){
            request_parser::result_type result;
            std::tie(result, std::ignore) = request_parser_.parse(request_, buffer_.data(), buffer_.data() + bytes_transferred);

            if(result == request_parser::good){
                request_handler_.handle_request(request_, reply_);
                do_write();
            }else if (result == request_parser::bad){
                reply_ = reply::stock_reply(reply::bad_request);
                do_write();
            }else{
                do_read();
            }
        }else if (ec != boost::asio::error::operation_aborted){
          connection_manager_.stop(shared_from_this());
        }
    });
}

void connection::do_write(){
    auto self(shared_from_this());
    boost::asio::async_write(socket_, reply_.to_buffers(),
    [this, self](boost::system::error_code ec, std::size_t){
        if (!ec){
            // Initiate graceful connection closure.
            boost::system::error_code ignored_ec;
            socket_.shutdown(boost::asio::ip::tcp::socket::shutdown_both,ignored_ec);
        }

        if (ec != boost::asio::error::operation_aborted){
            connection_manager_.stop(shared_from_this());
        }
    });
}

} // namespace server
} // namespace http
}

#endif // HTTP_CONNECTION_MANAGER_HPP
