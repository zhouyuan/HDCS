// Copyright [2017] <Intel>

#ifndef HDCS_INSTANCE_CTX_H
#define HDCS_INSTANCE_CTX_H

#include "core/policy/Policy.h"
#include "core/BlockGuard.h"
#include "core/store/DataStore.h"

namespace hdcs {
namespace core {

class InstanceCtx {
public:
  InstanceCtx(Policy policy, BlockGuard block_guard,
              DataStore data_store, BackendStore back_store):
              policy(policy), block_guard(block_guard),
              data_store(data_store), back_store(back_store) {

  }

  ~InstanceCtx() {

  }
  
  Policy policy;
  BlockGuard block_guard;
  DataStore data_store;
  DataStore back_store;
};

}// hdcs
}// core

#endif
