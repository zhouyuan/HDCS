//g++ -o test_librbc  test_librbc.cpp ../utils/librbc.cpp  ../CacheService/CacheService.cpp ../DataStore/BlockCacher/SimpleBlockCacher.cpp ../common/BufferList.cpp ../BackendStore/BackendStore.cpp ../CacheService/AgentService.cpp ../MetaStore/MetaStore.cpp ../Messenger/Messenger.cpp ../CacheService/CacheEntry.cpp -std=c++11 -lrados -lrbd -lboost_thread -lboost_system -lpthread -lmemcached -lrocksdb
#include "../utils/librbc.h"
#include "stdlib.h"
#include "stdio.h"

int main(int argc, char *argv[]){
    librbc rbc;
    char* op_type = argv[1];
    if(op_type[0] == 'w'){
        char* image_name = argv[2];
        uint64_t off = strtoul(argv[3], NULL, 0);
        char* data = argv[4];
        uint64_t length = sizeof data;
        rbc.rbc_write(image_name, off, length, data);
        std::cout << "rbc_write: " << data << std::endl;

    }else if(op_type[0] == 'r'){
        char* image_name = argv[2];
        uint64_t off = strtoul(argv[3], NULL, 0);
        uint64_t length = strtoul(argv[4], NULL, 0);
        char* data = new char[length];
        rbc.rbc_read(image_name, off, length, data);
        std::cout << "rbc_read: " << data << std::endl;

    }else{
        printf("Unrecognised type: ./test_librbc read/write volume_name offset data/length\n");
    }
    return 0;
}
