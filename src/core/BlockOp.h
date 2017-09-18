// Copyright [2017] <Intel>
#ifndef HDCS_BLOCK_OP_H
#define HDCS_BLOCK_OP_H

#include "common/AioCompletion.h"
#include "common/Log.h"
#include "common/LRU_Linklist.h"
#include "core/BlockRequest.h"
#include "core/BlockMap.h"
#include "store/SimpleStore/SimpleBlockStore.h"

namespace hdcs {

namespace core {

#define MAX_BLOCK_ID 1073741824 

typedef LRU_LIST<void*> LRU_TYPE;
class Entry;
class BlockOp {
public:
  BlockOp(Block* block, BlockRequest* block_request, BlockOp* block_op) :
          block(block),
          block_request(block_request),
          block_op_next(block_op) {
  }
  void complete(int r) {
    if (r < 0) {
      log_print("Block complete before expected, block: %lu", block->block_id);
      block_request->complete(r);
    } else {
      if (block_op_next != nullptr) {
        block_op_next->send();
      }
    }
    delete this;
  }
  virtual void send() = 0;
  Block* block;
  BlockRequest* block_request;
  BlockOp* block_op_next;
};

class BlockRequestComplete : public BlockOp{
public:
  BlockRequestComplete(Block* block, BlockRequest &&block_request,
                       BlockOp* block_op) :
                       block_request_inst(block_request),
                       BlockOp(block, &block_request_inst, block_op) {
  }
  void send() {
    complete(0);
  }
  void complete(int r) {
    bool call_next = false;
    block->block_mutex.lock();
    if (block_op_next != nullptr) {
      call_next = true;
    } else {
      block->in_process = false;
      block->block_ops_end = nullptr;
    }
    block->block_mutex.unlock();
    
    if(call_next) {
      log_print("Continue to do next request block: %lu", block->block_id);
      block_request->complete(r);
      block_op_next->send();
    } else {
      log_print("Complete block: %lu", block->block_id);
      block_request->complete(r);
    }
    delete this;
  }
  BlockRequest block_request_inst;
};

class DemoteBlockBuffer : public BlockOp{
public:
  DemoteBlockBuffer(char* block_buffer, Block* block,
                   BlockRequest* block_request, BlockOp* block_op) :
                   BlockOp(block, block_request, block_op),
                   block_buffer(block_buffer) {
  }
  void send() {
    free(block_buffer);
    complete(0);
  }
  char* block_buffer;
};

class ReadFromBuffer : public BlockOp{
public:
  ReadFromBuffer(char* block_buffer, Block* block,
                 BlockRequest* block_request, BlockOp* block_op) :
                 BlockOp(block, block_request, block_op),
                 block_buffer(block_buffer) {
  }
  void send() {
    log_print("ReadFromBuffer block: %lu", block->block_id);
    memcpy(block_request->data_ptr, block_buffer+block_request->offset, block_request->size);
    complete(0);
  }
  char* block_buffer;
};

class WriteToBuffer : public BlockOp{
public:
  WriteToBuffer(char* block_buffer, Block* block,
                 BlockRequest* block_request, BlockOp* block_op) :
                 BlockOp(block, block_request, block_op),
                 block_buffer(block_buffer) {
  }
  void send() {
    log_print("WriteToBuffer block: %lu", block->block_id);
    memcpy(block_buffer+block_request->offset, block_buffer, block_request->size);
    complete(0);
  }
  char* block_buffer;
};

class PromoteBlockFromBackend : public BlockOp{
public:
  PromoteBlockFromBackend(char* data, store::DataStore* back_store,
                          Block* block, BlockRequest* block_request,
                          BlockOp* block_op) :
                          BlockOp(block, block_request, block_op),
                          data(data),
                          back_store(back_store) {
  }
  void send() {
    log_print("PromoteBlockFromBackend block: %lu", block->block_id);
    uint64_t block_id = block->block_id;
    /*AioCompletion* on_finish = new AioCompletion(
      [this](ssize_t r){
        complete(r);
    });*/ 
    int ret = back_store->block_read(block_id, data);
    complete(ret);
  }
  store::DataStore *back_store;
  char* data;
};

class WriteBlockToBackend : public BlockOp{
public:
  WriteBlockToBackend(char* data, store::DataStore* back_store,
                      Block* block, BlockRequest* block_request,
                      BlockOp* block_op) :
                      BlockOp(block, block_request, block_op),
                      data(data),
                      back_store(back_store) {
  } 
  void send() {
    log_print("WriteBlockToBackend block: %lu", block->block_id);
    //back_store->block_aio_wrire(block->block_id, block_request->data_ptr, this);
    int ret = back_store->block_write(block->block_id, data);
    complete(ret);
  }
  char* data;
  store::DataStore *back_store;
};

class PromoteFromBackend : public BlockOp{
public:
  PromoteFromBackend(char* data, store::DataStore* back_store,
                      Block* block, BlockRequest* block_request,
                      BlockOp* block_op) :
                      BlockOp(block, block_request, block_op),
                      data(data),
                      back_store(back_store) {
  } 
  void send() {
    log_print("PromoteFromBackend block: %lu", block->block_id);
    //back_store->block_aio_wrire(block->block_id, block_request->data_ptr, this);
    uint64_t offset = block->block_id * block->block_size + block_request->offset;
    int ret = back_store->read(data, offset, block_request->size);
    complete(ret);
  }
  char* data;
  store::DataStore *back_store;
};

class WriteToBackend : public BlockOp{
public:
  WriteToBackend(char* data, store::DataStore* back_store,
                      Block* block, BlockRequest* block_request,
                      BlockOp* block_op) :
                      BlockOp(block, block_request, block_op),
                      data(data),
                      back_store(back_store) {
  } 
  void send() {
    log_print("WriteToBackend block: %lu", block->block_id);
    uint64_t offset = block->block_id * block->block_size + block_request->offset;
    int ret = back_store->write(data, offset, block_request->size);
    complete(ret);
  }
  char* data;
  store::DataStore *back_store;
};

class ReadBlockFromCache : public BlockOp{
public:
  ReadBlockFromCache(uint64_t entry_id, char* data,
                     store::DataStore* data_store,
                     Block* block,
                     BlockRequest* block_request,
                     BlockOp* block_op) :
                     BlockOp(block, block_request, block_op),
                     entry_id(entry_id),
                     data(data),
                     data_store(data_store) {
  }
  void send() {
    log_print("ReadBlockFromCache block: %lu", block->block_id);
    int ret = data_store->block_read(entry_id, data);
    complete(ret);
  }
private:
  uint64_t entry_id;
  char* data;
  store::DataStore *data_store;
};

class WriteBlockToCache : public BlockOp{
public:
  WriteBlockToCache(uint64_t entry_id, char* data,
                    store::DataStore* data_store,
                    Block* block,
                    BlockRequest* block_request,
                    BlockOp* block_op) :
                    BlockOp(block, block_request, block_op),
                    entry_id(entry_id),
                    data(data),
                    data_store(data_store) {
  }
  void send() {
    log_print("WriteBlockToCache block: %lu", block->block_id);
    int ret = data_store->block_write(entry_id, data);
    if (ret >= 0) {
      block->status = LOCATE_IN_CACHE;
    }
    complete(ret);
  }
  uint64_t entry_id;
  store::DataStore *data_store;
  char* data;
};

class DemoteBlockToCache : public BlockOp{
public:
  DemoteBlockToCache(uint64_t entry_id, store::DataStore* data_store,
                    Block* block, BlockRequest* block_request, BlockOp* block_op) :
                    BlockOp(block, block_request, block_op),
                    entry_id(entry_id), data_store(data_store) {
  }
  void send() {
    log_print("DemoteBlockToCache block: %lu", block->block_id);
    int ret = data_store->block_discard(entry_id);
    if (ret >= 0) {
      block->status = NOT_IN_CACHE;
    }
    complete(ret);
  }
  uint64_t entry_id;
  store::DataStore *data_store;
};

class UpdateToMeta : public BlockOp{
public:
  UpdateToMeta(bool* dirty_flag, uint32_t entry_id, store::DataStore* data_store,
               Block* block, BlockRequest* block_request, BlockOp* block_op) :
               entry_id(entry_id), dirty_flag(dirty_flag),
               BlockOp(block, block_request, block_op),
               data_store(data_store) {
  }
  void send() {
    log_print("UpdateToMeta block: %lu", block->block_id);
    assert(entry_id <= MAX_BLOCK_ID);
    uint32_t status = entry_id;
    if (!dirty_flag) {
    // clean
      status = status | ((block->status) << 30) | (0X0 << 31);
    } else {
    // dirty
      status = status | ((block->status) << 30) | (0X1 << 31);
    }
    data_store->block_meta_update(block->block_id, status);  
    complete(0);
  }
  store::DataStore *data_store;
  bool* dirty_flag;
  uint32_t entry_id;
};

class SetDirtyToPolicy : public BlockOp{
public:
  SetDirtyToPolicy(bool* dirty_flag, Block* block, BlockRequest* block_request,
                   BlockOp* block_op) : dirty_flag(dirty_flag),
                   BlockOp(block, block_request, block_op) {
  }
  void send() {
    log_print("SetDirtyToPolicy block: %lu", block->block_id);
    *dirty_flag = true;
    complete(0);
  }
  bool* dirty_flag;
};

class SetCleanToPolicy : public BlockOp{
public:
  SetCleanToPolicy(bool* dirty_flag,  Block* block, BlockRequest* block_request,
                   BlockOp* block_op) : dirty_flag(dirty_flag),
                   BlockOp(block, block_request, block_op) {
  }
  void send() {
    log_print("SetCleanToPolicy block: %lu", block->block_id);
    *dirty_flag = false;
    complete(0);
  }
  bool* dirty_flag;
};

class DoNothing : public BlockOp{
public:
  DoNothing(Block* block, BlockRequest* block_request,
            BlockOp* block_op) :
            BlockOp(block, block_request, block_op){
  }
  void send() {
    log_print("DoNothing block: %lu", block->block_id);
    complete(0);
  }
};

class UpdateLRU : public BlockOp{
public:
  UpdateLRU(LRU_TYPE* clean_lru, LRU_TYPE* dirty_lru,
            bool* dirty_flag, Entry* entry,
            Block* block, BlockRequest* block_request, BlockOp* block_op) :
            clean_lru(clean_lru), dirty_lru(dirty_lru),
            dirty_flag(dirty_flag), entry(entry),
            BlockOp(block, block_request, block_op) {
  }
  void send() {
    log_print("UpdateLRU block: %lu", block->block_id);
    if (*dirty_flag) {
      dirty_lru->touch_key(entry);
    } else {
      clean_lru->touch_key(entry);
    }
    complete(0);
  }
  LRU_TYPE* clean_lru;
  LRU_TYPE* dirty_lru;
  bool* dirty_flag;
  Entry* entry;
};

} //core

} //hdcs
#endif
