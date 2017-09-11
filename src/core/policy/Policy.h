// Copyright [2017] <Intel>
#ifndef HDCS_POLICY_H
#define HDCS_POLICY_H
#include "core/BlockOp.h"

namespace hdcs {

namespace core {
  class Policy {
  public:
    virtual BlockOp* map(BlockRequest &&block_request, BlockOp** block_op_end) = 0;

  };

}// core

}// hdcs
#endif
