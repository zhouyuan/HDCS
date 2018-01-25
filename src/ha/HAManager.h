#ifndef HDCS_HA_MANAGER_H
#define HDCS_HA_MANAGER_H

#include "common/AioCompletionImp.h"
#include <iostream>
#include "HDCSDomainMap.h"

namespace hdcs {
namespace ha {

class HAManager : public HACore{
public:
  HAManager (std::string name, std::string config_path = "") :
    HACore(config_path, "10001"),
    core_stat_receiver(name, &global_domain_map),
    global_domain_map(get_host_list(), get_replication_count()),
    hb_worker(std::move(HeartBeatOpts(1000000000, 1000000000))){
      core_stat_receiver.set_host_list(get_host_list());
      global_domain_map.generate_domain_map();
  }

  void register_hdcs_node (std::string node) {
    //create conn
    int colon_pos;
    colon_pos = node.find(':');
    std::string addr = node.substr(0, colon_pos);
    std::string port = node.substr(colon_pos + 1, node.length() - colon_pos);
    //not same as current messenger, dehao will fix network later.
    auto it = conn_map.insert(std::pair<std::string, networking::Connection*>(node,
      new networking::Connection([&](void* p, std::string s){request_handler(p, s);}, 1, 1)));
    it.first->second->connect(addr, port);

    // register to Heartbeat
    std::shared_ptr<hdcs::AioCompletion> err_handler = std::make_shared<hdcs::AioCompletionImp>([node](ssize_t r){
     printf("bad news, heartbeat to %s failed.\n", node.c_str());    
     // update to ha_core
     //update_node_status(node, HDCS_HEARTBEAT_FAIL);
    }, -1, false);
    hb_worker.register_node(it.first->second, node, err_handler);

    // register to CMDHandler
    cmd_handler.register_node(node, it.first->second);
  }

  void unregister_hdcs_node (std::string node) {
    //unregister from HeartBeat
    hb_worker.unregister_node(node);

    //unregister from CMDHandler
    cmd_handler.unregister_node(node);
  }

  void handle_heartbeat_request (void* session_arg, std::string msg_content) {
    hb_worker.request_handler(session_arg, msg_content);
  }

  void handle_core_stat_request (void* session_arg, std::string msg_content) {
    core_stat_receiver.request_handler(session_arg, msg_content); 
  }

  void handle_mgr_request (void* session_arg, std::string msg_content) {
    cmd_handler.request_handler(session_arg, msg_content);
  }

  void process_cmd (std::string cmd) {
    HDCS_CMD_MSG cmd_msg(HDCS_CMD_MSG_CONSOLE, cmd);
    handle_mgr_request (nullptr, std::move(std::string(cmd_msg.data(), cmd_msg.size())));
  }
private:
  HeartBeatService hb_worker;
  HDCSCoreStatController core_stat_receiver;
  HDCSDomainMap global_domain_map;
};

}// ha
}// hdcs

#endif
