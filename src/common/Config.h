#ifndef HDCS_CONFIG_H
#define HDCS_CONFIG_H

#include <map>
#include <string>
#include <vector>
#include <sstream>
#include <iostream>

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>

#define HDCS_OK        0
#define HDCS_ERR      -1
#define HDCS_EAGIN    -2
#define HDCS_ENOMEM   -3


namespace hdcs {

struct hdcs_repl_options {
  hdcs_repl_options(std::string role, std::string replication_nodes): role(role), replication_nodes(replication_nodes){};
  std::string role;
  std::string replication_nodes;
};


class Config{

public:
    typedef std::map<std::string, std::string> ConfigInfo;
    ConfigInfo configValues{
        {"cfg_file_path","/etc/hdcs/general.conf"},
        {"log_to_file","false"},
        {"rbd_pool_name","rbd"},
        {"rbd_volume_name","volume_1"},
        {"cache_dir","/tmp/"},
        {"cache_mode","write_back"},
        {"policy_mode","tier"},
        {"total_size","10737418240"},
        {"cache_total_size","10737418240"},
        {"cache_ratio_health","0.85"},
        {"cache_dirty_timeout_nanoseconds", "10000000000"},
        {"cache_min_alloc_size","4096"},
        {"op_threads_num","64"},
        {"engine_type","simple"},
    };
    Config(std::string name, struct hdcs_repl_options replication_options, std::string config_name="/etc/hdcs/general.conf"){

        const std::string cfg_file = config_name;
        boost::property_tree::ptree pt;
        try {
            boost::property_tree::ini_parser::read_ini(cfg_file, pt);
        } catch(...) {
            std::cout << "error when reading: " << cfg_file
                      << ", config file for missing?" << std::endl;
            // assume general.conf should be created by admin manually
            assert(0);
        }
        configValues["cfg_file_path"] = cfg_file;

        std::string s;
        //scan global section, overwrite default config
        for (ConfigInfo::const_iterator it = configValues.begin(); it!=configValues.end(); it++) {
            try {
                s = pt.get<std::string>("global." + it->first);
            } catch(...) {
                continue;
            }
            if (s != "") {
                configValues[it->first] = s;
            }
            s = "";
        }

        // accept role from cmdline
        // if role is not master/slave, then assert
        if ("master" == replication_options.role) {
          configValues["role"] = "hdcs_master";
          configValues["replication_nodes"] = replication_options.replication_nodes;
        } else if ("slave" == replication_options.role) {
          configValues["role"] = "hdcs_replica";
          configValues["replication_nodes"] = "";
        } else {
          assert(0);
        }

        configValues["rbd_volume_name"] = name;
        configValues["cache_dir_dev"] = configValues["cache_dir"] + "/" + name + "_cache.data";
        configValues["cache_dir_meta"] = configValues["cache_dir"] + "/" + name + "_meta";
        configValues["cache_dir_run"] = configValues["cache_dir"] + "/" + name + "_run";

        for (auto &it : configValues) {
            std::cout << it.first << " : " << it.second << std::endl;

        }
    }
    ~Config(){
    }
};

}

#endif
