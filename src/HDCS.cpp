#include <iostream>
#include <boost/program_options.hpp>

#include "HDCSController.h"


namespace po = boost::program_options;

int main(int argc, char **argv) {
  std::string config_name;
  std::string hdcs_role;
  std::string replication_nodes;

  po::options_description desc("Usage:");
  desc.add_options()
      ("help,h", "Show brief usage message")
      ("version,v", "Display the version number")
      ("config,c", po::value<std::string>()->default_value("general.conf"), "Path to Config file")
      ("role,r", po::value<std::string>()->default_value("slave"), "Role")
      ("replicate_nodes,n", po::value<std::string>()->default_value("192.168.1.1:9091"), "Replication nodes");

  po::variables_map args;

  try {
      po::store(po::parse_command_line(argc, argv, desc), args);

      if (args.count("help")) {
        std::cout << desc << std::endl;
        return 0;
      } else if (args.count("version")) {
        //TODO(): extract from header file
        std::cout << "HDCS 1.3.0" << std::endl;
        return 0;
      }

  } catch (po::error const& e) {
      std::cerr << e.what() << '\n';
      exit( EXIT_FAILURE );
  }

  po::notify(args);

  config_name = args["config"].as<std::string>();
  hdcs_role = args["role"].as<std::string>();
  replication_nodes = args["replicate_nodes"].as<std::string>();

  hdcs::hdcs_repl_options repl_opt(hdcs_role, replication_nodes);
  hdcs::HDCSController controller(repl_opt, config_name);
  return 0;
}
