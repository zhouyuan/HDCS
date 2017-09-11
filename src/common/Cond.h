#ifndef COND_H
#define COND_H

#include <time.h>
#include <pthread.h>
#include <mutex>
#include <stdio.h>
#include <unistd.h>
#include <condition_variable>
#include <pthread.h>
#include <thread>

namespace rbc {
class SafeCond{
    //std::mutex m;    ///< Mutex to take
    //std::condition_variable cond;     ///< Cond to signal
    bool done;
    //pthread_mutex_t m;
    //pthread_cond_t cond;
public:
    SafeCond(): done(false){}

    void Signal() {
      //printf("enter cond signal\n");
      //std::unique_lock<std::mutex> lck(m);
      done = true;
      //printf("notify_all\n");
      //cond.notify_all();
      //pthread_cond_signal(&cond);
    }

    /// Returns rval once the Context is called
    void wait() {
      //std::unique_lock<std::mutex> lck(m);
      //pthread_mutex_lock(&m);
      //printf("start cond wait\n");
      //cond.wait(lck);
      while(!done){
          //sleep(0.001);
          std::this_thread::yield();
      }
      //pthread_cond_wait(&cond, &m);
      //pthread_mutex_unlock(&m);
      //printf("stop cond wait\n");
    }
};
}
#endif
