//
// request.hpp
// ~~~~~~~~~~~
//
// Copyright (c) 2003-2013 Christopher M. Kohlhoff (chris at kohlhoff dot com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//

#ifndef HTTP_REQUEST_HPP
#define HTTP_REQUEST_HPP

#include <string>
#include <vector>
#include <boost/asio.hpp>
#include "rbc/common/Admin.h"

#define REPLY_OK                    200
#define REPLY_CREATED               201
#define REPLY_ACCEPTED              202
#define REPLY_NO_CONTENT            204
#define REPLY_MULTIPLE_CHOICES      300
#define REPLY_MOVED_PERMANENTLY     301
#define REPLY_MOVED_TEMPORARILY     302
#define REPLY_NOT_MODIFIED          304
#define REPLY_BAD_REQUEST           400
#define REPLY_UNAUTHORIZED          401
#define REPLY_FORBIDDEN             403
#define REPLY_NOT_FOUND             404
#define REPLY_INTERNAL_SERVER_ERROR 500
#define REPLY_NOT_IMPLEMENTED       501
#define REPLY_BAD_GATEWAY           502
#define REPLY_SERVICE_UNAVAILABLE   503

namespace rbc {
namespace http {
namespace server {

struct header{
    std::string name;
    std::string value;
};

struct request{
    std::string method;
    std::string uri;
    int http_version_major;
    int http_version_minor;
    std::vector<header> headers;
};

struct reply{
    enum status_type{
        ok = REPLY_OK,
        created = REPLY_CREATED,
        accepted = REPLY_ACCEPTED,
        no_content = REPLY_NO_CONTENT,
        multiple_choices = REPLY_MULTIPLE_CHOICES,
        moved_permanently = REPLY_MOVED_PERMANENTLY,
        moved_temporarily = REPLY_MOVED_TEMPORARILY,
        not_modified = REPLY_NOT_MODIFIED,
        bad_request = REPLY_BAD_REQUEST,
        unauthorized = REPLY_UNAUTHORIZED,
        forbidden = REPLY_FORBIDDEN,
        not_found = REPLY_NOT_FOUND,
        internal_server_error = REPLY_INTERNAL_SERVER_ERROR,
        not_implemented = REPLY_NOT_IMPLEMENTED,
        bad_gateway = REPLY_BAD_GATEWAY,
        service_unavailable = REPLY_SERVICE_UNAVAILABLE
    } status;
    std::vector<header> headers;
    std::string content;
    std::vector<boost::asio::const_buffer> to_buffers();
    static reply stock_reply(status_type status);
};

namespace misc_strings {
    const char name_value_separator[] = { ':', ' ' };
    const char crlf[] = { '\r', '\n' };
} // namespace misc_strings

namespace status_strings{
    const std::string ok =
      "HTTP/1.0 200 OK\r\n";
    const std::string created =
      "HTTP/1.0 201 Created\r\n";
    const std::string accepted =
      "HTTP/1.0 202 Accepted\r\n";
    const std::string no_content =
      "HTTP/1.0 204 No Content\r\n";
    const std::string multiple_choices =
      "HTTP/1.0 300 Multiple Choices\r\n";
    const std::string moved_permanently =
      "HTTP/1.0 301 Moved Permanently\r\n";
    const std::string moved_temporarily =
      "HTTP/1.0 302 Moved Temporarily\r\n";
    const std::string not_modified =
      "HTTP/1.0 304 Not Modified\r\n";
    const std::string bad_request =
      "HTTP/1.0 400 Bad Request\r\n";
    const std::string unauthorized =
      "HTTP/1.0 401 Unauthorized\r\n";
    const std::string forbidden =
      "HTTP/1.0 403 Forbidden\r\n";
    const std::string not_found =
      "HTTP/1.0 404 Not Found\r\n";
    const std::string internal_server_error =
      "HTTP/1.0 500 Internal Server Error\r\n";
    const std::string not_implemented =
      "HTTP/1.0 501 Not Implemented\r\n";
    const std::string bad_gateway =
      "HTTP/1.0 502 Bad Gateway\r\n";
    const std::string service_unavailable =
      "HTTP/1.0 503 Service Unavailable\r\n";

