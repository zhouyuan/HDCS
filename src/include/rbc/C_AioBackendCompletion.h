#ifndef C_AIOBACKENDCOMPLETION_H
#define C_AIOBACKENDCOMPLETION_H

#include <inttypes.h>

#include "rbc/CacheEntry.h"

namespace rbc{
struct C_AioBackendCompletion{

    C_AioBackendCompletion(){}
    virtual void finish( ssize_t r ) = 0;

};

}
#endif
