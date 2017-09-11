// Copyright [2017] <Intel>
#include "core/BlockOp.h"
#include "core/BlockRequest.h"
#include "core/policy/CachePolicy.h"
#include "common/LRU_Linklist.h"

namespace hdcs {

namespace core {

CachePolicy::CachePolicy(uint64_t total_size, uint64_t cache_size, uint32_t block_size,
            store::DataStore *data_store, store::DataStore *back_store) :
            total_size(total_size), cache_size(cache_size),
            block_size(block_size), data_store(data_store),
            back_store(back_store) {
  blocks_count = total_size / block_size + 1; 
  cache_blocks_count = cache_size / block_size + 1; 
  for (int64_t i = cache_blocks_count - 1; i >= 0; i--) {
    entries.push_back(Entry(i));
  }
  for (auto &entry : entries) {
    free_lru.touch_key(&entry);
  }
}

CachePolicy::~CachePolicy() {
  delete data_store;
  delete back_store;
}

BlockOp* CachePolicy::map(BlockRequest &&block_request, BlockOp** block_op_end) {
  std::lock_guard<std::mutex> lock(entry_map_lock);
  Entry *entry;
  Block* block = block_request.block;
  assert (block != nullptr);
  char* block_buffer = nullptr;
  Entry* cache_entry = nullptr;
  
  BlockOp* block_op = new BlockRequestComplete(block, std::move(block_request), nullptr);
  BlockRequest* block_request_ptr = block_op->block_request;
  *block_op_end = block_op;
  switch (block_request.req->io_type) {
    case IO_TYPE_READ:
      if (block->entry != nullptr){ //in cache
        cache_entry = block->entry;
        if (block_request.size < block->block_size) {// partial read
          block_buffer = new char[block->block_size]();
          block_op = new DemoteBlockBuffer(block_buffer, block, block_request_ptr, block_op);
          block_op = new ReadFromBuffer(block_buffer, block, block_request_ptr, block_op);
          block_op = new ReadBlockFromCache(cache_entry->entry_id, block_buffer, data_store,
                                            block, block_request_ptr, block_op); 
        } else {// full block read
          block_op = new ReadBlockFromCache(cache_entry->entry_id, block_request_ptr->data_ptr,
                                            data_store, block, block_request_ptr, block_op); 
        }
      } else { //not in cache
        //find a cache entry
        cache_entry = (Entry*)free_lru.get_head();
        if (cache_entry != nullptr) {
          free_lru.remove((void*)cache_entry);
          block->entry = cache_entry;
          if (block_request_ptr->size < block->block_size) {// partial read
            block_buffer = new char[block->block_size]();
            block_op = new DemoteBlockBuffer(block_buffer, block, block_request_ptr, block_op);
            block_op = new ReadFromBuffer(block_buffer, block, block_request_ptr, block_op);
            block_op = new WriteBlockToCache(cache_entry->entry_id, block_buffer, data_store,
                                           block, block_request_ptr, block_op); 
            block_op = new PromoteBlockFromBackend(block_buffer, back_store,
                                                 block, block_request_ptr, block_op); 
          } else {// full block read
            block_op = new WriteBlockToCache(cache_entry->entry_id, block_request_ptr->data_ptr, data_store,
                                           block, block_request_ptr, block_op); 
            block_op = new PromoteBlockFromBackend(block_request_ptr->data_ptr, back_store,
                                                 block, block_request_ptr, block_op); 
          }
        } else { //cache run out
          block_op = new PromoteFromBackend(block_request_ptr->data_ptr, back_store,
                                            block, block_request_ptr, block_op); 
        }
      }
      break;
    case IO_TYPE_WRITE:
      if (block->entry != nullptr){ //in cache
        cache_entry = block->entry;
        //block_op = new UpdateToMeta(block, &block_request, block_op, data_store); 
        if (block_request_ptr->size < block->block_size) {// partial write
          block_buffer = new char[block->block_size]();
          block_op = new DemoteBlockBuffer(block_buffer, block, block_request_ptr, block_op);
          block_op = new WriteBlockToCache(cache_entry->entry_id, block_buffer, data_store,
                                           block, block_request_ptr, block_op); 
          block_op = new WriteToBuffer(block_buffer, block, block_request_ptr, block_op);
          block_op = new ReadBlockFromCache(cache_entry->entry_id, block_request_ptr->data_ptr,
                                            data_store, block, block_request_ptr, block_op); 
        } else {// full block write
          block_op = new WriteBlockToCache(cache_entry->entry_id, block_request_ptr->data_ptr, data_store,
                                           block, block_request_ptr, block_op); 
        }
      } else { //not in cache
        cache_entry = (Entry*)free_lru.get_head();
        if (cache_entry != nullptr) {
          free_lru.remove((void*)cache_entry);
          block->entry = cache_entry;
          if (block_request_ptr->size < block->block_size) {// partial write
            block_buffer = new char[block->block_size]();
            block_op = new DemoteBlockBuffer(block_buffer, block, block_request_ptr, block_op);
            block_op = new WriteBlockToCache(cache_entry->entry_id, block_buffer, data_store,
                                             block, block_request_ptr, block_op); 
            block_op = new WriteToBuffer(block_buffer, block, block_request_ptr, block_op);
            block_op = new ReadBlockFromCache(cache_entry->entry_id, block_request_ptr->data_ptr,
                                              data_store, block, block_request_ptr, block_op); 
          } else {// full block write
            block_op = new WriteBlockToCache(cache_entry->entry_id, block_request_ptr->data_ptr, data_store,
                                             block, block_request_ptr, block_op); 
          }
        } else {// run out cache
          block_op = new WriteToBackend(block_request_ptr->data_ptr, back_store,
                                        block, block_request_ptr, block_op); 
        }
      }
      break;
    case IO_TYPE_DISCARD:
      switch (block->status) {
        case LOCATE_IN_CACHE:
          /*block_op = new UpdateToMeta(block, &block_request, block_op, data_store); 
          block_op = new SetBlockStatus(NOT_IN_CACHE, block, &block_request, block_op); 
          block_op = new WriteBlockToBackend(block, &block_request, block_op, back_store); 
          break;
          */
        case NOT_IN_CACHE:
        default:
          block_op = new DoNothing(block, block_request_ptr, block_op); 
          break;
      }//switch block->status
      break;
    case IO_TYPE_FLUSH:
      switch (block->status) {
        case LOCATE_IN_CACHE:
          /*
          block_op = new UpdateToMeta(block, &block_request, block_op, data_store); 
          block_op = new SetCleanToPolicy(block, &block_request, block_op); 
          block_op = new WriteBlockToBackend(block, &block_request, block_op, back_store); 
          */
          break;
        case NOT_IN_CACHE:
        default:
          block_op = new DoNothing(block, block_request_ptr, block_op); 
          break;
      }// switch block->status
      break;
    default:
      block_op = new DoNothing(block, block_request_ptr, block_op); 
  }// switch io_type
  return block_op;
}// map
  
}// core
}// hdcs