    boost::asio::const_buffer to_buffer(reply::status_type status){
        switch (status){
            case REPLY_OK:
              return boost::asio::buffer(ok);
            case REPLY_CREATED:
              return boost::asio::buffer(created);
            case REPLY_ACCEPTED:
              return boost::asio::buffer(accepted);
            case REPLY_NO_CONTENT:
              return boost::asio::buffer(no_content);
            case REPLY_MULTIPLE_CHOICES:
              return boost::asio::buffer(multiple_choices);
            case REPLY_MOVED_PERMANENTLY:
              return boost::asio::buffer(moved_permanently);
            case REPLY_MOVED_TEMPORARILY:
              return boost::asio::buffer(moved_temporarily);
            case REPLY_NOT_MODIFIED:
              return boost::asio::buffer(not_modified);
            case REPLY_BAD_REQUEST:
              return boost::asio::buffer(bad_request);
            case REPLY_UNAUTHORIZED:
              return boost::asio::buffer(unauthorized);
            case REPLY_FORBIDDEN:
              return boost::asio::buffer(forbidden);
            case REPLY_NOT_FOUND:
              return boost::asio::buffer(not_found);
            case REPLY_INTERNAL_SERVER_ERROR:
              return boost::asio::buffer(internal_server_error);
            case REPLY_NOT_IMPLEMENTED:
              return boost::asio::buffer(not_implemented);
            case REPLY_BAD_GATEWAY:
              return boost::asio::buffer(bad_gateway);
            case REPLY_SERVICE_UNAVAILABLE:
              return boost::asio::buffer(service_unavailable);
            default:
              return boost::asio::buffer(internal_server_error);
        }
    }
} // namespace status_strings
namespace stock_replies {
    const char ok[] = "";
    const char created[] =
      "<html>"
      "<head><title>Created</title></head>"
      "<body><h1>201 Created</h1></body>"
      "</html>";
    const char accepted[] =
      "<html>"
      "<head><title>Accepted</title></head>"
      "<body><h1>202 Accepted</h1></body>"
      "</html>";
    const char no_content[] =
      "<html>"
      "<head><title>No Content</title></head>"
      "<body><h1>204 Content</h1></body>"
      "</html>";
    const char multiple_choices[] =
      "<html>"
      "<head><title>Multiple Choices</title></head>"
      "<body><h1>300 Multiple Choices</h1></body>"
      "</html>";
    const char moved_permanently[] =
      "<html>"
      "<head><title>Moved Permanently</title></head>"
      "<body><h1>301 Moved Permanently</h1></body>"
      "</html>";
    const char moved_temporarily[] =
      "<html>"
      "<head><title>Moved Temporarily</title></head>"
      "<body><h1>302 Moved Temporarily</h1></body>"
      "</html>";
    const char not_modified[] =
      "<html>"
      "<head><title>Not Modified</title></head>"
      "<body><h1>304 Not Modified</h1></body>"
      "</html>";
    const char bad_request[] =
      "<html>"
      "<head><title>Bad Request</title></head>"
      "<body><h1>400 Bad Request</h1></body>"
      "</html>";
    const char unauthorized[] =
      "<html>"
      "<head><title>Unauthorized</title></head>"
      "<body><h1>401 Unauthorized</h1></body>"
      "</html>";
    const char forbidden[] =
      "<html>"
      "<head><title>Forbidden</title></head>"
      "<body><h1>403 Forbidden</h1></body>"
      "</html>";
    const char not_found[] =
      "<html>"
      "<head><title>Not Found</title></head>"
      "<body><h1>404 Not Found</h1></body>"
      "</html>";
    const char internal_server_error[] =
      "<html>"
      "<head><title>Internal Server Error</title></head>"
      "<body><h1>500 Internal Server Error</h1></body>"
      "</html>";
    const char not_implemented[] =
      "<html>"
      "<head><title>Not Implemented</title></head>"
      "<body><h1>501 Not Implemented</h1></body>"
      "</html>";
    const char bad_gateway[] =
      "<html>"
      "<head><title>Bad Gateway</title></head>"
      "<body><h1>502 Bad Gateway</h1></body>"
      "</html>";
    const char service_unavailable[] =
      "<html>"
      "<head><title>Service Unavailable</title></head>"
      "<body><h1>503 Service Unavailable</h1></body>"
      "</html>";

