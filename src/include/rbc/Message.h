#ifndef MESSAGE_H
#define MESSAGE_H

#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <iostream>
#include <sstream>
#include <boost/archive/binary_oarchive.hpp>
#include <boost/archive/binary_iarchive.hpp>
#include <boost/serialization/string.hpp>

#define LOCATION_BUFFER_SIZE 128
#define MSG_FLAG_SIZE 8
#define MSG_FLAG  0xFAFA0F0F
#define MSG_WRITE 0X0001
#define MSG_READ  0X0002
#define MSG_REPLY_DATA 0X0003
#define MSG_REPLY_STAT  0X0004
#define MSG_FLUSH  0X0005
#define MSG_DISCARD  0X0006
#define MSG_SUCCESS  0X000F
#define MSG_FAIL  0X0000
#define MSG_HEADER_LEN 89 

namespace rbc {

struct Msg_Header{
    uint32_t type;
    uint64_t seq_id;
    uint64_t offset;
    uint64_t length;
    uint64_t content_length;
    ssize_t reserve;
    void init( uint64_t offset_p, uint64_t data_len_p, uint64_t location_id_length, uint32_t type_p, uint64_t seq_id_p ){
        type = type_p;
        seq_id = seq_id_p;
        offset = offset_p;
        length = data_len_p + location_id_length;
        content_length = data_len_p;
        reserve = 0;
    }

    friend class boost::serialization::access;
    template<class Archive>
    void serialize( Archive & ar, const unsigned int version ){
        ar & type;
        ar & seq_id;
        ar & offset;
        ar & length;
        ar & content_length;
        ar & reserve;
    }
};

struct Msg{
    Msg_Header header;
    //std::string location_id;
    char* location_id = NULL;
    char* content = NULL;
    //std::string content_str;

    Msg( const char* location, uint64_t offset, const char* data, uint64_t data_len, uint32_t type=MSG_WRITE, uint64_t seq_id = 0 ){
        //printf("msg location id length: %ld\n", strlen(location));
        header.init( offset, data_len, strlen(location), type, seq_id );
        location_id = const_cast<char*>(location);
        content = const_cast<char*>(data);
    }

    Msg( const char* location, uint64_t offset, std::string data, uint64_t data_len, uint32_t type=MSG_WRITE, uint64_t seq_id = 0 ){
        header.init( offset, data_len, strlen(location), type, seq_id );
        location_id = const_cast<char*>(location);
        content = const_cast<char*>(data.c_str());
    }

    Msg( std::string data, char* shared_mem_ptr = NULL ){
        std::istringstream archive_stream(data);
        boost::archive::binary_iarchive archive(archive_stream);
        archive >> header;

        if( shared_mem_ptr ){
            uint64_t location_len = header.length - header.content_length;
            char* data_ptr = const_cast<char*>(data.c_str());

            location_id = new char[location_len+1]();
            memcpy( location_id, &data_ptr[MSG_HEADER_LEN], location_len );
            if(header.type == MSG_WRITE || header.type == MSG_READ || header.type == MSG_REPLY_DATA){
                content = &shared_mem_ptr[header.reserve];
            }
        }else{
            //content = new char[header.content_length]();
        }
    }

    ~Msg(){
    }

    ssize_t length(){
        return header.length;
    }

    ssize_t content_length(){
        return header.content_length;
    }

    char* get_location_id(){
        return location_id;
    }

    ssize_t get_reserve(){
        return header.reserve;
    }

    std::string headerToString(){
        std::stringstream ss;
        boost::archive::binary_oarchive oa(ss);
        oa << header;
        ss << location_id;
        return ss.str();
    }

    std::string toString_shm(){
        std::stringstream ss;
        ss << headerToString();
        return ss.str();
    }

    std::string toString(){
        std::stringstream ss;
        ss << headerToString();
        if( header.content_length ){
            std::string data(content, header.content_length);
            ss << data;
        }
        return ss.str();
    }

    int cp_content_to_shm( char* shm_ptr ){
        memcpy( shm_ptr, content, header.content_length );
        content = shm_ptr;
    }

    void set_type(uint32_t type){
        header.type = type;
    }

    void set_length(uint64_t length){
        header.content_length = length;
        header.length = length + strlen(location_id);
    }

    void set_callback( void* arg ){
        header.seq_id = (uint64_t)arg;
    }

    void set_seq_id( uint64_t seq ){
        header.seq_id = seq;
    }

    void set_reserve( ssize_t data ){
        header.reserve = data;
    }

    void set_location_id( char* location_id_p ){
        location_id = location_id_p;
    }

    void set_content( char* content_p ){
        content = content_p;
    }

    void delete_location_id(){
        if(location_id) delete location_id;
    }

    void delete_content(){
        if(content) delete content;
    }
};

}
#endif
