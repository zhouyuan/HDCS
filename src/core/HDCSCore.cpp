// Copyright [2017] <Intel>

#include "core/HDCSCore.h"
#include "core/policy/CachePolicy.h"
#include "store/SimpleStore/SimpleBlockStore.h"
#include "store/RBD/RBDImageStore.h"

#include <string>

namespace hdcs {
namespace core {
HDCSCore::HDCSCore() {
  config = new Config("hdcs"); 

  std::string log_path = config->configValues["log_to_file"];
  std::cout << "log_path: " << log_path << std::endl;
  if( log_path!="false" ){
    int stderr_no = dup(fileno(stderr));
    log_fd = fopen( log_path.c_str(), "w" );
	  if(log_fd==NULL){}
    if(-1==dup2(fileno(log_fd), STDERR_FILENO)){}
  }

  int hdcs_thread_max = stoi(config->configValues["cacheservice_threads_num"]);
  hdcs_op_threads = new ThreadPool( hdcs_thread_max );
  uint64_t total_size = stoull(config->configValues["total_size"]);
  uint64_t block_size = stoull(config->configValues["cache_min_alloc_size"]);
  uint64_t cache_size = stoull(config->configValues["cache_total_size"]);
  std::string path = config->configValues["cache_dir_run"];
  std::string pool_name = config->configValues["rbd_pool_name"];
  std::string volume_name = config->configValues["rbd_volume_name"];

  block_guard = new BlockGuard(total_size, block_size);
  BlockMap* block_ptr_map = block_guard->get_block_map();
  policy = new CachePolicy(total_size, cache_size, block_size, block_ptr_map,
                      new store::SimpleBlockStore(path, cache_size, block_size),
                      new store::RBDImageStore(pool_name, volume_name, block_size));

  go = true;
  //main_thread = new ThreadPool(1);
  //main_thread->schedule(std::bind(&HDCSCore::process, this));
}

HDCSCore::~HDCSCore() {
  go = false;
  delete hdcs_op_threads;
  delete policy;
  delete block_guard;
  //delete main_thread;
}

void HDCSCore::queue_io(Request *req) {
  //request_queue.enqueue((void*)req);
  process_request(req);
}

void HDCSCore::process() {
  while(go){
    Request *req = (Request*)request_queue.dequeue();
    if (req != nullptr) {
      process_request(req);
    }
  }
}

void HDCSCore::process_request(Request *req) {
  // Request -> list<BlockRequest> -> list<BlockOp>
  BlockRequestList block_request_list;
  block_guard->create_block_requests(req, &block_request_list);

  for (auto &block_request : block_request_list) {
    log_print("block %lu: %lu-%lu", block_request.block->block_id, block_request.offset, block_request.size); 
    map_block(std::move(block_request));
  }
}

void HDCSCore::map_block(BlockRequest &&block_request) {
  BlockOp *block_ops_end;
  Block* block = block_request.block;
  bool do_process = false;
  block->block_mutex.lock();
  BlockOp *block_ops_head = policy->map(std::move(block_request), &block_ops_end);
  if (!block->in_process) {
    block->in_process = true;
    block->block_ops_end = block_ops_end;
    do_process = true;
    log_print("Block not in process, block: %lu, new end: %p", block->block_id, block_ops_end);
  } else {
    log_print("Block in process, append request, block: %lu, append BlockOp: %p after BlockOp: %p, new end: %p", block->block_id, block_ops_head, block->block_ops_end, block_ops_end);
    block->block_ops_end->block_op_next = block_ops_head;
    block->block_ops_end = block_ops_end;
  }
  block->block_mutex.unlock();
  if (do_process) {
    hdcs_op_threads->schedule(std::bind(&BlockOp::send, block_ops_head));
    //block_ops_head->send();
  }
}

void HDCSCore::aio_read (char* data, uint64_t offset, uint64_t length,  void* arg) {
  Request *req = new Request(IO_TYPE_READ, data, offset, length, arg);
  process_request(req);
}

void HDCSCore::aio_write (const char* data, uint64_t offset, uint64_t length,  void* arg) {
  Request *req = new Request(IO_TYPE_WRITE, const_cast<char*>(data), offset, length, arg);
  process_request(req);
}

}// core
}// hdcs
