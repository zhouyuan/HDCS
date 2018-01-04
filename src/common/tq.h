// Copyright [2017] <Intel>
#ifndef WORK_QUEUE_HPP_
#define WORK_QUEUE_HPP_

#include <thread>
#include <mutex>
#include <vector>
#include <deque>
#include <list>
#include <future>
#include <functional>
#include <condition_variable>

namespace hdcs {
class TWorkQueue {
  typedef std::function<void(void)> fp_t;

  bool stop;
  bool binding;
  unsigned int num_core;
  std::deque<fp_t> job_queue;
  std::vector<std::thread> threads;
  std::mutex q_lock;
  std::condition_variable cond;

  void add_worker(unsigned thd_index) {
    std::thread t([this]() {
      while(1) {
        std::function<void()> task;
        {
          std::unique_lock<std::mutex> lock(q_lock);
          cond.wait(lock, [this]{ return this->stop || !this->job_queue.empty(); });

          if(this->stop && this->job_queue.empty()) {
            return;
          }

          task = std::move(job_queue.front());
          job_queue.pop_front();
        }
        task();
      }
    });
    if (binding) {
      cpu_set_t cpuset;
      CPU_ZERO(&cpuset);
      if (thd_index >= num_core) {
          // loop back
          CPU_SET(thd_index - num_core, &cpuset);
        } else {
          CPU_SET(thd_index, &cpuset);
        }
        int rc = pthread_setaffinity_np(t.native_handle(), sizeof(cpu_set_t), &cpuset);
    }
    threads.push_back(std::move(t));
  }

 public:
  TWorkQueue(size_t thd_cnt = 1, bool binding = false) : stop(false), binding(binding) {

    num_core = std::thread::hardware_concurrency();

    for ( unsigned i = 0; i < thd_cnt; ++i )
      add_worker(i);
    }
  ~TWorkQueue() {
    {
      std::unique_lock<std::mutex> lock(q_lock);
      stop = true;
    }
    cond.notify_all();
    for (auto &t : threads)
      t.join();
  }

  template<class F, class... Args>
  std::future<typename std::result_of<F(Args...)>::type> add_task(F&& f, Args&&... args)
  {
    using packaged_task_t = std::packaged_task<typename std::result_of<F(Args...)>::type ()>;
    std::shared_ptr<packaged_task_t> task(new packaged_task_t(
            std::bind(std::forward<F>(f), std::forward<Args>(args)...)
        ));

    auto ret = task->get_future();
    {
      std::unique_lock<std::mutex> lock(q_lock);

      if(stop) {
          throw std::runtime_error("add_task on stopped WorkQueue");
      }

      job_queue.push_back([task](){ (*task)(); });
    }

    cond.notify_one();

    return ret;
  }



};
}  //  namespace dslab

#endif  //  WORK_QUEUE_HPP_
