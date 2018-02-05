#ifndef HDCSDOMAINMAPREQUESTHANDLER_H
#define HDCSDOMAINMAPREQUESTHANDLER_H

namespace hdcs {
namespace ha {

typedef uint8_t HDCS_HA_MSG_TYPE;
#define HDCS_MSG_DOMAIN_MAP  0X33

struct HDCS_DOMAIN_ITEM_MSG_HEADER_T {
  HDCS_HA_MSG_TYPE reserved_flag;
};

struct HDCS_DOMAIN_ITEM_MSG_DATA_T {
  char node_name[32];
};

struct HDCS_DOMAIN_ITEM_MSG_T {
  HDCS_DOMAIN_ITEM_MSG_HEADER_T header;
  HDCS_DOMAIN_ITEM_MSG_DATA_T* data;
};

class HDCS_DOMAIN_ITEM_MSG {
public:
  HDCS_DOMAIN_ITEM_MSG (HDCS_DOMAIN_ITEM_TYPE domain_item)
    : replication_num(domain_item.size()),
      data_size(sizeof(HDCS_DOMAIN_ITEM_MSG_DATA_T) * replication_num) {
    data_ = (char*)malloc(data_size + sizeof(HDCS_DOMAIN_ITEM_MSG_HEADER_T));
    memset(data_, 0, data_size + sizeof(HDCS_DOMAIN_ITEM_MSG_HEADER_T));
    ((HDCS_DOMAIN_ITEM_MSG_T*)data_)->header.reserved_flag = HDCS_MSG_DOMAIN_MAP; 

    int i = 0;
    for (auto &it : domain_item) {
      char* node_name = data_ + sizeof(HDCS_DOMAIN_ITEM_MSG_HEADER_T) + i++ * sizeof(HDCS_DOMAIN_ITEM_MSG_DATA_T);
      memcpy(node_name, it.c_str(), it.size());
    }
  }

  HDCS_DOMAIN_ITEM_MSG (std::string msg) {
    data_size = msg.length() - sizeof(HDCS_DOMAIN_ITEM_MSG_HEADER_T);
    data_ = (char*)malloc (sizeof(HDCS_DOMAIN_ITEM_MSG_HEADER_T) + data_size);
    memcpy(data_, msg.c_str(), sizeof(HDCS_DOMAIN_ITEM_MSG_HEADER_T) + data_size);
    replication_num = data_size / sizeof(HDCS_DOMAIN_ITEM_MSG_DATA_T);

  }

  ~HDCS_DOMAIN_ITEM_MSG() {
    free(data_);
  }

  uint8_t get_replication_num() {
    return replication_num;
  }

  char* data() {
    return data_;
  }

  uint64_t size() {
    return sizeof(HDCS_DOMAIN_ITEM_MSG_HEADER_T) + data_size;
  }

  HDCS_DOMAIN_ITEM_TYPE get_domain_item() {
    HDCS_DOMAIN_ITEM_TYPE domain_item;
    for (int i = 0; i < replication_num; i++) {
      char* node_name = data_ + sizeof(HDCS_DOMAIN_ITEM_MSG_HEADER_T) + i * sizeof(HDCS_DOMAIN_ITEM_MSG_DATA_T);
      domain_item.push_back(std::string(node_name));
    }
    return domain_item;
  } 

private:
  char* data_;
  uint8_t replication_num;
  uint64_t data_size;
};

}// ha
}// hdcs
#endif