    std::string to_string(reply::status_type status){
        switch (status){
            case REPLY_OK:
              return ok;
            case REPLY_CREATED:
              return created;
            case REPLY_ACCEPTED:
              return accepted;
            case REPLY_NO_CONTENT:
              return no_content;
            case REPLY_MULTIPLE_CHOICES:
              return multiple_choices;
            case REPLY_MOVED_PERMANENTLY:
              return moved_permanently;
            case REPLY_MOVED_TEMPORARILY:
              return moved_temporarily;
            case REPLY_NOT_MODIFIED:
              return not_modified;
            case REPLY_BAD_REQUEST:
              return bad_request;
            case REPLY_UNAUTHORIZED:
              return unauthorized;
            case REPLY_FORBIDDEN:
              return forbidden;
            case REPLY_NOT_FOUND:
              return not_found;
            case REPLY_INTERNAL_SERVER_ERROR:
              return internal_server_error;
            case REPLY_NOT_IMPLEMENTED:
              return not_implemented;
            case REPLY_BAD_GATEWAY:
              return bad_gateway;
            case REPLY_SERVICE_UNAVAILABLE:
              return service_unavailable;
            default:
              return internal_server_error;
        }
    }
} // namespace stock_replies

std::vector<boost::asio::const_buffer> reply::to_buffers(){
    std::vector<boost::asio::const_buffer> buffers;
    buffers.push_back(status_strings::to_buffer(status));
    for (std::size_t i = 0; i < headers.size(); ++i)
    {
      header& h = headers[i];
      buffers.push_back(boost::asio::buffer(h.name));
      buffers.push_back(boost::asio::buffer(misc_strings::name_value_separator));
      buffers.push_back(boost::asio::buffer(h.value));
      buffers.push_back(boost::asio::buffer(misc_strings::crlf));
    }
    buffers.push_back(boost::asio::buffer(misc_strings::crlf));
    buffers.push_back(boost::asio::buffer(content));
    return buffers;
}

reply reply::stock_reply(reply::status_type status){
    reply rep;
    rep.status = status;
    rep.content = stock_replies::to_string(status);
    rep.headers.resize(2);
    rep.headers[0].name = "Content-Length";
    rep.headers[0].value = std::to_string(rep.content.size());
    rep.headers[1].name = "Content-Type";
    rep.headers[1].value = "text/html";
    return rep;
}
    
class request_handler{
public:
    request_handler(Admin *admin):admin(admin){}

    /// Handle a request and produce a reply.
    void handle_request(const request& req, reply& rep){
        // Decode url to path.
        std::string request_path;
        if (!url_decode(req.uri, request_path)){
            rep = reply::stock_reply(reply::bad_request);
            return;
        }
    
        // Request path must be absolute and not contain "..".
        if (request_path.empty() || request_path[0] != '/'|| request_path.find("..") != std::string::npos){
            rep = reply::stock_reply(reply::bad_request);
            return;
        }
    
        //parse the request
        std::string request(request_path);
        std::vector<std::string> request_vector = split_uri( request, '/' );
        rep.content = admin->exec( request_vector );
    
        // Fill out the reply to be sent to the client.
        rep.status = reply::ok;
        rep.headers.resize(2);
        rep.headers[0].name = "Content-Length";
        rep.headers[0].value = std::to_string(rep.content.size());
        rep.headers[1].name = "Content-Type";
        rep.headers[1].value = "text/plain";
    }

