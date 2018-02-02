#ifndef HDCS_HA_CONFIG
#define HDCS_HA_CONFIG

#include <vector>
#include <string>
#include <boost/algorithm/string.hpp>
namespace hdcs {
namespace ha {
class HAConfig {
private:
  std::map<std::string, std::string> config_data{
    {"ha_heartbeat_listen_port", "10000"},
    {"hdcs_replication_count", "3"},
    {"status_check_timeout", "30000000000"},
    {"layback_domain_distribute_timeout", "10000000000"},
    {"hdcs_host_list", "host02, host03, host04, host05, host06"}
  };

  std::map<std::string, std::string> host_to_addr_map{
    {"host01", "127.0.0.1:10001"},
    {"host02", "127.0.0.1:10002"},
    {"host03", "127.0.0.1:10003"},
    {"host04", "127.0.0.1:10004"},
    {"host05", "127.0.0.1:10005"},
    {"host06", "127.0.0.1:10006"}
  };

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

  std::string get_host_addr (std::string host_name) {
    auto it = host_to_addr_map.find(host_name);
    assert (it != host_to_addr_map.end());
    return it->second;
  }

  std::string get_host_port (std::string host_name) {
    auto it = host_to_addr_map.find(host_name);
    assert (it != host_to_addr_map.end());

    std::string host_addr_iss(it->second);
    std::cout << host_addr_iss << std::endl;
    std::vector<std::string> addr;
    boost::erase_all(host_addr_iss, " ");
    boost::split(addr, host_addr_iss, boost::is_any_of(":"));
    return addr[1];
  }

};
}// ha
}// hdcs

#endif
