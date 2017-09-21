// Copyright [2017] <Intel>
#ifndef HDCS_CACHE_POLICY_H
#define HDCS_CACHE_POLICY_H
#include "core/BlockOp.h"
#include "core/BlockRequest.h"
#include "core/policy/Policy.h"
#include "common/LRU_Linklist.h"
#include "store/DataStore.h"
#include "common/WorkQueue.h"
#include <mutex>
#include <condition_variable>

namespace hdcs {

namespace core {

struct Entry {
  Entry (uint32_t entry_id) : entry_id(entry_id), is_dirty(false) {
  }
  const uint32_t entry_id;
  bool is_dirty;
};  

typedef std::vector<Entry> Entries;
class CachePolicy : public Policy {
public:
  CachePolicy(uint64_t total_size, uint64_t cache_size, uint32_t block_size,
              Block** block_map,
              store::DataStore *data_store,
              store::DataStore *back_store,
              float cache_ratio_health, WorkQueue<void*> *request_queue);
  ~CachePolicy();
  BlockOp* map(BlockRequest &&block_request, BlockOp** block_op_end);

private:
  void process();
  bool go;
  uint64_t blocks_count;
  uint64_t cache_blocks_count;
  Entries entries;
  std::mutex entry_map_lock;
  LRU_TYPE free_lru;
  LRU_TYPE dirty_lru;
  LRU_TYPE clean_lru;
  uint64_t total_size;
  uint64_t cache_size;
  uint32_t block_size;
  store::DataStore *data_store;
  store::DataStore *back_store;
  float cache_ratio_health;
  WorkQueue<void*> *request_queue;

  std::thread *process_thread;
  std::condition_variable process_thread_cond;
  std::mutex process_thread_cond_lock;
  std::atomic<uint64_t> process_blocks_count;

  struct EntryToBlock_t {
    bool valid;
    Block* block;
    bool dirty_flag;
    EntryToBlock_t(): valid(false){}
  };
};

}//core

}//hdcs

#endif