    std::vector<std::string> split_uri(const std::string& uri, char chr){
        std::string::const_iterator first = uri.cbegin();
        std::string::const_iterator second = std::find(first+1, uri.cend(), chr);
        std::vector<std::string> vec;
    
        while(second != uri.cend())
        {
            vec.emplace_back(first+1, second);
            first = second;
            second = std::find(second+1, uri.cend(), chr);
        }
    
        vec.emplace_back(first+1, uri.cend());
    
        return vec;
    }

private:
    static bool url_decode(const std::string& in, std::string& out){
        out.clear();
        out.reserve(in.size());
        for (std::size_t i = 0; i < in.size(); ++i){
            if (in[i] == '%'){
                if (i + 3 <= in.size()){
                    int value = 0;
                    std::istringstream is(in.substr(i + 1, 2));
                    if (is >> std::hex >> value){
                        out += static_cast<char>(value);
                        i += 2;
                    }else{
                        return false;
                    }
                }else{
                    return false;
                }
            }else if (in[i] == '+'){
                out += ' ';
            }else{
                out += in[i];
            }
        }
        return true;
    }
    Admin *admin;
};

class request_parser{
public:
    request_parser():state_(method_start){}
  
    void reset(){
        state_ = method_start;
    }
  
    enum result_type { good, bad, indeterminate };
  
