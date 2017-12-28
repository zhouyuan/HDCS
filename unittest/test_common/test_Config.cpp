#include <iostream>

#include "../src/common/Config.h"
#include "gtest/gtest.h"

using std::cout;
using std::endl;
using namespace hdcs;

class TEST_Config{
public:

    int controller_config();
    int volume_config();
    void no_config();

private:
    Config* cfg;
};

void TEST_Config::no_config()
{
  struct hdcs_repl_options repl_opt("master", "192.168.0.1:9091");
  cfg = new Config("", repl_opt, "general.conf");
}


int TEST_Config::controller_config()
{
  struct hdcs_repl_options repl_opt("master", "192.168.0.1:9091");
  cfg = new Config("", repl_opt, "../general.conf");
  assert(cfg->configValues["role"] == "hdcs_master");
  assert(cfg->configValues["cfg_file_path"] == "../general.conf");
  assert(cfg->configValues["replication_nodes"] == "192.168.0.1:9091");
  delete cfg;
  return 0;
}

int TEST_Config::volume_config()
{

  struct hdcs_repl_options repl_opt("master", "192.168.0.1:9091");
  cfg = new Config("testrbd", repl_opt, "../general.conf");
  assert(cfg->configValues["cfg_file_path"] == "../general.conf");
  assert(cfg->configValues["rbd_volume_name"] == "testrbd");
  delete cfg;
  return 0;
}

TEST_Config test_config;

TEST (Config, no_config)
{
    EXPECT_DEATH(test_config.no_config(), "");
}

TEST (Config, controller_config)
{
    ASSERT_EQ(0, test_config.controller_config());
}

TEST (Config, volume_config)
{
    ASSERT_EQ(0, test_config.volume_config());
}
