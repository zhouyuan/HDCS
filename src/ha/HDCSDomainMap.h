#ifndef HDCSDOMAINMAP_H
#define HDCSDOMAINMAP_H

#include "ha/CrushMapGenerator.h"
#include "ha/HDCSDomainMapRequestHandler.h"
#include <iostream>
#include <sstream>

namespace hdcs {
namespace ha {

class HDCSDomainMap {
public:
  HDCSDomainMap(std::vector<std::string> host_list, uint8_t replication_count):
    replication_count(replication_count),
    cmap(replication_count) {
    for (auto &it : host_list) {
      HDCS_DOMAIN_ITEM_TYPE initial_domain_item;
      initial_domain_item.resize(replication_count);
      domain_map[it] = std::move(initial_domain_item);
    }
  }

  ~HDCSDomainMap() {

  }

  void generate_domain_map () {
    cmap.build(domain_map);
    cmap.get(&domain_map);
  } 

  void offline_host (std::string host) {
    cmap.offline_host(host);
  }

  void online_host (std::string host) {
    cmap.online_host(host);
  }

  void refresh_domain_map () {
    cmap.get(&domain_map);
  }

  HDCS_DOMAIN_ITEM_TYPE get_host_domain_item (std::string host_id) {
    auto it = domain_map.find(host_id);
    if (it == domain_map.end()) {
      HDCS_DOMAIN_ITEM_TYPE new_item;
      new_item.resize(replication_count);
      auto new_it = domain_map.insert(std::pair<std::string, HDCS_DOMAIN_ITEM_TYPE>(host_id, std::move(new_item))); 
      return new_it.first->second;
    } else {
      return it->second;
    }
  }

  uint8_t get_replication_count () {
    return replication_count;
  }

  std::string printToString () {
    std::stringstream ss;
    for (auto &it : domain_map) {
      ss << "Host: " << it.first << " -> {";
      ss << printToString(it.second);
      ss << "}" << std::endl;
    }
    return ss.str();
  }

  std::string printToString (HDCS_DOMAIN_ITEM_TYPE domain_item) {
    std::stringstream ss;
    bool first = true;
    for (auto &it : domain_item) {
      if (!first) ss << ", ";
      else first = false;
      ss << it;
    }
    return ss.str();
  }

  std::string printToString_host_weights () {
    return cmap.printToString_weight();
  }

private:
  HDCS_DOMAIN_MAP_TYPE domain_map;
  uint8_t replication_count;
  CrushMapGenerator cmap;
}; 

}// ha
}// hdcs

#endif
