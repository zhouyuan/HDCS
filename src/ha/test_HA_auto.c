#include "ha/HAClient.h"
#include "ha/HAManager.h"
#include "common/AioCompletionImp.h"
#include <iostream>

int main(int argc, char *argv[]) {
  if (argc == 5) {
  } else {
   printf("Usage:\n\t%s -r server/client -n ${name}\n\n", argv[0]);
   return -1;
  }

  hdcs::ha::HAConfig ha_config("");
  std::string cmd;
  std::string node;
  if (argv[2][0] == 'c') {
    hdcs::ha::HAClient ha_client(argv[4], std::move(ha_config));
    ha_client.add_ha_server("host01");
    while (true) {
      printf("Input bye to exit.");
      std::cin >> cmd;
      if (cmd.compare("bye") == 0) break;
    }
  }

  if (argv[2][0] == 's') {
    hdcs::ha::HAManager ha_mgr(argv[4], std::move(ha_config));
    while (true) {
      printf("Please input your cmd(bye/cmdline): ");
      std::cin >> cmd;
      if (cmd.compare("bye") == 0) break;
      else {
        ha_mgr.process_cmd(cmd);
      }
    }
  }
  return 0;
}
