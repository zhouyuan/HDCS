#ifndef HDCS_HA_CONFIG
#define HDCS_HA_CONFIG

#include <vector>
#include <string>
#include <boost/algorithm/string.hpp>
namespace hdcs {
namespace ha {
class HAConfig {
public:
  HAConfig (std::string path) {

  }

  ~HAConfig () {

  }

  std::string get(std::string key) {
    return config_data.find(key)->second;
  }

  std::vector<std::string> get_host_list () {
    std::string host_list_iss(get("hdcs_host_list"));
    std::vector<std::string> nodes;
    boost::erase_all(host_list_iss, " ");
    boost::split(nodes, host_list_iss, boost::is_any_of(","));
    return nodes;
  }

private:
  std::map<std::string, std::string> config_data{
    {"ha_heartbeat_listen_port", "10000"},
    {"hdcs_replication_count", "3"},
    {"hdcs_host_list", "host01, host02, host03, host04, host05, host06"}
  };
};
}// ha
}// hdcs

#endif
