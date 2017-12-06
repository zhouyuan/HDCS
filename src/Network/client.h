#ifndef CLIENT 
#define CLIENT 
#include <mutex>
#include <string>
#include <thread>
#include <map>
#include <vector>
#include <atomic>
#include <memory>
#include <atomic>
#include "connect.h"
//#include "../io_service/thread_group.h"

namespace hdcs{
namespace networking{
class Connection{   
private:

    std::vector<SessionPtr> session_vec;
    std::atomic<int> session_index;
    std::atomic<bool> is_closed;
    Connect m_connect;
    ProcessMsgClient process_msg;
    void* process_msg_arg;
    int session_num;
    std::mutex receive_lock;
    bool is_begin_aio;
    std::mutex send_lock;
//    ThreadGroup thread_pool;
public:

    Connection( ProcessMsgClient _process_msg , int _s_num, int _thd_num)
        : session_index(0)
        , session_num(_s_num)
        , process_msg(_process_msg)
        , is_begin_aio(false)
        , m_connect(_s_num, _thd_num)
        , is_closed(true)
       // , thread_pool(10)
    {}

    ~Connection(){
        if(!is_closed.load()){
            close();
        }
    }

    void close() {
        for(int i = 0 ; i < session_vec.size(); ++i){
            session_vec[i]->close();
            delete session_vec[i];
        }
        is_closed.store(true);
    }

    void cancel(){
        for(int i = 0; i < session_vec.size(); ++i){
            session_vec[i]->cancel();
        }
        sleep(1);
    }
    
    void set_session_arg(void* arg){
        process_msg_arg = arg; 
        for(int i = 0; i < session_vec.size(); ++i){
            session_vec[i]->set_session_arg(arg);
        }
    }

    int connect( std::string ip_address, std::string port){
        SessionPtr new_session;
        for(int i=0; i < session_num; i++){
            new_session = m_connect.sync_connect( ip_address, port, process_msg );
            if(new_session != NULL){
                session_vec.push_back( new_session );
            }else{
                std::cout<<"Client::sync_connect failed.."<<std::endl;
            }
        }
        if( session_vec.size() == session_num ){
            std::cout<<"Networking: "<<session_vec.size()<<" sessions have been created..."<<std::endl;
            is_closed.store(true);
        }else{
            assert(0);
        }
        return 0;
    }

    ssize_t communicate( std::string send_buffer){
        send_lock.lock();
        int temp_index = session_index;
        if(++session_index==session_vec.size()){
            session_index = 0;
        }
        send_lock.unlock();
#ifdef INFO
        std::cout<<"client::communicate."<<std::endl;
#endif
        ssize_t ret = session_vec[temp_index]->communicate(send_buffer);
        return ret;
    }

    void aio_communicate(std::string&& send_buffer){
        int temp_index; 
        send_lock.lock();
        temp_index = session_index;
        if(++session_index==session_vec.size()){
            session_index = 0;
        }
        send_lock.unlock();
#ifdef INFO
        std::cout<<"client::aio_communicate."<<std::endl;
#endif
        session_vec[temp_index]->aio_communicate( send_buffer );
    }

private:

    Session* select_idle_session(){
        while(true){
            for( int i = 0; i<session_vec.size(); i++){
                if(!(session_vec[i]->if_busy())){
                    std::cout<<"select session id is "<<i<<std::endl;
                    session_vec[i]->set_busy();
                    return session_vec[i];
                }
            }
        }
    }

};
} //hdcs
}
#endif
