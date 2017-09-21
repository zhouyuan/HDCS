#ifndef HDCS_AIOCOMPLETIONIMP_H
#define HDCS_AIOCOMPLETIONIMP_H

#include "AioCompletion.h"

namespace hdcs{

class AioCompletionImp : public AioCompletion {
public:
  AioCompletionImp(std::function<void(ssize_t)>&& Callback) : Callback(Callback), data(nullptr) {
  }
  ~AioCompletionImp(){
    if (data != nullptr) {
      free(data);
    }
  }
  void complete(ssize_t r) {
    Callback(r);
    delete this;
  }
  ssize_t get_return_value() {};
  void wait_for_complete() {};
  void set_reserved_ptr(void* ptr) {
    data = (char*)ptr;
  }
  std::function<void(ssize_t)> Callback;
  char* data;
};

}// hdcs
#endif
