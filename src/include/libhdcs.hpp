//Copyright [2017] <Intel>
#include <stdint.h>
#include <cstddef>
#include "libhdcs.h"

#ifndef LIB_HDCS_H
#define LIB_HDCS_H

namespace hdcs {
  namespace core {
    class HDCSCore;
  }
}

class libhdcs {
public:
  libhdcs(const char* name);
  ~libhdcs();
  int hdcs_aio_read(const char* volume_name, char* data, uint64_t offset, uint64_t length, hdcs_completion_t c);
  int hdcs_aio_write(const char* volume_name, const char* data, uint64_t offset, uint64_t length, hdcs_completion_t c);
private:
  hdcs::core::HDCSCore* hdcs_inst;
};
#endif