    template <typename InputIterator>
    std::tuple<result_type, InputIterator> parse(request& req, InputIterator begin, InputIterator end){
        while (begin != end){
            result_type result = consume(req, *begin++);
            if (result == good || result == bad)
                return std::make_tuple(result, begin);
        }
        return std::make_tuple(indeterminate, begin);
    }

private:
    /// Handle the next character of input.
    result_type consume(request& req, char input){
        switch (state_){
            case method_start:
                if (!is_char(input) || is_ctl(input) || is_tspecial(input)){
                    return bad;
                }else{
                    state_ = method;
                    req.method.push_back(input);
                    return indeterminate;
                }
            case method:
                if (input == ' '){
                    state_ = uri;
                    return indeterminate;
                }else if (!is_char(input) || is_ctl(input) || is_tspecial(input)){
                    return bad;
                }else{
                    req.method.push_back(input);
                    return indeterminate;
                }
            case uri:
                if (input == ' '){
                    state_ = http_version_h;
                    return indeterminate;
                }else if (is_ctl(input)){
                    return bad;
                }else{
                    req.uri.push_back(input);
                    return indeterminate;
                }
            case http_version_h:
                if (input == 'H'){
                    state_ = http_version_t_1;
                    return indeterminate;
                }else{
                    return bad;
                }
            case http_version_t_1:
                if (input == 'T'){
                    state_ = http_version_t_2;
                    return indeterminate;
                }else{
                    return bad;
                }
            case http_version_t_2:
                if (input == 'T'){
                  state_ = http_version_p;
                  return indeterminate;
                }else{
                  return bad;
                }
            case http_version_p:
                if (input == 'P'){
                    state_ = http_version_slash;
                    return indeterminate;
                }else{
                    return bad;
                }
            case http_version_slash:
                if (input == '/'){
                    req.http_version_major = 0;
                    req.http_version_minor = 0;
                    state_ = http_version_major_start;
                    return indeterminate;
                }else{
                    return bad;
                }
            case http_version_major_start:
                if (is_digit(input)){
                    req.http_version_major = req.http_version_major * 10 + input - '0';
                    state_ = http_version_major;
                    return indeterminate;
                }else{
                    return bad;
                }
            case http_version_major:
                if (input == '.'){
                    state_ = http_version_minor_start;
                    return indeterminate;
                }else if (is_digit(input)){
                    req.http_version_major = req.http_version_major * 10 + input - '0';
                    return indeterminate;
                }else{
                    return bad;
                }
            case http_version_minor_start:
                if (is_digit(input)){
                  req.http_version_minor = req.http_version_minor * 10 + input - '0';
                  state_ = http_version_minor;
                  return indeterminate;
                }else{
                  return bad;
                }
            case http_version_minor:
                if (input == '\r'){
                    state_ = expecting_newline_1;
                    return indeterminate;
                }else if (is_digit(input)){
                    req.http_version_minor = req.http_version_minor * 10 + input - '0';
                    return indeterminate;
                }else{
                    return bad;
                }
            case expecting_newline_1:
                if (input == '\n'){
                    state_ = header_line_start;
                    return indeterminate;
                }else{
                    return bad;
                }
            case header_line_start:
                if (input == '\r'){
                    state_ = expecting_newline_3;
                    return indeterminate;
                }else if (!req.headers.empty() && (input == ' ' || input == '\t')){
                    state_ = header_lws;
                    return indeterminate;
                }else if (!is_char(input) || is_ctl(input) || is_tspecial(input)){
                    return bad;
                }else{
                    req.headers.push_back(header());
                    req.headers.back().name.push_back(input);
                    state_ = header_name;
                    return indeterminate;
                }
            case header_lws:
                if (input == '\r'){
                    state_ = expecting_newline_2;
                    return indeterminate;
                }else if (input == ' ' || input == '\t'){
                    return indeterminate;
                }else if (is_ctl(input)){
                    return bad;
                }else{
                    state_ = header_value;
                    req.headers.back().value.push_back(input);
                    return indeterminate;
            }
            case header_name:
                if (input == ':'){
                    state_ = space_before_header_value;
                    return indeterminate;
                }else if (!is_char(input) || is_ctl(input) || is_tspecial(input)){
                    return bad;
                }else{
                    req.headers.back().name.push_back(input);
                    return indeterminate;
                }
            case space_before_header_value:
                if (input == ' '){
                    state_ = header_value;
                    return indeterminate;
                }else{
                    return bad;
                }
            case header_value:
                if (input == '\r'){
                    state_ = expecting_newline_2;
                    return indeterminate;
                }else if (is_ctl(input)){
                    return bad;
                }else{
                    req.headers.back().value.push_back(input);
                    return indeterminate;
                }
            case expecting_newline_2:
                if (input == '\n'){
                    state_ = header_line_start;
                    return indeterminate;
                }else{
                    return bad;
                }
            case expecting_newline_3:
                return (input == '\n') ? good : bad;
            default:
                return bad;
        }
    }

    /// Check if a byte is an HTTP character.
    static bool is_char(int c){
        return c >= 0 && c <= 127;
    }

    /// Check if a byte is an HTTP control character.
    static bool is_ctl(int c){
        return (c >= 0 && c <= 31) || (c == 127);
    }

    /// Check if a byte is defined as an HTTP tspecial character.
    static bool is_tspecial(int c){
        switch (c){
            case '(': case ')': case '<': case '>': case '@':
            case ',': case ';': case ':': case '\\': case '"':
            case '/': case '[': case ']': case '?': case '=':
            case '{': case '}': case ' ': case '\t':
                return true;
            default:
                return false;
        }
    }

    /// Check if a byte is a digit.
    static bool is_digit(int c){
        return c >= '0' && c <= '9';
    }

    /// The current state of the parser.
    enum state
    {
      method_start,
      method,
      uri,
      http_version_h,
      http_version_t_1,
      http_version_t_2,
      http_version_p,
      http_version_slash,
      http_version_major_start,
      http_version_major,
      http_version_minor_start,
      http_version_minor,
      expecting_newline_1,
      header_line_start,
      header_lws,
      header_name,
      space_before_header_value,
      header_value,
      expecting_newline_2,
      expecting_newline_3
    } state_;
};
} // namespace server
} // namespace http
}

#endif // HTTP_REQUEST_HPP
