#include "HDCSDomainMap.h"

int main () {
  std::vector<std::string> host_list = {
    "host01",
    "host02",
    "host03",
    "host04",
    "host05",
    "host06",
    "host07",
    "host08",
    "host09",
    "host10",
    "host11",
    "host12",
    "host13",
    "host14",
    "host15",
    "host16",
    "host17",
    "host18",
    "host19",
    "host20"
  };
  printf("Init map\n");
  hdcs::ha::HDCSDomainMap domain_map(host_list, 3);
  domain_map.generate_domain_map();
  domain_map.print();

  printf("Remove host 14\n");
  domain_map.rm_host("host14");
  domain_map.refresh_domain_map();
  domain_map.print();

  printf("Remove host 03\n");
  domain_map.rm_host("host03");
  domain_map.refresh_domain_map();
  domain_map.print();

  printf("Remove host 17\n");
  domain_map.rm_host("host17");
  domain_map.refresh_domain_map();
  domain_map.print();
  return 0;
}
