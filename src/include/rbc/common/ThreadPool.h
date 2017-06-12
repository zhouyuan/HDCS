#ifndef THREADPOOL_H
#define THREADPOOL_H

#include <stdio.h>
#include "rbc/common/lib/boost/threadpool/threadpool.hpp"

namespace rbc {
typedef boost::threadpool::pool ThreadPool;
}

#endif
