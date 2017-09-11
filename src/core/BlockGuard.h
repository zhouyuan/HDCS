// Copyright [2017] <Intel>
#ifndef HDCS_BLOCK_GUARD_H
#define HDCS_BLOCK_GUARD_H

#include "BlockRequest.h"
#include "BlockMap.h"

#include "common/Log.h"
namespace hdcs {

namespace core {

class BlockGuard {
public:
  BlockGuard(uint64_t total_size, uint32_t block_size) : 
         total_size(total_size), block_size(block_size) {
    uint64_t block_count = total_size / block_size;
    log_print("Total blocks: %lu", block_count);
    for (uint64_t i = 0; i < block_count; i++) {
      Block* block = new Block(i, block_size);
      block_map.insert(std::make_pair(i, block));
    }
  }

  ~BlockGuard() {
    for (auto &block : block_map) {
      delete block.second;
    }
  }

  void create_block_requests(Request *req, BlockRequestList *block_request_list) {
    uint64_t offset = req->offset;
    uint64_t length = req->length;
    uint64_t left = length;
    uint64_t offset_by_block = 0;
    uint64_t length_by_block = 0;
    char* data_ptr = req->data;
    Block* block;
    uint64_t block_id;

    while(left) {
      block_id = offset / block_size;
      auto block_it = block_map.find(block_id);
      if (block_it == block_map.end()) {
        log_print("hit block map end, block_map length: %lu, block_id: %lu\n", block_map.size(), block_id);
        assert(0);
      }
      block = block_it->second;

      offset_by_block = offset % block_size;
      length_by_block = (block_size - offset_by_block) < left ?
                          (block_size - offset_by_block):left;
      block_request_list->emplace_back(std::move(BlockRequest(
                                       data_ptr, offset_by_block,
                                       length_by_block, req, block)));
      data_ptr = req->data + length_by_block;
      left -= length_by_block;
      offset += length_by_block;
    }
  }

private:
  BlockMap block_map;
  uint64_t total_size;
  uint32_t block_size;

};

} //namespace core
} //namespace core
#endif
