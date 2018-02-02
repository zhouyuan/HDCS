#ifndef HACMDHANDLER_H
#define HACMDHANDLER_H

namespace hdcs {
namespace ha {
typedef uint8_t HDCS_HA_MSG_TYPE;
typedef uint8_t HDCS_CMD_MSG_TYPE;
#define HDCS_MSG_CMD  0X34
#define HDCS_CMD_MSG_REQUEST 0XC0
#define HDCS_CMD_MSG_REPLY 0XC1
#define HDCS_CMD_MSG_CONSOLE 0XC2

struct HDCS_CMD_MSG_T {
  HDCS_HA_MSG_TYPE reserved_flag;
  HDCS_CMD_MSG_TYPE type;
  char* data;
};

class HDCS_CMD_MSG {
public:
  HDCS_CMD_MSG (HDCS_CMD_MSG_TYPE type, std::string cmd):
    header_size(sizeof(HDCS_HA_MSG_TYPE) + sizeof(HDCS_CMD_MSG_TYPE)) {
    data_size = cmd.length();
    data_ = (char*)malloc (header_size + data_size);
    ((HDCS_CMD_MSG_T*)data_)->reserved_flag = HDCS_MSG_CMD; 
    ((HDCS_CMD_MSG_T*)data_)->type = type; 
    memcpy(data_ + header_size, cmd.c_str(), data_size);
  }

  HDCS_CMD_MSG (std::string msg_content):
    header_size(sizeof(HDCS_HA_MSG_TYPE) + sizeof(HDCS_CMD_MSG_TYPE)) {
    data_size = msg_content.length() - header_size;
    data_ = (char*)malloc (header_size + data_size);
    memcpy(data_, msg_content.c_str(), header_size + data_size);
  }

  ~HDCS_CMD_MSG() {
    free(data_);
  }

  char* data() {
    return data_;
  }

  uint64_t size() {
    return header_size + data_size;
  }

  std::string get_cmd() {
    return std::string(data_ + header_size, data_size);
  }

  HDCS_CMD_MSG_TYPE get_type() {
    return ((HDCS_CMD_MSG_T*)data_)->type;
  }

private:
  char* data_;
  uint8_t data_size;
  uint8_t header_size;
};

class HACmdHandler {
public:
  HACmdHandler() {
  }

  ~HACmdHandler() {
  }

  void set_core_stat(HDCSCoreStatController* hdcs_core_stat) {
    core_stat = hdcs_core_stat;
  }

  void register_node (std::string node, networking::Connection* new_conn) {
    hdcs_node_map[node] = new_conn;
  }

  void unregister_node (std::string node) {
    hdcs_node_map.erase(node);
  }

  void request_handler(void* session_id, std::string msg_content, networking::server* listener = nullptr) {
    HDCS_CMD_MSG cmd_msg(msg_content);
    switch (cmd_msg.get_type()) {
      case HDCS_CMD_MSG_CONSOLE:
      {
        std::cout << "HA Manager received CMD is: " << cmd_msg.get_cmd() << std::endl;
        if (cmd_msg.get_cmd().compare("get_status") == 0) {
          core_stat->print();
        } else {
          HDCS_CMD_MSG msg_content(HDCS_CMD_MSG_REQUEST, cmd_msg.get_cmd());
          for (auto &it : hdcs_node_map) {
            it.second->aio_communicate(std::move(std::string(msg_content.data(), msg_content.size())));
          }
        }
        break;
      }
      case HDCS_CMD_MSG_REQUEST:
      {
        std::cout << "HDCS NODE received CMD is: " << cmd_msg.get_cmd() << std::endl;
        HDCS_CMD_MSG msg_content(HDCS_CMD_MSG_REPLY, cmd_msg.get_cmd());
        listener->send(session_id, std::move(std::string(msg_content.data(), msg_content.size())));
        break;
      }
      case HDCS_CMD_MSG_REPLY:
      {
        std::cout << "HA Manager received CMD REPLY is: " << cmd_msg.get_cmd() << std::endl;
        break;
      }
      default:
      {
        break;
      }
    }
  }

  void receiver_handler(void* session_id, std::string msg_content) {

  }

private:
  std::map<std::string, networking::Connection*> hdcs_node_map;
  HDCSCoreStatController* core_stat;
};
}// ha
}// hdca

#endif
