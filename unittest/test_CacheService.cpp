//g++ test_CacheService.cpp  ../CacheService/CacheService.cpp ../Messenger/Messenger.cpp ../DataStore/BlockCacher/SimpleBlockCacher.cpp ../common/BufferList.cpp ../BackendStore/BackendStore.cpp ../CacheService/AgentService.cpp ../MetaStore/MetaStore.cpp ../CacheService/CacheEntry.cpp -o test -std=c++11 -lrados -lrbd -lboost_thread -lboost_system -lpthread -lmemcached -lrocksdb
#include "../CacheService/CacheService.h"


int main(){
    CacheService csd;
    csd.start();
    return 0;
}
